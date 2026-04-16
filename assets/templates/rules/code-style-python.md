# Code style (Python)

Conventions for writing Python in this project. Claude should read this before editing `.py` files.

## General principles

- **Readability over cleverness.** PEP 20 ("The Zen of Python") is the tie-breaker.
- **Match the neighbours.** Consistency with existing files beats personal preference.
- **Type hints everywhere public.** All function signatures on public APIs must have type hints. Internal helpers may skip them if the types are obvious.

## Naming

- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private: prefix with single underscore (`_internal`)
- Files and modules: `snake_case.py`

## Formatting

- Formatter: **ruff format** (configured in `pyproject.toml`)
- Linter: **ruff check**
- Line length: 100 characters
- Indent: 4 spaces

Run `ruff format . && ruff check --fix .` before committing.

## Imports

Group imports in this order, separated by blank lines:
1. Standard library
2. Third-party packages
3. Local imports (this project)

Sort alphabetically within each group. Prefer absolute imports over relative.

## Typing

- Use built-in generics: `list[str]`, `dict[str, int]` — not `List`, `Dict`.
- Use `|` for unions: `str | None` — not `Optional[str]` or `Union[str, None]`.
- Use `typing.Protocol` for structural typing; avoid `ABC` unless inheritance is genuinely needed.

## Errors

- Raise specific exception types. Never `raise Exception(...)`.
- Define custom exceptions in `{{PROJECT_NAME}}/errors.py` (or similar).
- Use `raise ... from e` to preserve the cause when re-raising.

## Docstrings

- Use Google-style docstrings for public functions/classes.
- Skip docstrings on obvious helpers.
- The first line is a one-sentence summary in imperative mood ("Return the ...", not "Returns the ...").

## What not to do

- Don't use `print()` for logging. Use the `logging` module.
- Don't use bare `except:` — always specify the exception type.
- Don't add a dependency without asking.
- Don't commit code that `ruff check` rejects.
