# Examples

Short, realistic examples of what filled-in files look like for different stacks. Use as inspiration when customizing templates.

## Example 1: Python FastAPI project

**CLAUDE.md excerpt:**

```markdown
# Orderflow

Internal order-management API for the logistics team. Replaces the legacy Rails app (`orderflow-v1`, read-only, to be sunset Q3).

## Project overview

**Stack:** Python 3.12 + FastAPI + PostgreSQL + SQLAlchemy 2.0
**Test framework:** pytest
**Entry point:** `src/orderflow/main.py`

Orderflow handles ~40k orders/day. It's read-heavy (~10:1 read:write) and
latency-sensitive for warehouse staff using the mobile app.

## Development workflow

**Install:** `uv sync`
**Run tests:** `pytest`
**Run linter:** `ruff check . && mypy src`
**Start dev server:** `uvicorn src.orderflow.main:app --reload`
```

## Example 2: Next.js + TypeScript project

**rules/code-style.md excerpt:**

```markdown
### Server vs client components

- Default to **server components**. Only add `"use client"` when you need
  state, effects, or browser APIs.
- Keep the client boundary as deep in the tree as possible.
- Data fetching happens in server components; client components receive
  data as props.

### State management

- Local UI state: `useState` / `useReducer`.
- Server state: `@tanstack/react-query`.
- URL state: `useSearchParams` / `usePathname`.
- We don't use Redux, Zustand, or Jotai in this project. If you think
  you need one, raise it with the team first.
```

## Example 3: agents/code-reviewer.md tailored for a startup

```markdown
---
name: code-reviewer
description: Reviews diffs. Biased toward shipping — flags blockers, notes nits, lets style wars go.
---

# Code Reviewer

Startup context: we ship daily, we fix in prod, we iterate. Your job is to
catch the things that will bite us, not to enforce ideology.

## Priorities (in order)

1. Security — missed auth check, injectable query, leaked secret.
2. Data loss — unmigrated schema, untested delete, forgotten transaction.
3. User-visible bugs — wrong logic, broken edge case.
4. Maintainability — if the next person will hate this, say so.
5. Style — only if it's jarring or makes the code hard to read.

Don't block on preferences. Don't rewrite the code. Point out the thing,
suggest a fix, move on.
```

## What makes these examples good

- **Specific, not generic.** "pytest", not "testing framework". "SQLAlchemy 2.0", not "ORM".
- **Opinionated.** "We don't use Redux" is more useful than "choose a state manager".
- **Honest about constraints.** "We ship daily, we fix in prod" sets realistic review expectations.
- **Actionable.** Every rule tells Claude what to do differently, not just describes the world.

## What makes bad examples

- "Write clean, readable code." — Meaningless. Everyone agrees with this; it tells Claude nothing.
- "Follow best practices." — Which ones? Whose? In what context?
- "Use descriptive names." — Fine, but what's the convention? camelCase? snake_case? How long is too long?

When writing rules, if a human skimming them wouldn't learn anything new about this specific project, the rule isn't pulling its weight.
