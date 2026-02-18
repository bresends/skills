# Gatekeeper Workflow

Evaluates new ideas/tasks/videos against the planning hierarchy. Default answer is **no**.

## Step 1: Understand the Input

What is the user proposing? Extract the core topic/subject. Is it a video to watch, a skill to learn, a project idea, a task?

**If the input contains a YouTube URL**, use Gemini to get the video summary:

```bash
nix-shell ~/dev/skills/skills/filtering-youtube-videos/shell.nix --run "python ~/dev/skills/skills/filtering-youtube-videos/scripts/gemini_api.py summarize '<youtube_url>'"
```

This returns JSON with `title`, `channel`, `topics`, `summary`, and `key_concepts`. Use this to understand what the video is about before proceeding to alignment.

## Step 2: Check the Graveyard First

Before doing a full evaluation, search the Graveyard project for this idea:

```bash
nix-shell ~/dev/skills/skills/managing-projects/shell.nix --run "python ~/dev/skills/skills/managing-projects/scripts/nexus_tasks.py search '<keyword>'"
```

**If the idea is already in the Graveyard** → Show the user the existing entry with its rejection reasoning. Say: "You already evaluated this on [date]. Here's why you said no: [reason]. Has something changed?" Only proceed with a full re-evaluation if the user can articulate what's different now.

## Step 3: Load the Hierarchy

Read these files (in order):

1. `📋Planning/Purpose.md`
2. `📋Planning/Strategic Roadmap.md`
3. `📋Planning/About Me.md` (background and identity)

## Step 4: Alignment Check

For each level, check alignment:

- **Purpose**: Does this serve any life purpose? Which one(s)?
- **Vision**: Does this advance any 3-5 year vision? Which one(s)?
- **Goal**: Does this contribute to any 1-2 year goal?
- **Project**: Does it fit into any active project?

```bash
nix-shell ~/dev/skills/skills/managing-projects/shell.nix --run "python ~/dev/skills/skills/managing-projects/scripts/nexus_tasks.py project-summary"
```

Present a clear alignment score:

```text
Purpose  ✅/❌
Vision   ✅/❌
Goal     ✅/❌
Project  ✅/❌
```

Always think about the danger of confusing "motion" (doing lots of small things) with "progress" (moving the needle). Make the user focus on tasks that are high-impact.

## Step 5: Make the Call

- **4/4 or 3/4** → **File it.** Help place it in Nexus.
- **2/4** → **Challenge it.** "This loosely connects to [purpose] but doesn't advance any active goal or project. This is a distraction."
- **1/4 or 0/4** → **Discard it.** "This doesn't align with your current direction. Your milestones for [period] are [X, Y, Z]. This would pull you away from those."

## Step 6: File or Bury

**If filing (3-4/4):**

1. Find the right project via `project-summary`
2. File using `nexus_db.py`:

```bash
echo '{"project_id": <id>, "name": "...", "description": "..."}' | nix-shell ~/dev/skills/skills/filtering-youtube-videos/shell.nix --run "python ~/dev/skills/skills/filtering-youtube-videos/scripts/nexus_db.py create-task -"
```

**If discarding (0-2/4) → Send to the Graveyard (project ID: 49):**

- Be hard on the user. Reinforce what they should focus on instead (reference current milestones).
- File the idea as a task in the **Graveyard** project (ID: 49) with:
  - **name**: The idea/topic/video title
  - **description**: The alignment score, rejection reasoning, what the user should focus on instead, and the date. Include the URL if one was provided.
  - **status**: `done` (it's dead on arrival)

```bash
echo '{"project_id": 49, "name": "<idea>", "description": "Rejected YYYY-MM-DD. Purpose ✅/❌ | Vision ✅/❌ | Goal ✅/❌ | Project ✅/❌. Reason: <why>. Focus instead on: <current milestones>.", "status": "done"}' | nix-shell ~/dev/skills/skills/filtering-youtube-videos/shell.nix --run "python ~/dev/skills/skills/filtering-youtube-videos/scripts/nexus_db.py create-task -"
```

The Graveyard is not a "someday/maybe" list. It's a cemetery — ideas go there to stay dead. Its purpose is to prevent re-evaluation loops, not to keep options open.
