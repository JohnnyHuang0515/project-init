# Plan file schemas

This file defines the exact structure of `PLAN.md` and `FIX_PLAN.md`.

- **planner** writes these files following this schema.
- **implementer** reads them to know what to execute.
- **reviewer** reads them to understand what the change is supposed to do.

All three agents should reference this file when working with plans.

---

## PLAN.md — New feature or non-trivial change

```markdown
# Plan: <feature name>

## Status
<!-- planner sets this; human edits to approve -->
DRAFT | APPROVED | IN PROGRESS | DONE

## Context
<1–3 sentences: what this is, why we're building it, who asked.>

## Goals
- <specific, measurable outcome — not "add caching" but "reduce p95 latency on /users by 50%">

## Non-goals
- <explicit things NOT in scope — prevents scope creep during implementation>

## Approach

<1–2 paragraphs describing the solution and why this approach over alternatives.>

### Alternatives considered
- **<option A>** — rejected because <reason>
- **<option B>** — rejected because <reason>
<!-- Only include if a real choice exists. Don't fabricate alternatives. -->

## Design

### Files changed
- `path/to/new_file.py` — <what it is, key classes/functions>
- `path/to/existing.py` — <what changes and why>
<!-- List every file that will be touched. Implementer uses this as a checklist. -->

### Data model / schema
<!-- Only if the change adds/modifies DB tables, API request/response shapes, or config schemas. -->

### Public API
<!-- Only if adding or changing a public interface (HTTP endpoint, library function, CLI arg).
     Include: signature, example request, example response. -->

### Technology choices
<!-- Only if introducing a new library, framework, or pattern.
     Format: "chose X over Y because Z" — one line each. -->

## Implementation steps

<!-- Ordered. Each step should be small enough to review independently.
     Implementer executes these in order, running tests after each. -->

1. <step — be specific about what code changes> (touches: `file_a.py`)
2. <step> (touches: `file_b.py`)
3. Write tests for <what behaviour>
4. Update docs / README (if public-facing change)

## Testing strategy

- Unit tests: <what cases>
- Integration tests: <if any>
- Manual verification: <if needed>

## Risks and open questions

<!-- Things the human must decide or be aware of before approving. -->
- <risk or unanswered question>
<!-- If none: "None identified." -->

## Out-of-scope follow-ups

<!-- Things noticed during planning that aren't part of this change. Track here so they're not lost. -->
- <follow-up item>
<!-- If none: omit this section. -->
```

---

## FIX_PLAN.md — Bug fix or regression

```markdown
# Fix Plan: <short description of the bug>

## Status
<!-- planner sets this; human edits to approve -->
DRAFT | APPROVED | IN PROGRESS | DONE

## Symptoms
<Exactly what the user or test sees when the bug occurs.
 Be specific: error message, wrong output, failing test name.>

## Reproduction
<Minimal steps to trigger the bug — or "Could not reproduce" with details on what was tried.>

## Root cause

<2–4 sentences. Cite file:line. Explain WHY the code does the wrong thing for this input/state.
 This must be the actual cause, not just the symptom.>

### How it got this way
<!-- Optional: "Introduced in commit abc123 when X was refactored" -->

## Proposed fix

<The specific change. Cite file:line. Be concrete — not "handle the None case" but
 "add `if result is None: return []` before line 47 in user_service.py".>

### Scope
- `path/to/file.py` — <what changes>
<!-- List every file touched. -->

### Not fixing (out of scope)
<!-- Related issues noticed but deliberately excluded from this fix. -->
- <item>

## Regression test

<Describe the test that will be added.>
- It MUST fail on current `main` without the fix.
- It MUST pass after the fix is applied.
- Implementer should verify this manually before marking done.

Test location: `tests/path/to/test_file.py`
Test name: `test_<descriptive_name>`

## Verification checklist

- [ ] Regression test written
- [ ] Regression test fails on `main` (verified before fixing)
- [ ] Regression test passes after fix
- [ ] Existing test suite still passes
- [ ] Linter clean

## Risk

<What could break as a side effect of this fix?
 Who else calls this code? What depends on the current (buggy) behaviour?>
```

---

## Rules for all plan files

- **Status field** is how implementer knows whether to proceed. Implementer should refuse to execute a plan that isn't `APPROVED`.
- **Never leave placeholder text** like `<what changes>` in the final plan. Every field must be filled in with real content.
- **Non-goals are mandatory** for PLAN.md. The absence of a non-goals section is a signal the plan's scope hasn't been thought through.
- **File list must be complete**. If implementer encounters a file not in the list, it should pause and flag it rather than silently editing.
- **Implementation steps must be ordered and specific**. "Implement the feature" is not a step. "Add `UserCache` class to `services/cache.py` with `get(user_id)` and `invalidate(user_id)` methods" is a step.
