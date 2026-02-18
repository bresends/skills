---
name: filtering-youtube-videos
description: >
  End-to-end YouTube video pipeline: filter videos against your knowledge profile
  using Gemini, update knowledge profiles, and file videos into Nexus.
  Combines knowledge filtering and Nexus filing into a single automated workflow.
  Use when: the user shares a YouTube link, wants to filter/triage a video,
  evaluate if a video is worth watching, file a video into a project, or mentions
  "youtube filter", "youtube triage", "filter video", "is this worth watching",
  "file this video", "add video to nexus", "save to nexus", or "sort video".
disable-model-invocation: true
---

# YouTube Pipeline

Filter YouTube videos against your existing knowledge using Gemini, update knowledge profiles, and file videos into Nexus — all in one workflow.

## Setup

Requires `.env` in the skill directory with:

```bash
GEMINI_API_KEYS=key1,key2,key3   # Comma-separated, rotated to avoid rate limits
DATABASE_URL=postgresql://...
```

MANDATORY: When using this skill the timeout should be changed to 10 minutes!

## Nix Shell

All Python scripts run via:

```bash
nix-shell ~/dev/skills/skills/filtering-youtube-videos/shell.nix --run "python ~/dev/skills/skills/filtering-youtube-videos/scripts/<script>.py <args>"
```

## Guiding Principles

- **Think before matching.** Consider whether the video truly belongs in a project or is just tangentially related.
- **Push back when it doesn't fit.** If no project is a good home, say so. Sometimes the answer is "just watch it, don't file it."
- **Prefer existing homes over new projects.** Creating a new project is overhead. Only suggest it when nothing fits.
- **Respect the user's time.** The whole point of filtering is to avoid rabbit holes — if the verdict is SKIP, don't push them to file it anyway.

## Workflow

### Step 1: Extract Video Information

When the user provides a YouTube URL, immediately fetch:

**Video title and channel:**

```bash
nix-shell -p curl jq --run "curl -sf 'https://www.youtube.com/oembed?url=<youtube_url>&format=json' | jq -r '\"Channel: \\(.author_name)\", \"Title: \\(.title)\"'"
```

**Is duplicated?:**

```bash
nix-shell ~/dev/skills/skills/filtering-youtube-videos/shell.nix --run \
  "python ~/dev/skills/skills/filtering-youtube-videos/scripts/nexus_db.py check-url '<youtube_url>'"
```

