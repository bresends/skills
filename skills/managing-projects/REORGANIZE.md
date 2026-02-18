Move tasks between projects, close projects, and clean up scope.

### Operations

**Move a task to another project** — update its `project_id`. Resources follow automatically:

```bash
echo '{"task_id": <id>, "project_id": <new_project_id>}' | nix-shell .claude/skills/filtering-youtube-videos/shell.nix --run "python .claude/skills/filtering-youtube-videos/scripts/nexus_db.py update-task -"
```

**Close a project** — mark as Completed via `update-project`:

```bash
echo '{"id": <project_id>, "status": "Completed"}' | nix-shell .claude/skills/filtering-youtube-videos/shell.nix --run "python .claude/skills/filtering-youtube-videos/scripts/nexus_db.py update-project -"
```

**Update a project** — change status, priority, is_active, name, description, purpose, desired_outcome, deadline:

```bash
echo '{"id": <project_id>, "status": "On Hold"}' | nix-shell .claude/skills/filtering-youtube-videos/shell.nix --run "python .claude/skills/filtering-youtube-videos/scripts/nexus_db.py update-project -"
```

### Workflow

1. List projects and tasks to understand the current state
2. Identify misplaced tasks — tasks that don't align with their project's purpose
3. Propose moves: show source project, task name, and destination project
4. Execute moves by updating `project_id` on each task
5. Close or update projects that are now empty or completed
