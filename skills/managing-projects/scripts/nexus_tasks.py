#!/usr/bin/env python3
"""Nexus task queries for managing-projects skill.

Subcommands:
  active-tasks      Actionable tasks from active projects (excludes Done/Cancelled)
  project-summary   Compact overview: project name, purpose, task count, status
  search <query>    Find tasks/projects matching a keyword

Outputs JSON to stdout.
"""

import sys
import json
import os
from pathlib import Path

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

SKILL_DIR = Path(__file__).resolve().parent.parent
load_dotenv(SKILL_DIR / ".env")

DATABASE_URL = os.environ["DATABASE_URL"]


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def active_tasks():
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT
                t.id AS task_id,
                t.name AS task_name,
                t.description AS task_description,
                t.status AS task_status,
                t.priority AS task_priority,
                p.id AS project_id,
                p.name AS project_name,
                p.purpose AS project_purpose,
                p.status AS project_status
            FROM tasks t
            JOIN projects p ON t.project_id = p.id
            WHERE p.is_active = true
              AND LOWER(t.status) NOT IN ('done', 'cancelled')
            ORDER BY p.priority DESC NULLS LAST, p.name, t.sort_order
        """)
        return cur.fetchall()


def project_summary():
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT
                p.id,
                p.name,
                p.purpose,
                p.status,
                p.priority,
                p.is_active,
                COUNT(t.id) AS task_count,
                COUNT(t.id) FILTER (WHERE LOWER(t.status) = 'done') AS done_count
            FROM projects p
            LEFT JOIN tasks t ON t.project_id = p.id
            WHERE p.is_active = true
            GROUP BY p.id
            ORDER BY p.priority DESC NULLS LAST, p.name
        """)
        return cur.fetchall()


def search(query: str):
    pattern = f"%{query}%"
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT 'project' AS type, id, name, description, purpose, status, is_active
            FROM projects
            WHERE name ILIKE %s OR description ILIKE %s OR purpose ILIKE %s
            ORDER BY is_active DESC, name
        """, (pattern, pattern, pattern))
        projects = cur.fetchall()

        cur.execute("""
            SELECT 'task' AS type, t.id, t.name, t.description, t.status,
                   p.name AS project_name, p.is_active AS project_active
            FROM tasks t
            JOIN projects p ON t.project_id = p.id
            WHERE t.name ILIKE %s OR t.description ILIKE %s
            ORDER BY p.is_active DESC, p.name, t.sort_order
        """, (pattern, pattern))
        tasks = cur.fetchall()

        return {"projects": projects, "tasks": tasks}


def main():
    if len(sys.argv) < 2:
        print("Usage: nexus_tasks.py <subcommand> [args]", file=sys.stderr)
        print("Subcommands: active-tasks, project-summary, search <query>", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "active-tasks":
        result = active_tasks()
    elif cmd == "project-summary":
        result = project_summary()
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: nexus_tasks.py search <query>", file=sys.stderr)
            sys.exit(1)
        result = search(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, default=str, indent=2))


if __name__ == "__main__":
    main()
