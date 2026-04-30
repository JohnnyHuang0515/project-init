# TDD standards

Rules for writing tests before implementation. Read alongside `.claude/rules/testing.md`.

- **tester** follows these rules when writing tests from a plan.
- **implementer** follows these rules when tester's tests are missing and must write their own.
- **reviewer** uses these as the standard for judging test quality.

---

## Test structure

Every test must follow AAA — use comments to separate the three phases:

```python
def test_expired_token_returns_401():
    # Arrange
    token = create_token(expires_at=one_hour_ago())
    client = AuthClient(token)

    # Act
    response = client.get("/profile")

    # Assert
    assert response.status_code == 401
```

---

## Test case coverage

For every behaviour in the plan, cover:

- **Happy path** — valid input produces the expected output
- **Boundaries** — empty, zero, max, off-by-one around any limit
- **Error paths** — invalid input returns the right error (not a crash)
- **Regression (bug fixes only)** — one test named `test_regression_<description>` that reproduces the exact reported symptom

---

## Mock rules

Mock external dependencies only. Never mock the code under test.

**Mock these:**
- Databases — at the repository/DAO boundary
- HTTP clients — at the client call (`requests.get`, `fetch`)
- Time — `datetime.now()`, `Date.now()`, `time.time()`
- External services — email, SMS, payment, third-party APIs
- Filesystems — unless the test is specifically about file I/O

**Never mock:**
- The code under test
- Pure functions
- Simple data/value objects
- Your own domain logic

**Mock at the boundary, not inside it:**
```python
# Wrong
mock(UserService._hash_password)

# Right
mock(bcrypt.hashpw)
```

---

## Query vs Command

- **Query** (returns a value) → assert the return value
- **Command** (causes a side effect) → assert the interaction at the boundary

```python
# Query — assert return value
assert user_service.find(42).email == "alice@example.com"

# Command — assert the boundary was called correctly
mailer.send.assert_called_once_with(to="alice@example.com", subject="Welcome")
```

Do not verify interactions for queries. Do not skip interaction verification for commands.

---

## Database tests

For code with real query logic, use an in-memory database (SQLite `:memory:`, H2, `pg_tmp`) — not a mock repository. Mocking the DB layer hides SQL errors and schema mismatches.

Mock the DB only when the test is about business logic that happens to call a repository, not about the data access itself.

---

## Design for testability

- **Dependency injection** — always write tests assuming dependencies are injected via constructor or arguments, not instantiated inside the class. `implementer` must accept injected instances; never instantiate external dependencies (DB connections, API clients) directly inside a class.
- **Test data minimalism** — only include fields relevant to the current assertion. Use a factory or fixture for the rest. Override only what the test cares about.
- **Explicit assertions** — assert specific attributes, not whole objects: `assert user.email == "alice@example.com"`, not `assert user == expected_user`.

---

## Async rules

- Never use `time.sleep()` or `await delay()` to wait for async results.
- Use polling/retry patterns or await the promise/future directly.
- All async tests must have an explicit timeout — default maximum 5 seconds.
- Use the correct async decorator (`@pytest.mark.asyncio`, `async () => {}` in Jest, etc.).

---

## Environment and cleanup

- Tests must not depend on external environment variables. Use `mock.patch.dict` or equivalent to set env vars per test.
- All env var changes must be restored in teardown.
- All filesystem writes must go to the OS temp directory and be deleted after the test.

---

## Test quality rules

- One logical assertion per test — if asserting 5 things, write 5 tests
- Name describes behaviour: `test_expired_token_returns_401`, not `test_auth_check_3`
- No shared mutable state — each test sets up its own fixtures
- Idempotent — running 10 times gives the same result
- Avoid hardcoded setup over 10 lines — use a factory or `conftest.py` fixture instead

---

## Contract alignment

- Tests must strictly follow the function signatures and types defined in the plan. Do not invent or change interfaces.
- If the plan says `getUser(id: string)`, the test must not call `getUser(id: number)`.
- If a signature is ambiguous in the plan, use the most idiomatic interpretation and document the assumption in the red state report.

---

## Non-determinism

Any logic involving randomness, ordering, or unique IDs must be stabilised:

- **Randomness** — mock the random generator or use a fixed seed
- **UUIDs** — mock UUID generators to return predictable values if the ID appears in the assertion
- **Unordered collections** — assert on sorted lists or use set-based comparison; never assert order unless the code explicitly sorts

---

## Red state requirement

Before handing off to implementer, every new test must be confirmed to fail. State the expected failure for each test:

```
test_create_user_returns_201 — will raise AttributeError: module has no attribute 'create_user'
test_invalid_email_returns_422 — will raise AssertionError: 200 != 422
```

Target **strong failure** (logic mismatch), not weak failure (file not found):

- **Weak** — `ImportError: cannot import name 'create_user'` — only proves the file is missing
- **Strong** — `AssertionError: 404 != 201` — proves the logic is wrong

To achieve strong failure, create a minimal stub of the class or function first (returns `None` or raises `NotImplementedError`), then confirm the test fails on the assertion, not the import.

A test that might already pass before implementation is a broken test.

---

## What not to do

- `assert result is not None` — catches nothing
- `assert response.status_code == 200` without checking the body
- Verifying a mock was called for a query
- One test with many unrelated assertions
- Leaving `.only`, `.skip`, `fdescribe`, `xit` committed
- Tests that pass regardless of production code
- `time.sleep()` or fixed delays in async tests
- No teardown after DB writes, file writes, or env var changes
- Instantiating external dependencies directly inside the class under test
