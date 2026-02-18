---
name: evaluating-notes
description: >
  Evaluate and review Obsidian vault notes. Two modes:
  (1) Evaluate — score note alignment against Purpose/Vision/Goal/Projects.
  If aligned: fix tags, add Core Connections, improve frontmatter. If not: delete.
  (2) Review — check if you're applying the note's knowledge. Adaptive SRS timing.
  Use when: "evaluate this note", "is this note important?", "clean up this note",
  "review this note", "what should I review?", "am I applying this?", "note review"
---

# Note Evaluator & Reviewer

Evaluate Obsidian notes against the life hierarchy. Default answer is **no** — every note must serve your direction or it's dead weight. If a note doesn't connect to your life hierarchy, delete it. A note with no connections is an orphan. Orphans die. The user is a maniac hoarder — be harsh.

## Mode Routing

- **Evaluate** — "evaluate this note", "is this note important?", "clean up this note" → go to Evaluate Workflow
- **Review** — "review this note", "what should I review?", "am I applying this?" → go to Review Workflow

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

## Evaluate Workflow

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

## Review Workflow

### Review Step 1: Pick a Note

Two entry points:

- **User provides a note** → review that specific note.
- **User asks "what should I review?"** → scan all vault folders for notes where `next_review <= today`. Present the most overdue ones first. If none are overdue, say so.

### Review Step 2: Read and Ask for Evidence

Read the note. Then ask: **"What from this note have you applied recently? Give me one concrete example."**

One sentence. No scoring scales — just proof or honesty.

### Review Step 3: Judge Application

Based on the user's answer, categorize:

| Response                                    | Level            | Next Review Interval                                    |
| ------------------------------------------- | ---------------- | ------------------------------------------------------- |
| Concrete example with specifics             | **Practicing**   | `review_count * 30` days (cap 180)                      |
| Vague or partial ("I've been trying to...") | **Aware**        | 30 days                                                 |
| Nothing / honest "no"                       | **Not applying** | 14 days. Suggest one tiny action they can do this week. |
| "This is second nature now"                 | **Internalized** | 365 days                                                |

If a note has been "Not applying" for 2+ consecutive reviews (check the Application Log), force deletion: "If you're not doing this, it's not a priority. Focus on what matters." Ask for confirmation, then delete the file. No negotiation.

### Review Step 4: Update the Note

Update frontmatter:

- `last_review` → today's ISO timestamp
- `next_review` → today + calculated interval from Step 3
- `review_count` → increment by 1

Append to `## 📝 Application Log` at the bottom of the note. Create the section if it doesn't exist.

```markdown
## 📝 Application Log

- **2026-02-18** — [Practicing] "Used the 2-day rule when I skipped gym Monday — went Tuesday instead of letting it slide."
- **2026-01-15** — [Not applying] "Haven't thought about this since last review."
```

Format: `- **YYYY-MM-DD** — [Level] "user's evidence sentence"`

This is append-only. Never edit or remove previous entries.

### Review Step 5: Propose and Apply

Show the user the frontmatter changes and the new Application Log entry. Wait for approval before applying.
