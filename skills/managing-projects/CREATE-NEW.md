# How to create new projects

## Concept

A project is obliged to have:

1. **A clear goal** — what are you building?
2. **A clear "good enough"** — what satisfies v1.0?
3. **A clear ending** — when does this stop?

## Create new project workflow

Copy this checklist and check off items as you complete them:

```text
Create new project progress:
- [ ] Step 1: Ask and undersantand what the user want to build
- [ ] Step 2: Define purpose
- [ ] Step 3: Brainstorm
- [ ] Step 4: Cut for v1.0
- [ ] Step 5: Create a definition of done (DOD)
- [ ] Step 6: File new project to Nexus
```

## Workflow

### Step 1: Ask and understand

- **Ask** what they want to build — understand the rough idea.
- Here push the concept he doesn't need more ideas or better planning. They need to finish projects or kill them. Publicly. Permanently.
  A project you're not actively working on is not "waiting" — it's dead. Call it dead.

### Step 2: Define purpose

- Question why this matters. What does finishing this unlock or enable?
- Push back here. Analyze if it is really important for the greater picture of the user life.
- Make the user try to give up on doing that. Show their priorities.
- Here you should explore the user 📋Planning folder. A project should mandatory be linked to his goals, values or purpose. Push back hard here.

### Step 3: Brainstorm

- After all the back and forth, if the project is really gonna be made encourage listing every feature/requirement imaginable, no filter. Help the user with good questions.
- Help to write every feature imaginable, even ridiculous ones.

### Step 4: Cut for (v.1.0)

- Present the list with the requirements, ask to rank each 1–5 (only 5s make v.1.0).
- Encourage cutting ruthlessly — v1 is about finishing, not perfection

### Step 5: Create the definition of done (DOD)

- Based on the requirements and tasks selected for v.1.0 help the user to create a definition of done. It should be the name of the project to point to the user the exact criteria or moment when that project will be done.
- Turn surviving features into checkable requirements. Each item must be something you can put a check mark next to and be sure it's complete. If you can't check it off, the project has permission to continue forever.

### Step 6: File project to Nexus

- Add Time Constraint: Decide how long this project is allowed to exist: a week, a month, a year. Different projects have different timelines, but it must be defined. When time runs out, choose: ship as-is, stop, or cut requirements.

- Use `create-project` with name (following the rules), description (the done list), purpose, deadline. Then `create-task` for each requirement

Output summary: project name, purpose, v1 done list, deadline, tasks created.
