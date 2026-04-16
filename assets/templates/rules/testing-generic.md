# Testing

How we test in this project. Claude should read this before writing or modifying tests.

## Framework

Test framework: **{{TEST_FRAMEWORK}}**

**Run all tests:** `{{TEST_CMD}}`
**Run one file:** `{{TEST_ONE_CMD}}`
**Run with coverage:** `{{COVERAGE_CMD}}`

## What to test

- **Every bug fix gets a test.** The test should fail before the fix and pass after.
- **Public API surface.** Any function exposed to other modules needs tests covering the happy path and at least one edge case.
- **Boundaries.** Empty inputs, single-element inputs, maximum-size inputs, and whatever "weird" looks like in the domain.

## What not to test

- Implementation details. Tests should survive refactors that don't change behaviour.
- Third-party libraries. Assume they work; test your integration with them.
- Trivial getters/setters.

## Test structure

Prefer the **Arrange-Act-Assert** pattern:

```
def test_user_can_reset_password():
    # Arrange
    user = create_user(email="a@b.com")

    # Act
    token = request_password_reset(user.email)

    # Assert
    assert token is not None
    assert user.reload().reset_token == token
```

## Naming

- Test names describe behaviour, not implementation: `test_empty_cart_returns_zero_total`, not `test_get_total`.
- One logical assertion per test. Multiple `assert` statements are fine if they're checking the same outcome.

## Test data

- Use factories / builders for complex objects, not shared fixtures spread across files.
- Prefer realistic-looking data ("alice@example.com") over garbage ("asdf123") — it helps debugging.
- Keep test data close to the test that uses it.

## Mocking

- Mock at the boundary, not in the middle. If you're mocking your own internal code, the design is probably wrong.
- Prefer fakes (in-memory implementations) over mocks (verify calls) when possible.
- Never mock the thing you're testing.

## Flaky tests

If a test fails intermittently:
1. **Don't retry-loop it.** That hides the bug.
2. Investigate the actual cause — usually timing, shared state, or external dependencies.
3. If it truly can't be fixed (e.g., external service), skip it with a tracking issue.

## What not to do

- Don't write tests that pass regardless of the production code (check that they actually fail when you break the code).
- Don't commit `.skip` / `.only` / `fdescribe` / `xit`.
- Don't let test execution time balloon — split slow integration tests from fast unit tests.
