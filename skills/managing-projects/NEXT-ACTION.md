# Next Action Workflow

Tells the user exactly what to do right now based on today's plan and current time.

## Step 1: Check Today's Plan

1. Run `date` to get the current date and time.
2. Read `📋Planning/Daily Plan.md`.
3. Compare the date in the "Today's Focus" header against today's actual date.

**If no plan exists for today** → Stop. Tell the user: "No plan for today yet. Let's make one." → Route to DAILY-PLANNING workflow (`DAILY-PLANNING.md`).

**If a plan exists for today** → Continue to Step 2.

## Step 2: Locate the Current Time Slot

The daily plan contains a schedule with specific time slots (e.g., `08:00–10:00 — Deep work on X`). Parse all time slots and find:

1. **The slot the user is currently inside** (current time falls between start and end) → That's the active task.
2. **If between slots** (e.g., it's 10:15 and the next slot starts at 10:30) → Show the upcoming slot and how many minutes until it starts.
3. **If past all slots** → All scheduled work is done for the day. Congratulate and suggest rest or a bonus task from Nexus.

## Step 3: Present the Next Action

Present the single current or next action:

- **What**: The specific task from the time slot
- **Time**: "You're in the 08:00–10:00 block" or "Next up at 10:30"
- **Why**: Which goal/project/milestone it serves (reference the Prioritization Rationale)
- **How long**: Time remaining in the current slot, or duration of the next slot
- **Heads up**: If a fixed-time commitment (e.g., live class) is within 30 minutes, warn about it regardless of what slot they're in

Also check for unchecked items (`[ ]`) — if the current slot's task is already checked off, advance to the next unchecked slot.

## Rules

- **One action only.** Never present a list. Pick the single current/next item.
- **Respect the plan.** Don't re-prioritize. The planning happened earlier — now is execution time.
- **Be time-aware.** If a fixed appointment is approaching, always surface it as a heads-up even if it's not the current slot.
