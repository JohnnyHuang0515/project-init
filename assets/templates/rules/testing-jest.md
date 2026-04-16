# Testing ({{TEST_FRAMEWORK}})

How we test in this project using {{TEST_FRAMEWORK}}. Claude should read this before writing or modifying tests.

## Commands

- **Run all tests:** `npm test`
- **Watch mode:** `npm test -- --watch`
- **One file:** `npm test -- path/to/file.test.ts`
- **With coverage:** `npm test -- --coverage`
- **Update snapshots:** `npm test -- -u` (only after confirming the change is intended)

## Layout

- Co-locate tests with source: `foo.ts` → `foo.test.ts` in the same directory.
- Shared test utilities in `test/helpers/` or similar.
- Avoid a separate top-level `__tests__/` directory unless the project already uses one.

## Structure

Use `describe` blocks to group, `it` (or `test`) for cases. Nesting beyond two levels is a smell.

```ts
describe("Cart", () => {
  describe("total", () => {
    it("returns zero for empty cart", () => { /* ... */ });
    it("sums line items", () => { /* ... */ });
    it("applies discounts after tax", () => { /* ... */ });
  });
});
```

## Naming

- Test names are sentences: `it("returns zero for empty cart")`, not `it("test empty")`.
- File names: `foo.test.ts` for unit, `foo.integration.test.ts` for integration.

## Matchers

- Use the most specific matcher available: `toEqual` for deep equality, `toBe` for reference/primitive, `toMatchObject` for partial match.
- For async: `await expect(promise).resolves.toEqual(...)` or `.rejects.toThrow(...)`.
- Error message assertions should use `toThrow("specific message")` or a regex — not just `toThrow()`.

## Snapshots

- Use snapshots sparingly. They're great for stable serialized output, terrible for UI components that change often.
- Inline snapshots (`toMatchInlineSnapshot`) are easier to review than external files.
- When a snapshot changes, read the diff — don't blindly `-u`.

## Mocking

- Prefer dependency injection over `jest.mock`/`vi.mock` when possible.
- When you must mock a module, mock at the module boundary, not individual functions.
- Always restore mocks: `afterEach(() => vi.restoreAllMocks())` or use `mockReset` config.

## React Testing (if applicable)

- Use `@testing-library/react`. Query by accessible role/name first, `data-testid` last.
- Test behaviour, not implementation — assert what the user sees, not which component rendered.
- For user events, use `userEvent` (from `@testing-library/user-event`), not `fireEvent`.

## What not to do

- Don't commit `.only` / `.skip` / `fdescribe` / `xit`.
- Don't mock what you're trying to test.
- Don't write tests that pass regardless of production code — sanity-check by breaking the code and confirming the test fails.
- Don't let the suite get slow; split integration tests so the default run stays fast.
