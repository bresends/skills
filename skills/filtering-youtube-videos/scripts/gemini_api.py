#!/usr/bin/env python3
"""Gemini API calls for filtering-youtube-videos skill.

Subcommands:
  filter <youtube_url> <profile_path>   Analyze video against knowledge profile
  summarize <youtube_url>               Extract structured video summary (JSON)

Uses round-robin key rotation across GEMINI_API_KEYS (comma-separated).
Retries on 429 rate-limit errors by rotating to the next key (up to 3 attempts).
"""

import json
import os
import sys
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

SKILL_DIR = Path(__file__).resolve().parent.parent
load_dotenv(SKILL_DIR / ".env")

KEY_INDEX_FILE = Path("/tmp/filtering-youtube-videos-key-index")
MODEL = "gemini-3-flash-preview"


def get_api_keys() -> list[str]:
    raw = os.environ["GEMINI_API_KEYS"]
    keys = [k.strip() for k in raw.split(",") if k.strip()]
    if not keys:
        print("Error: GEMINI_API_KEYS is empty", file=sys.stderr)
        sys.exit(1)
    return keys


def rotate_key() -> tuple[str, int]:
    """Read current index, increment mod len(keys), write back, return (key, index)."""
    keys = get_api_keys()
    try:
        idx = int(KEY_INDEX_FILE.read_text().strip())
    except (FileNotFoundError, ValueError):
        idx = -1
    idx = (idx + 1) % len(keys)
    KEY_INDEX_FILE.write_text(str(idx))
    return keys[idx], idx


def call_gemini(contents, config=None, max_retries=3):
    """Call Gemini with automatic key rotation and retry on 429."""
    keys = get_api_keys()
    last_error = None

    for attempt in range(max_retries):
        api_key, idx = rotate_key()
        client = genai.Client(api_key=api_key)
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=config,
            )
            return response
        except Exception as e:
            last_error = e
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print(
                    f"Rate limited on key {idx}, rotating... (attempt {attempt + 1}/{max_retries})",
                    file=sys.stderr,
                )
                continue
            raise

    print(
        f"All {max_retries} attempts failed. Last error: {last_error}", file=sys.stderr
    )
    sys.exit(1)


# --- Summarize subcommand ---
class VideoSummary(BaseModel):
    topics: List[str] = Field(description="Main subjects and areas covered.")
    summary: str = Field(description="2-3 sentence summary of the video content.")
    key_concepts: List[str] = Field(
        description="Specific concepts, methods, or ideas discussed."
    )


SUMMARIZE_PROMPT = """\
Watch this video carefully. Produce a structured analysis extracting:
- The main subjects and areas covered
- A concise summary of what the video is about
- Specific concepts, methods, or ideas discussed

Be specific with topic names (e.g., "Stoic philosophy on adversity" not just "philosophy", \
"Real-time communication with WebSockets" not just "programming").
"""


def cmd_summarize(youtube_url: str):
    contents = types.Content(
        parts=[
            types.Part(file_data=types.FileData(file_uri=youtube_url)),
            types.Part(text=SUMMARIZE_PROMPT),
        ]
    )

    response = call_gemini(
        contents=contents,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": VideoSummary.model_json_schema(),
        },
    )

    result = VideoSummary.model_validate_json(response.text)
    output = result.model_dump()
    print(json.dumps(output, indent=2))


# --- Filter subcommand ---
def cmd_filter(youtube_url: str, profile_path: str):
    template_path = SKILL_DIR / "references" / "filter-prompt-template.md"
    template = template_path.read_text()

    profile_content = Path(profile_path).read_text()
    prompt = template.replace("{knowledge_profile}", profile_content)

    contents = types.Content(
        parts=[
            types.Part(file_data=types.FileData(file_uri=youtube_url)),
            types.Part(text=prompt),
        ]
    )

    response = call_gemini(contents=contents)
    print(response.text)


# --- Main ---


def main():
    if len(sys.argv) < 2:
        print("Usage: gemini_api.py <filter|summarize> <args...>", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "summarize":
        if len(sys.argv) < 3:
            print("Usage: gemini_api.py summarize <youtube_url>", file=sys.stderr)
            sys.exit(1)
        cmd_summarize(sys.argv[2])

    elif cmd == "filter":
        if len(sys.argv) < 4:
            print(
                "Usage: gemini_api.py filter <youtube_url> <profile_path>",
                file=sys.stderr,
            )
            sys.exit(1)
        cmd_filter(sys.argv[2], sys.argv[3])

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
