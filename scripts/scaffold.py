#!/usr/bin/env python3
"""
Scaffold a Claude Code project structure from a config JSON.

Usage:
    python scaffold.py --config config.json [--target .] [--dry-run]

The config JSON should have the shape shown in the example below.
Example config (single language):
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

Example config (multi-language: Node backend + Python ML):
    {
        "project_name": "myapp",
        "project_description": "Node API with Python ML service",
        "stack": "Node.js + Express + Python + FastAPI",
        "languages": ["typescript", "python"],
        "test_frameworks": ["jest", "pytest"],
        "entry_point": "src/index.ts",
        "install_cmd": "npm install && uv sync",
        "test_cmd": "npm test && pytest",
        "lint_cmd": "eslint . && ruff check .",
        "dev_cmd": "npm run dev"
    }

All fields are required except:
    - deploy_target (optional; omit to skip the deploy skill)
    - agents (defaults to all four)
    - gitignore_plans (defaults to true)

Backward compat: "language" (string) and "test_framework" (string) still work,
and are automatically converted to single-element lists.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

# Map language -> code-style template filename.
LANG_TEMPLATES = {
    "python": "code-style-python.md",
    "typescript": "code-style-typescript.md",
    "javascript": "code-style-typescript.md",  # close enough
    "go": "code-style-go.md",
}

# Map test framework -> testing template filename.
TEST_TEMPLATES = {
    "pytest": "testing-pytest.md",
    "jest": "testing-jest.md",
    "vitest": "testing-jest.md",
    "mocha": "testing-jest.md",
}

DEFAULT_AGENTS = ["planner", "implementer", "reviewer", "researcher"]

GITIGNORE_CLAUDE_BLOCK = """\
# Claude Code personal overrides
CLAUDE.local.md
.claude/settings.local.json
"""

GITIGNORE_PLANS_BLOCK = """\
# Working documents from agent pipeline
PLAN.md
FIX_PLAN.md
"""


def log(msg: str, level: str = "info") -> None:
    """Simple colored logger."""
    prefix = {
        "info": "  ",
        "ok": "✓ ",
        "warn": "⚠ ",
        "err": "✗ ",
        "step": "▸ ",
    }.get(level, "  ")
    print(f"{prefix}{msg}", file=sys.stderr)


def load_config(path: Path) -> dict:
    """Load and lightly validate the config JSON."""
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    with path.open() as f:
        cfg = json.load(f)

    # Backward compat: "language"/"test_framework" (strings) → lists.
    if "language" in cfg and "languages" not in cfg:
        cfg["languages"] = [cfg.pop("language")]
    if "test_framework" in cfg and "test_frameworks" not in cfg:
        cfg["test_frameworks"] = [cfg.pop("test_framework")]

    required = [
        "project_name", "project_description", "stack", "languages",
        "test_frameworks", "entry_point",
        "install_cmd", "test_cmd", "lint_cmd", "dev_cmd",
    ]
    missing = [k for k in required if k not in cfg or not cfg[k]]
    if missing:
        raise ValueError(f"Config missing required fields: {missing}")

    # Normalise to lowercase lists.
    cfg["languages"] = [l.lower() for l in cfg["languages"]]
    cfg["test_frameworks"] = [f.lower() for f in cfg["test_frameworks"]]

    cfg.setdefault("agents", DEFAULT_AGENTS)
    cfg.setdefault("gitignore_plans", True)
    cfg.setdefault("deploy_target", None)

    # Validate agent names.
    unknown = set(cfg["agents"]) - set(DEFAULT_AGENTS)
    if unknown:
        raise ValueError(f"Unknown agent names: {unknown}. "
                         f"Valid: {DEFAULT_AGENTS}")

    return cfg


def build_replacements(cfg: dict) -> dict:
    """Build the {{PLACEHOLDER}} -> value mapping."""
    deploy_target = cfg.get("deploy_target")
    languages = cfg["languages"]
    primary_lang = languages[0]  # 用第一個語言決定 indent 等風格

    return {
        "PROJECT_NAME": cfg["project_name"],
        "PROJECT_DESCRIPTION": cfg["project_description"],
        "STACK": cfg["stack"],
        "TEST_FRAMEWORK": ", ".join(cfg["test_frameworks"]),
        "ENTRY_POINT": cfg["entry_point"],
        "INSTALL_CMD": cfg["install_cmd"],
        "TEST_CMD": cfg["test_cmd"],
        "LINT_CMD": cfg["lint_cmd"],
        "DEV_CMD": cfg["dev_cmd"],
        "LANGUAGE": ", ".join(languages),
        "DEPLOY_TARGET": deploy_target or "",
        "BUILD_CMD": cfg.get("build_cmd", cfg["install_cmd"]),
        "DEPLOY_CMD": cfg.get("deploy_cmd", "# TODO: fill in deploy command"),
        "TEST_ONE_CMD": f"{cfg['test_cmd']} <path>",
        "COVERAGE_CMD": (
            f"{cfg['test_cmd']} --cov"
            if "pytest" in cfg["test_cmd"]
            else f"{cfg['test_cmd']} -- --coverage"
        ),
        "FUNCTION_NAMING": "see existing code",
        "TYPE_NAMING": "see existing code",
        "CONSTANT_NAMING": "see existing code",
        "FILE_NAMING": "see existing code",
        "FORMATTER": "see existing code",
        "LINE_LENGTH": "100",
        "INDENT": "4 spaces" if primary_lang == "python" else "2 spaces",
        "DEPLOY_SKILL_LINE": (
            f"- `deploy` — deployment workflow for {deploy_target}."
            if deploy_target else ""
        ),
    }


def substitute(text: str, replacements: dict) -> str:
    """Replace all {{KEY}} markers with values from replacements dict."""
    def repl(match: re.Match) -> str:
        key = match.group(1)
        return replacements.get(key, match.group(0))  # keep unknown as-is
    return re.sub(r"\{\{(\w+)\}\}", repl, text)


def find_unreplaced_placeholders(text: str) -> list[str]:
    """Return any {{FOO}} markers still present."""
    return re.findall(r"\{\{(\w+)\}\}", text)


def copy_template(
    src: Path, dst: Path, replacements: dict, dry_run: bool,
) -> list[str]:
    """Copy a template with substitution. Returns any unreplaced placeholders."""
    if not src.exists():
        raise FileNotFoundError(f"Template not found: {src}")

    text = src.read_text(encoding="utf-8")
    text = substitute(text, replacements)
    leftover = find_unreplaced_placeholders(text)

    if dry_run:
        log(f"[DRY-RUN] Would write {dst}", "info")
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8")
        log(f"Wrote {dst}", "ok")

    return leftover


def update_gitignore(
    target: Path, include_plans: bool, dry_run: bool,
) -> None:
    """Append Claude-related entries to .gitignore without duplicating."""
    gitignore = target / ".gitignore"
    existing = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    lines_to_add = []

    if "CLAUDE.local.md" not in existing:
        lines_to_add.append(GITIGNORE_CLAUDE_BLOCK)

    if include_plans and "PLAN.md" not in existing:
        lines_to_add.append(GITIGNORE_PLANS_BLOCK)

    if not lines_to_add:
        log(".gitignore already up to date", "info")
        return

    new_content = existing
    if existing and not existing.endswith("\n"):
        new_content += "\n"
    if existing:
        new_content += "\n"
    new_content += "\n".join(lines_to_add)

    if dry_run:
        log(f"[DRY-RUN] Would update {gitignore}", "info")
    else:
        gitignore.write_text(new_content, encoding="utf-8")
        log(f"Updated {gitignore}", "ok")


def check_existing_files(target: Path) -> list[Path]:
    """Return list of paths we're about to write that already exist.

    Only flags paths that THIS script produces — not other things that may
    live under .claude/ (e.g., settings.local.json, which Claude Code itself
    creates and which is unrelated to our scaffolding).
    """
    candidates = [
        target / "CLAUDE.md",
        target / "CLAUDE.local.md",
        target / ".claude" / "agents",
        target / ".claude" / "rules",
        target / ".claude" / "skills",
        target / ".claude" / "references",
    ]
    return [p for p in candidates if p.exists()]


def scaffold(
    skill_dir: Path, target: Path, cfg: dict, dry_run: bool = False,
    force: bool = False,
) -> None:
    """Main scaffolding logic."""
    log(f"Scaffolding {cfg['project_name']} at {target}", "step")

    # 1. Safety check.
    existing = check_existing_files(target)
    if existing and not force:
        log("Existing Claude files detected:", "warn")
        for p in existing:
            log(f"  - {p.relative_to(target)}", "warn")
        log("Pass --force to overwrite, or delete them first.", "err")
        raise SystemExit(2)

    templates_dir = skill_dir / "assets" / "templates"
    if not templates_dir.is_dir():
        raise FileNotFoundError(f"Templates directory missing: {templates_dir}")

    replacements = build_replacements(cfg)
    all_leftover: dict[Path, list[str]] = {}

    # 2. Copy core files.
    jobs: list[tuple[Path, Path]] = [
        (templates_dir / "CLAUDE.md", target / "CLAUDE.md"),
        (templates_dir / "CLAUDE.local.md", target / "CLAUDE.local.md"),
        (templates_dir / "rules" / "api-conventions.md",
         target / ".claude" / "rules" / "api-conventions.md"),
    ]

    # 3. Language-specific code-style — one file per language.
    for lang in cfg["languages"]:
        style_template = LANG_TEMPLATES.get(lang, "code-style-generic.md")
        # Single language → code-style.md, multi → code-style-python.md etc.
        if len(cfg["languages"]) == 1:
            dst_name = "code-style.md"
        else:
            dst_name = f"code-style-{lang}.md"
        jobs.append((
            templates_dir / "rules" / style_template,
            target / ".claude" / "rules" / dst_name,
        ))

    # 4. Framework-specific testing rules — one file per framework.
    for framework in cfg["test_frameworks"]:
        test_template = TEST_TEMPLATES.get(framework, "testing-generic.md")
        if len(cfg["test_frameworks"]) == 1:
            dst_name = "testing.md"
        else:
            dst_name = f"testing-{framework}.md"
        jobs.append((
            templates_dir / "rules" / test_template,
            target / ".claude" / "rules" / dst_name,
        ))

    # 5. Bundled skills.
    jobs.append((
        templates_dir / "skills" / "security-review.md",
        target / ".claude" / "skills" / "security-review" / "SKILL.md",
    ))
    if cfg.get("deploy_target"):
        jobs.append((
            templates_dir / "skills" / "deploy.md",
            target / ".claude" / "skills" / "deploy" / "SKILL.md",
        ))

    # 6. Agents.
    for agent_name in cfg["agents"]:
        jobs.append((
            templates_dir / "agents" / f"{agent_name}.md",
            target / ".claude" / "agents" / f"{agent_name}.md",
        ))

    # 7. References — shared docs that agents read at runtime.
    # Only copy files that agents actually need during work (not human-facing docs).
    AGENT_REFERENCES = ["plan-schema.md"]
    references_dir = skill_dir / "references"
    if references_dir.is_dir():
        for ref_name in AGENT_REFERENCES:
            ref_file = references_dir / ref_name
            if ref_file.exists():
                jobs.append((
                    ref_file,
                    target / ".claude" / "references" / ref_name,
                ))

    # 7. Execute jobs.
    for src, dst in jobs:
        leftover = copy_template(src, dst, replacements, dry_run)
        if leftover:
            all_leftover[dst] = leftover

    # 8. .gitignore update.
    update_gitignore(target, cfg["gitignore_plans"], dry_run)

    # 9. Final validation.
    if all_leftover:
        log("", "info")
        log("VALIDATION FAILED — unreplaced placeholders found:", "err")
        for path, markers in all_leftover.items():
            log(f"  {path}: {set(markers)}", "err")
        log("", "info")
        log("The files were still written, but you should review and fix these.", "warn")
        raise SystemExit(1)

    log("", "info")
    log(f"Scaffolding complete. Files written under: {target}", "ok")
    if not dry_run:
        log("Next: review CLAUDE.md (especially the Project overview section).", "info")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a Claude Code project structure.",
    )
    parser.add_argument(
        "--config", type=Path, required=True,
        help="Path to config JSON file.",
    )
    parser.add_argument(
        "--target", type=Path, default=Path("."),
        help="Target directory (default: current).",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print actions without writing files.",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Overwrite existing Claude files without asking.",
    )
    args = parser.parse_args()

    # The script expects to live at <skill>/scripts/scaffold.py
    skill_dir = Path(__file__).resolve().parent.parent

    cfg = load_config(args.config)
    scaffold(skill_dir, args.target.resolve(), cfg, args.dry_run, args.force)


if __name__ == "__main__":
    main()
