# Code style (TypeScript)

Conventions for writing TypeScript in this project. Claude should read this before editing `.ts` / `.tsx` files.

## General principles

- **Readability over cleverness.** If a clear solution is 10% slower, take the clear one.
- **Match the neighbours.** Look at adjacent files before introducing a new pattern.
- **Strict typing.** `strict: true` in tsconfig. No `any` without an inline comment explaining why.

## Naming

- Functions and variables: `camelCase`
- Types, interfaces, classes, enums: `PascalCase`
- Constants (module-level, truly constant): `UPPER_SNAKE_CASE`
- React components: `PascalCase.tsx`
- Other files: `kebab-case.ts` (unless the project already uses `camelCase` — match existing)

## Formatting

- Formatter: **prettier** (config in `.prettierrc`)
- Linter: **eslint** (config in `.eslintrc` or `eslint.config.js`)
- Line length: 100 characters
- Indent: 2 spaces
- Semicolons: yes
- Quotes: single

Run `npm run format && npm run lint` before committing.

## Types vs interfaces

- Use `type` for unions, intersections, and shape aliases.
- Use `interface` for object shapes meant to be extended or implemented by classes.
- When in doubt, use `type`.

## Imports

- Use named exports — avoid default exports except for React components and pages.
- Group imports: external packages first, then internal (`@/` or relative), then type-only imports.
- Use `import type { ... }` for type-only imports.

## Error handling

- Don't throw strings — throw `Error` subclasses.
- At module boundaries, return `Result<T, E>` or similar tagged unions rather than throwing, unless the existing code uses exceptions.
- Never swallow errors silently. At minimum, log them.

## Async

- Prefer `async/await` over `.then()` chains.
- Always `await` promises or explicitly handle them — no floating promises.
- Use `Promise.all` for concurrent independent work; `Promise.allSettled` when failures shouldn't cascade.

## React (if applicable)

- Function components only. No class components.
- One component per file for non-trivial components.
- Hooks at the top of the function, in dependency order.
- Co-locate styles, tests, and stories with the component.

## What not to do

- Don't use `any`. Use `unknown` and narrow.
- Don't use `// @ts-ignore`. Use `// @ts-expect-error` with a comment explaining why.
- Don't add a dependency without asking.
- Don't commit code that `tsc --noEmit` rejects.
