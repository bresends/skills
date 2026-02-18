# Daily Planning Workflow

The most important workflow. Builds today's hour-by-hour plan through conversation.

## Step 1: Calendar Check

1. Run `date` to get the current date, time, and day of week.
2. Read `📋Planning/Calendar.md`. Identify:
   - Recurring items for today's day-of-week (e.g., pull-up training on Mon/Wed/Fri)
   - Any deadlines or upcoming events
3. Present everything relevant to today.
4. Ask: "Anything else happening today I should know about?" (appointments, errands, obligations, energy level, wake-up time)

These become **fixed slots** — they go into the schedule first and everything else fits around them.

## Step 2: Staleness Check

Read the `milestones_reviewed` frontmatter in `📋Planning/About Me.md`. Compare to today's date.

**If >30 days since last review** → Stop. Do not plan. Force a milestone review first:

1. Read milestones and goals files.
2. For each milestone, ask: "Did you accomplish this? Current status?"
3. Update files with honest current reality — remove accomplished, re-date pending, discard abandoned.
4. Update `milestones_reviewed` to today's date.
5. Only then proceed to Step 3.

## Step 3: Gather Commitments

Run these commands to get the full picture:

```bash
nix-shell ~/dev/skills/skills/managing-projects/shell.nix --run "python ~/dev/skills/skills/managing-projects/scripts/nexus_tasks.py active-tasks"
nix-shell ~/dev/skills/skills/managing-projects/shell.nix --run "python ~/dev/skills/skills/managing-projects/scripts/nexus_tasks.py project-summary"
```

Also read `📋Planning/Strategic Roadmap.md` for milestone deadlines.

## Step 4: Interactive Planning

Present to the user:

1. **Fixed commitments** (from calendar + user input) — these are locked in
2. **Top priority tasks** from Nexus, ranked by:
   - Deadline proximity (hard deadlines first)
   - Milestone alignment (what moves the needle on current milestones?)
   - Completion proximity (almost-done projects get priority — finish what you started)
3. **Ask the user to pick** what goes into today

**Push back if they try to overload.** A realistic day has 6-8 hours of productive work, not 14. Account for transitions, breaks, meals, and energy dips. Discuss tradeoffs openly — "If you add X, what gets cut?"

## Step 5: Build the Schedule

Organize selected items into specific time slots with start and end times:

### Scheduling principles:

- **Deep work early.** Cognitively demanding tasks (studying, coding, writing) go in the first hours of the day.
- **Fixed appointments are anchors.** Schedule everything else around them.
- **Buffer between slots.** Leave 15-30 min gaps for transitions, not back-to-back.
- **Energy curve.** Hardest work early → medium tasks midday → lightest in evening.
- **Time estimates are mandatory.** Every task gets a realistic duration. Round up, not down.
- **No slot longer than 2 hours** without a break. Split long tasks into focused blocks.

### Example format:

```
08:00–10:00 — Deep work: Draft Auditor Fiscal study plan (2h)
10:00–10:30 — Break
10:30–11:30 — Perícia live class (1h)
11:30–12:00 — Review notes from class (30min)
12:00–13:00 — Lunch
13:00–14:30 — Code: Implement feature X (1.5h)
14:30–15:00 — Break / walk
15:00–16:00 — Pull-up training + shower (1h)
19:00–20:00 — Watch recorded Perícia class (1h)
```

Confirm the schedule with the user before writing.

## Step 6: Write the Plan

Overwrite `📋Planning/Daily Plan.md` with the finalized plan using this format:

```markdown
# Daily Plan

## Notes about important next events (give maximum priority)

- [Any critical upcoming deadlines or events]

## Today's Focus (Day: YYYY-MM-DD, Weekday)

- **[Daily Goal]** One-sentence summary of the day's main objective

## Prioritization Rationale

[2-3 sentences explaining why these tasks were chosen and what they advance]

## Schedule

- [ ] 08:00–10:00 — Deep work: [task] (2h)
- [ ] 10:00–10:30 — Break
- [ ] 10:30–11:30 — [fixed commitment] (1h)
- [ ] 13:00–14:30 — [task] (1.5h)
- [ ] 15:00–16:00 — [task] (1h)
- [ ] 19:00–20:00 — [task] (1h)
```

Each task is a checkbox with a specific time slot, description, and duration.

**Important:** Always use emojis in the Daily Plan headers. Match or improve upon the emoji style already in the file.
