---
name: automating-sei-workflows
description: >
  Automate SEI browser workflows — tag processes, extract PDFs,
  summarize with AI, export data. Use when: "tag SEI processes",
  "extract PDF from SEI", "summarize process", "export SEI data".
disable-model-invocation: true
---

# SEI Automation

Playwright-based automation for SEI (Sistema Eletrônico de Informações).

## Setup

- Credentials: `.env` in skill directory
- All scripts: `nix-shell .claude/skills/automating-sei-workflows/shell.nix --run "python .claude/skills/automating-sei-workflows/scripts/sei.py <cmd> <args>"`

## Guiding Principles

- **Automate the boring parts.** Manual clicking in SEI is the enemy.
- **Fail loudly.** If a page changes or login expires, error clearly — don't silently skip.
- **One process at a time by default.** Bulk operations require explicit confirmation.

## Workflows

- **Tag processes** → `workflows/tag-processes.md`
- **Extract PDF** → `workflows/extract-pdf.md`
- **Summarize process** → `workflows/summarize.md`
