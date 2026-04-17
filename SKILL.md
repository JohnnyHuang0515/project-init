---
name: project-init
description: Scaffold a complete .claude/ folder structure for a Claude Code project, including CLAUDE.md (team instructions), CLAUDE.local.md (personal overrides), rules/ (modular conventions like code-style, testing, API rules), skills/ (auto-invoked workflows), and agents/ (specialized sub-agents). Use this skill whenever the user wants to set up, initialize, bootstrap, or scaffold a Claude Code project; whenever they mention configuring CLAUDE.md, .claude folder, project rules, sub-agents, or a "anatomy of .claude" template; or whenever they're starting a new codebase and want Claude Code to know about it. Also use when migrating an existing project to use Claude Code conventions.
---

# Project Init

Scaffolds a production-ready `.claude/` folder for a Claude Code project, using `scripts/scaffold.py` to do the mechanical work. Your job is to interview the user, build a config, and run the script. **Don't** try to read templates and replace placeholders yourself — the script does that deterministically and verifies the result.

## Workflow

### 1. Interview the user

Keep it tight. Required info:

- **Project name** (short identifier, used in CLAUDE.md)
- **One-line description** (what the project does)
- **Stack** — e.g. "Python 3.12 + FastAPI + PostgreSQL". Determines the code-style and testing templates. Supported specialized templates:
  - Languages: `python`, `typescript`, `javascript`, `go` (others → generic)
  - Test frameworks: `pytest`, `jest`, `vitest`, `mocha` (others → generic)
- **Commands** — install, test, lint, dev server
- **Entry point** — main file path
- **Target directory** — default: current working directory

Optional:
- **Deploy target** — e.g. "Fly.io", "Vercel". Omit to skip the deploy skill.
- **Agents** — default: all four (`planner`, `implementer`, `reviewer`, `researcher`). Valid names are only these four; don't invent new ones.
- **gitignore_plans** — whether to gitignore `PLAN.md` / `FIX_PLAN.md` (default: true).

Use `ask_user_input_v0` if available (mobile-friendly). Otherwise ask in prose. **Don't interrogate** — skip anything the user already told you.

### 2. Build the config JSON

Write a config file to `/tmp/project-init-config.json` (or similar) with this shape:

```json
{
  "project_name": "orderflow",
  "project_description": "Internal order management API",
  "stack": "Python 3.12 + FastAPI + PostgreSQL",
  "languages": ["python"],
  "test_frameworks": ["pytest"],
  "entry_point": "src/orderflow/main.py",
  "install_cmd": "uv sync",
  "test_cmd": "pytest",
  "lint_cmd": "ruff check .",
  "dev_cmd": "uvicorn src.orderflow.main:app --reload",
  "deploy_target": "Fly.io",
  "agents": ["planner", "implementer", "reviewer", "researcher"],
  "gitignore_plans": true
}
```

For multi-language projects (e.g. Node backend + Python ML):
```json
{
  "languages": ["typescript", "python"],
  "test_frameworks": ["jest", "pytest"]
}
```
The script will produce one `code-style-{lang}.md` and one `testing-{framework}.md` per entry.

Required fields: everything except `deploy_target`, `agents`, `gitignore_plans`.
Backward compat: `"language"` (string) and `"test_framework"` (string) still work.

### 3. Run the scaffold script

```bash
python3 <skill-path>/scripts/scaffold.py \
    --config /tmp/project-init-config.json \
    --target <user's target dir>
```

Pass `--dry-run` first if you're unsure about the target, then again without it to actually write.

If the target directory already contains `CLAUDE.md`, `.claude/`, or `CLAUDE.local.md`, the script errors out. Either delete those first (after asking the user), or use `--force` (only after explicit user confirmation).

### 4. Report

After the script succeeds, give the user a brief summary:

- List what was created (the script's stderr output already shows this — don't duplicate at length).
- Point them at `CLAUDE.md` — specifically the project overview section at the top, which the template leaves as a TODO.
- Mention the two git steps:
  1. `git add CLAUDE.md .claude/ .gitignore && git commit` (team-shared config)
  2. `CLAUDE.local.md` stays local (already gitignored)

Keep the summary short. The user can read the files.

## What the script does (for reference, not your job)

The script reads templates from `assets/templates/`, substitutes `{{PLACEHOLDER}}` markers, writes to the target, and validates that no placeholders remain. If something goes wrong, it exits non-zero and tells you what. You don't need to re-do its work — just run it.

## When the script fails

- **"Existing Claude files detected"** → the script found files it would overwrite (e.g., a previous scaffold's `CLAUDE.md`, or existing `.claude/agents/`). Note: `.claude/settings.local.json` does NOT trigger this — it belongs to Claude Code and is left alone. Ask the user whether to overwrite; if yes, add `--force`.
- **"Template not found"** → the skill is broken; tell the user to reinstall.
- **"VALIDATION FAILED — unreplaced placeholders"** → rare; report the specific placeholders to the user and ask what they should be (the script will have written files with the raw `{{FOO}}` still in them).
- **"Config missing required fields"** → you forgot a field; fix the JSON and retry.

**Important:** if the script fails for any reason, do NOT fall back to manually creating files one by one — that defeats the purpose. Fix the actual problem and rerun the script.

## References

- `references/anatomy.md` — deeper explanation of the `.claude/` folder structure, read if the user asks what each piece is for.
- `references/examples.md` — worked examples of good CLAUDE.md and rules content for different stacks.
