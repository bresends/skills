---
name: evaluating-notes
description: >
  Evaluate Obsidian vault note's alignment with life priorities. Score it against
  Purpose/Vision/Goal/Projects. If aligned: fix tags, add Core Connections,
  improve frontmatter. If not: delete it.
  Use when: "evaluate this note", "is this note important?", "clean up this note",
  "review note", "check this note"
---

# Note Evaluator

Evaluate Obsidian notes against the life hierarchy. Default answer is **no** — every note must serve your direction or it's dead weight. If a note doesn't connect to your life hierarchy, delete it. A note with no connections is an orphan. Orphans die. The user is a maniac hoarder — be harsh.

## Vault

All notes live under the `cwd` directory.

**Planning files (never evaluate these — they are the anchors):**

- `📋Planning/Purpose.md` — life purposes
- `📋Planning/Strategic Roadmap.md` — visions, goals, milestones
- `📋Planning/About Me.md` — background and identity

## Database Access

Fetch active projects from Nexus:

```bash
nix-shell ~/dev/skills/skills/managing-projects/shell.nix --run "python ~/dev/skills/skills/managing-projects/scripts/nexus_tasks.py project-summary"
```

## Workflow

### Step 1: Read the Note

Accept the note path (absolute or relative to vault root). Read the note contents, existing tags, frontmatter, and links.

### Step 2: Load the Hierarchy

Read these files (in order):

1. `📋Planning/Purpose.md`
2. `📋Planning/Strategic Roadmap.md`
3. `📋Planning/About Me.md`
4. Fetch active projects via `nexus_tasks.py project-summary`

Extract all H1/H2 section headings from Purpose.md and Strategic Roadmap.md — these are the available link targets for Core Connections.

### Step 3: Alignment Scoring

Score the note against 4 levels (same format as the Gatekeeper):

```text
Purpose  ✅/❌  — Does this note serve any life purpose?
Vision   ✅/❌  — Does it advance any 3-5 year vision?
Goal     ✅/❌  — Does it contribute to any 1-2 year goal/milestone?
Project  ✅/❌  — Does it fit into any active project?
```

Present the score with a brief justification for each level.

### Step 4: Make the Call

- **3-4/4** → Important. Proceed to Step 5 (improve the note).
- **2/4** → Challenge: "This loosely connects but doesn't advance your active direction." Ask the user: keep or delete?
- **0-1/4** → Recommend deletion. State what the user should focus on instead (current milestones). Ask for confirmation, then delete the file.

### Step 5: Note Quality Audit (important notes only)

Check against this quality checklist:

| Check            | Expected                                                                                                        |
| ---------------- | --------------------------------------------------------------------------------------------------------------- |
| Frontmatter      | Has `date_created`, `last_review`, `next_review`, `review_count`, `recurring`, `tags`                           |
| Tags             | 1-3 relevant tags in kebab-case                                                                                 |
| Core Connections | Has `# 🔗Core Connections` section at the top (after frontmatter) with wiki links to relevant Planning sections |
| Content depth    | More than a stub — has structured content with headings                                                         |

If the note is a **stub** (just a link, a sentence, or empty body) but scores 3-4/4, flag it: "This topic aligns but the note has no substance. Flesh it out or delete it — a placeholder is not a note." Ask the user to decide.

### Step 6: Propose and Apply Changes

Show the user exactly what will be added or changed. Wait for approval before applying.

Changes to propose:

1. **Fix frontmatter** — add missing fields (`date_created`, `last_review`, `next_review`, `review_count`, `recurring`, `tags`)
2. **Add/update tags** — 1-3 relevant kebab-case tags based on content
3. **Add Core Connections section** — insert `# 🔗Core Connections` after frontmatter, linking to the specific section headings in Purpose.md and Strategic Roadmap.md that the note relates to

Core Connections format:

```markdown
# 🔗Core Connections

- [[📋Planning/Purpose#📚 Learn throughout life]]
- [[📋Planning/Strategic Roadmap#🛠️ Building a Personal Productivity Ecosystem (Since Jan 2025)]]
```

Link to the **specific section heading** extracted in Step 2 — not just the file. Use the exact heading text including emojis.
