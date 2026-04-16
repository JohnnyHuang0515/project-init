# Code style

Conventions for writing code in this project. Claude should read this before editing source files.

## General principles

- **Readability over cleverness.** If a clear solution is 10% slower, take the clear one unless a benchmark proves it matters.
- **Match the neighbours.** Before introducing a new pattern, look at nearby files. Consistency beats personal preference.
- **Small functions.** Aim for functions that fit on one screen. If a function needs a table of contents in its comments, it's too long.

## Language: {{LANGUAGE}}

<!-- TODO: Fill in language-specific conventions. Examples below — delete whatever doesn't apply. -->

### Naming
- Functions: {{FUNCTION_NAMING}}
- Types/classes: {{TYPE_NAMING}}
- Constants: {{CONSTANT_NAMING}}
- Files: {{FILE_NAMING}}

### Formatting
- Formatter: {{FORMATTER}}
- Line length: {{LINE_LENGTH}}
- Indent: {{INDENT}}

### Imports
<!-- e.g. "Group imports: stdlib, third-party, local. Separate groups with a blank line. Sort alphabetically within groups." -->

## Comments

- Explain *why*, not *what*. The code shows what; comments explain intent and trade-offs.
- Delete commented-out code. Git remembers it.
- TODO comments should include a name or ticket: `# TODO(alice): handle the empty-list case`.

## Error handling

<!-- TODO: Describe the error-handling pattern. Examples:
- "Raise specific exception types, never bare `Exception`."
- "All errors crossing a service boundary must be structured with an error code and human-readable message."
- "Log errors at the boundary where they're handled, not where they're raised."
-->

## What not to do

- Don't introduce a new dependency without asking.
- Don't refactor code outside the scope of the current task.
- Don't use abbreviations that aren't already in the codebase.
