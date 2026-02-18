#!/usr/bin/env python3
"""SEI automation via Playwright.

Subcommands:
  login                    — Authenticate and save session
  tag <process_id> <tag>   — Tag a process in SEI
  extract-pdf <process_id> — Download full process as PDF
  list-processes [filter]  — List processes matching filter

Usage:
  nix-shell .claude/skills/automating-sei-workflows/shell.nix --run \
    "python .claude/skills/automating-sei-workflows/scripts/sei.py <cmd> [args]"
"""

import json
import sys
from pathlib import Path

from dotenv import load_dotenv

SKILL_DIR = Path(__file__).resolve().parent.parent
load_dotenv(SKILL_DIR / ".env")


def usage():
    print(__doc__)
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        usage()

    cmd = sys.argv[1]

    if cmd == "login":
        print(json.dumps({"status": "not_implemented", "message": "Login workflow not yet implemented"}))
    elif cmd == "tag":
        print(json.dumps({"status": "not_implemented", "message": "Tag workflow not yet implemented"}))
    elif cmd == "extract-pdf":
        print(json.dumps({"status": "not_implemented", "message": "PDF extraction not yet implemented"}))
    elif cmd == "list-processes":
        print(json.dumps({"status": "not_implemented", "message": "List processes not yet implemented"}))
    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