If the video already exists in Nexus, inform the user which project/task it belongs to and **stop** (don't continue).

### Step 2: Resolve Knowledge Profile

Verify for the following files in `🧠Knowledge Profiles/` directory a profile that matches the video's subject:

`ls "🧠Knowledge Profiles/"`

Compare filenames against the video title, channel, and topic area. Present the best match and confirm with the user.

**If a profile exists**: Read it and ask if they want to use it as-is or update it first.

**If no profile matches**: Run guided Q&A to create one. Ask these questions one at a time, conversationally:

1. "What topic does this video fall under for you?"
2. "What core concepts can you already explain about **[subject]**?"
3. "What terminology or jargon are you comfortable with?"
4. "What have you already studied, watched, or built related to this?"
5. "What areas feel fuzzy or uncertain to you?"
6. "What specific questions are you trying to answer?"

Save the profile to `🧠Knowledge Profiles/[Subject].md`:

```markdown
---
subject: "[Subject]"
date_created: [today]
date_updated: [today]
tags: [knowledge-profile, relevant-tags]
---

# [Subject]

## Known Concepts

- [from Q&A answers]

## Familiar Terminology

- [from Q&A answers]

## Study History

- [from Q&A answers]

## Knowledge Gaps

- [from Q&A answers]

## Open Questions

- [from Q&A answers]
```

**Escape hatch**: If the user wants to skip filtering and go straight to filing, jump to Step 6.

### Step 3: Filter Analysis

Run the Gemini-powered filter analysis:

```bash
nix-shell ~/dev/skills/skills/filtering-youtube-videos/shell.nix --run \
  "python ~/dev/skills/skills/filtering-youtube-videos/scripts/gemini_api.py filter '<youtube_url>' '<profile_path>'"
```

Present the full analysis to the user. The output includes a WATCH/SKIM/SKIP verdict with score, known vs. new concepts, timestamps, and gap analysis.

**Escape hatch**: If verdict is SKIP and the user agrees, stop here — no need to file it.

### Step 4: Review & Update Knowledge Profile

Discuss the filter results conversationally:

- Which "new concepts" are genuinely new vs. things they knew but weren't in the profile?
- Which gaps or open questions from the profile does this video address?
- Any surprising findings or things they want to dig deeper into?

If the user agrees, update the knowledge profile:

- Move learned concepts from **Knowledge Gaps** / **Open Questions** to **Known Concepts**
- Add new terminology to **Familiar Terminology**
- Add the video to **Study History** (title + brief note on what was gained)
- Add any new questions that arose to **Open Questions**
- Update `date_updated` in frontmatter

### Step 6: Video Summary for Nexus

Use context from the filter analysis (Step 3) if it provides enough information about the video's content and topics.

If there's no filter analysis (user skipped filtering) or it lacks sufficient context, run the summarize command:

```bash
nix-shell ~/dev/skills/skills/filtering-youtube-videos/shell.nix --run \
  "python ~/dev/skills/skills/filtering-youtube-videos/scripts/gemini_api.py summarize '<youtube_url>'"
```

Present a brief summary:

**[Verified Title]** by _[Verified Channel]_

> [summary]
> Topics: [topics]

### Step 7: Match to a Project

```bash
nix-shell ~/dev/skills/skills/filtering-youtube-videos/shell.nix --run \
  "python ~/dev/skills/skills/filtering-youtube-videos/scripts/nexus_db.py list-projects"
```

Compare video topics against project names, descriptions, and purposes. Then **have a conversation**:

1. Present top matching projects with a brief reason for each match.
2. If a match is weak, say so honestly — "This is a loose fit because..."
3. If nothing fits well, consider:
   - Could it be a task under a broader existing project?
   - Is this something the user should just watch without filing?
   - Does it warrant a new project? (Only as a last resort)
4. Ask the user to pick one, or discuss further.

**If creating a new project**:

```bash
nix-shell ~/dev/skills/skills/filtering-youtube-videos/shell.nix --run "python3 -c '
import json
data = {
    \"name\": \"...\",
    \"description\": \"...\",
    \"purpose\": \"...\"
}
print(json.dumps(data))
' | python ~/dev/skills/skills/filtering-youtube-videos/scripts/nexus_db.py create-project -"
```

### Step 8: Match to a Task

```bash
nix-shell ~/dev/skills/skills/filtering-youtube-videos/shell.nix --run \
  "python ~/dev/skills/skills/filtering-youtube-videos/scripts/nexus_db.py list-tasks <project_id>"
```

1. Does the video fit an existing task? Present matches with reasons.
2. If creating a new task, match the naming style of sibling tasks.
3. Suggest a task name and description — let the user confirm or adjust.

```bash
nix-shell ~/dev/skills/skills/filtering-youtube-videos/shell.nix --run "python3 -c '
import json
data = {
    \"project_id\": <id>,
    \"name\": \"...\",
    \"description\": \"...\"
}
print(json.dumps(data))
' | python ~/dev/skills/skills/filtering-youtube-videos/scripts/nexus_db.py create-task -"
```

**If renaming or updating a task**:

```bash
nix-shell ~/dev/skills/skills/filtering-youtube-videos/shell.nix --run "python3 -c '
import json
data = {
    \"task_id\": <id>,
    \"name\": \"...\"
}
print(json.dumps(data))
' | python ~/dev/skills/skills/filtering-youtube-videos/scripts/nexus_db.py update-task -"
```

### Step 9: Add Resource & Confirm

Ask: "Have you already watched this video?"

The resource title must use the **Verified** title and channel: `(Channel Name) - Video Title`.

Include a `notes` field with a brief summary. Use context from the filter analysis or video summary.

**Recommended approach** (no escaping issues, handles special characters):

```bash
nix-shell ~/dev/skills/skills/filtering-youtube-videos/shell.nix --run "python3 -c '
import json
data = {
    \"task_id\": <id>,
    \"title\": \"(<channel>) - <title>\",
    \"url\": \"<youtube_url>\",
    \"type\": \"video\",
    \"is_consumed\": <True|False>,
    \"notes\": \"<summary>\"
}
print(json.dumps(data))
' | python ~/dev/skills/skills/filtering-youtube-videos/scripts/nexus_db.py add-resource -"
```

Confirm:

> Added **[title]** to project **[project]** / task **[task]** (watched: yes/no)
