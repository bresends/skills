# Planning Hierarchy & GTD Rules

## Hierarchy (top → bottom)

1. **Purpose** — Why you exist / what drives you (timeless)
2. **Vision** — What life looks like in 3-5 years
3. **Goals** — Measurable targets with deadlines (1-2 years)
4. **Projects** — Multi-step outcomes (Nexus DB + Obsidian)
5. **Tasks** — Concrete next actions

Every commitment should trace upward. If a task doesn't serve a project, goal, vision, or purpose — it's a distraction.

## Obsidian File Paths

All paths relative to vault root (cwd). **Always read these files at runtime** — their contents change over time.

| File                                      | Contains                                           |
| ----------------------------------------- | -------------------------------------------------- |
| `📋Planning/Purpose.md`                   | Life purposes with why/how                         |
| `📋Planning/Strategic Roadmap.md`          | Visions, SMART milestones (backward-mapped), milestone review log, and strategic decisions |
| `📋Planning/Daily Plan.md`                | Today's daily plan with time-slotted schedule      |
| `📋Planning/(Project) - Next Projects.md` | Queued/waiting projects (not yet active)           |
| `📋Planning/(Project) - Habits.md`        | Habit tracker project with learning tasks          |
| `📋Planning/About Me.md`                  | Personal context, skills, values                   |
| `📋Planning/Calendar.md`                  | Recurring commitments and upcoming events          |

## Nexus Database

Active projects and tasks live in the Nexus PostgreSQL database. Query via:

```bash
nix-shell ~/dev/skills/skills/managing-projects/shell.nix --run "python ~/dev/skills/skills/managing-projects/scripts/nexus_tasks.py <subcommand>"
```

Subcommands: `active-tasks`, `project-summary`, `search <query>`

For write operations (create-task, create-project, update-task, update-project, add-resource), use the filtering-youtube-videos's `nexus_db.py`:

```bash
nix-shell ~/dev/skills/skills/filtering-youtube-videos/shell.nix --run "python ~/dev/skills/skills/filtering-youtube-videos/scripts/nexus_db.py <subcommand> <args>"
```

## GTD Rules for Next Actions

- A next action must be **physical, visible, concrete** ("Call X about Y", not "Handle X situation")
- If it takes < 2 minutes, do it now
- One next action per project at a time — the very next physical step
- Weekly Review: process all inboxes, review all projects, update next actions
- **No "someday/maybe" lists.** If it doesn't align, it goes to the Graveyard with a rejection reason — not kept alive.
