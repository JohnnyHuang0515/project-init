# Code style (Go)

Conventions for writing Go in this project. Claude should read this before editing `.go` files.

## General principles

- **Idiomatic Go wins.** Follow [Effective Go](https://go.dev/doc/effective_go) and the [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments). When in doubt, match the standard library.
- **Accept interfaces, return structs.**
- **Errors are values.** Handle them explicitly; don't rely on panics for flow control.

## Naming

- Exported identifiers: `PascalCase`
- Unexported: `camelCase`
- Acronyms stay consistent-case: `URL`, `ID`, `HTTP` (exported); `url`, `id` (unexported).
- Package names: short, lowercase, no underscores. Singular.
- Files: `snake_case.go`. Test files: `foo_test.go`.

## Formatting

- Formatter: **gofmt** (enforced — no exceptions).
- Additional: **goimports** for import ordering.
- Linter: **golangci-lint** with the project's `.golangci.yml`.

Run `gofmt -w . && goimports -w . && golangci-lint run` before committing.

## Errors

- Return errors as the last return value.
- Wrap with context: `fmt.Errorf("doing X: %w", err)`.
- Define sentinel errors at package level: `var ErrNotFound = errors.New("not found")`.
- Use `errors.Is` and `errors.As` for inspection — don't compare error strings.

## Context

- `context.Context` is always the first parameter.
- Never store a context in a struct. Pass it explicitly.
- Respect cancellation in long-running operations.

## Concurrency

- Use channels for communication, mutexes for state.
- Every goroutine must have a clear lifecycle — no fire-and-forget without a reason.
- Use `errgroup.Group` when you need to fan out and collect errors.

## Testing

- Use table-driven tests where there are multiple similar cases.
- Test files live next to the code they test.
- Use `t.Helper()` in assertion helpers.

## What not to do

- Don't use `init()` functions unless absolutely necessary.
- Don't use `panic` for expected errors — panics are for programmer mistakes.
- Don't ignore errors with `_`. If you're ignoring one, explain why in a comment.
- Don't add a dependency without asking.
