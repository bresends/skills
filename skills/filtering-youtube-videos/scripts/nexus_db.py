#!/usr/bin/env python3
"""Nexus database operations for filtering-youtube-videos skill.

Subcommands:
  list-projects          List all projects with id, name, description, status
  list-tasks <pid>       List tasks for a project
  create-project <json>  Create a project (JSON: name, description, purpose)
  create-task <json>     Create a task (JSON: project_id, name, description)
  add-resource <json>    Add a resource (JSON: task_id, title, url, type, is_consumed)
  update-resource <json> Update a resource (JSON: resource_id, and any of: is_consumed, notes)
  update-task <json>     Update a task (JSON: task_id, and any of: name, description)
  check-url <url>        Check if a URL already exists in resources

Outputs JSON to stdout.
"""

import sys
import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

SKILL_DIR = Path(__file__).resolve().parent.parent
load_dotenv(SKILL_DIR / ".env")

DATABASE_URL = os.environ["DATABASE_URL"]


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def list_projects():
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "SELECT id, name, description, purpose, status, priority, is_active "
            "FROM projects ORDER BY is_active DESC, updated_at DESC"
        )
        return cur.fetchall()


def list_tasks(project_id: int):
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "SELECT id, name, description, status, priority "
            "FROM tasks WHERE project_id = %s ORDER BY sort_order",
            (project_id,),
        )
        return cur.fetchall()


def create_project(data: dict):
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "INSERT INTO projects (name, description, purpose, status, is_active) "
            "VALUES (%(name)s, %(description)s, %(purpose)s, 'Planning', false) "
            "RETURNING id, name",
            data,
        )
        conn.commit()
        return cur.fetchone()


def create_task(data: dict):
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "SELECT COALESCE(MAX(sort_order), -1) + 1 AS next_order "
            "FROM tasks WHERE project_id = %(project_id)s",
            data,
        )
        data["sort_order"] = cur.fetchone()["next_order"]
        cur.execute(
            "INSERT INTO tasks (project_id, name, description, sort_order) "
            "VALUES (%(project_id)s, %(name)s, %(description)s, %(sort_order)s) "
            "RETURNING id, name",
            data,
        )
        conn.commit()
        return cur.fetchone()


def update_task(data: dict):
    task_id = data.pop("task_id")
    allowed = {"name", "description", "status", "priority", "sort_order", "context", "due_date", "project_id"}
    fields = {k: v for k, v in data.items() if k in allowed}
    if not fields:
        raise ValueError("No valid fields to update (allowed: name, description, status, priority, sort_order, context, due_date)")
    set_clause = ", ".join(f"{k} = %({k})s" for k in fields)
    fields["task_id"] = task_id
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            f"UPDATE tasks SET {set_clause} WHERE id = %(task_id)s RETURNING id, name",
            fields,
        )
        conn.commit()
        return cur.fetchone()


def update_project(data: dict):
    project_id = data.pop("id")
    allowed = {"name", "description", "purpose", "desired_outcome", "deadline", "status", "priority", "is_active"}
    fields = {k: v for k, v in data.items() if k in allowed}
    if not fields:
        raise ValueError("No valid fields to update")
    set_clause = ", ".join(f"{k} = %({k})s" for k in fields)
    fields["id"] = project_id
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            f"UPDATE projects SET {set_clause} WHERE id = %(id)s RETURNING id, name, status",
            fields,
        )
        conn.commit()
        return cur.fetchone()


def add_resource(data: dict):
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "SELECT COALESCE(MAX(sort_order), -1) + 1 AS next_order "
            "FROM resources WHERE task_id = %(task_id)s",
            data,
        )
        data["sort_order"] = cur.fetchone()["next_order"]
        data.setdefault("notes", None)
        cur.execute(
            "INSERT INTO resources (task_id, title, url, type, is_consumed, sort_order, notes) "
            "VALUES (%(task_id)s, %(title)s, %(url)s, %(type)s, %(is_consumed)s, %(sort_order)s, %(notes)s) "
            "RETURNING id, title, url",
            data,
        )
        conn.commit()
        return cur.fetchone()


def update_resource(data: dict):
    resource_id = data.pop("resource_id")
    allowed = {"is_consumed", "notes"}
    fields = {k: v for k, v in data.items() if k in allowed}
    if not fields:
        raise ValueError("No valid fields to update (allowed: is_consumed, notes)")
    set_clause = ", ".join(f"{k} = %({k})s" for k in fields)
    fields["resource_id"] = resource_id
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            f"UPDATE resources SET {set_clause} WHERE id = %(resource_id)s RETURNING id, title, url, is_consumed",
            fields,
        )
        conn.commit()
        return cur.fetchone()


def extract_video_id(url: str) -> str | None:
    """Extract YouTube video ID from various URL formats."""
    parsed = urlparse(url)
    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        return parse_qs(parsed.query).get("v", [None])[0]
    if parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")
    return None


def check_url(url: str):
    video_id = extract_video_id(url)
    if not video_id:
        return None
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "SELECT r.id, r.title, r.url, r.is_consumed, t.name AS task_name, "
            "p.name AS project_name FROM resources r "
            "JOIN tasks t ON r.task_id = t.id "
            "JOIN projects p ON t.project_id = p.id "
            "WHERE r.url LIKE %s OR r.url LIKE %s",
            (f"%youtube.com/watch?v={video_id}%", f"%youtu.be/{video_id}%"),
        )
        return cur.fetchone()


def read_json_arg(arg: str) -> dict:
    """Read JSON from argument or stdin if arg is '-'."""
    if arg == "-":
        return json.load(sys.stdin)
    return json.loads(arg)


def main():
    if len(sys.argv) < 2:
        print("Usage: nexus_db.py <subcommand> [args]", file=sys.stderr)
        print("  JSON commands: pass '-' to read from stdin, or pass JSON directly", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "list-projects":
        result = list_projects()
    elif cmd == "list-tasks":
        result = list_tasks(int(sys.argv[2]))
    elif cmd == "create-project":
        result = create_project(read_json_arg(sys.argv[2]))
    elif cmd == "create-task":
        result = create_task(read_json_arg(sys.argv[2]))
    elif cmd == "update-project":
        result = update_project(read_json_arg(sys.argv[2]))
    elif cmd == "update-task":
        result = update_task(read_json_arg(sys.argv[2]))
    elif cmd == "add-resource":
        result = add_resource(read_json_arg(sys.argv[2]))
    elif cmd == "update-resource":
        result = update_resource(read_json_arg(sys.argv[2]))
    elif cmd == "check-url":
        result = check_url(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, default=str, indent=2))


if __name__ == "__main__":
    main()
