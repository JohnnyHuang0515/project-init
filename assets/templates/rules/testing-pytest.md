# Testing (pytest)

How we test in this project using pytest. Claude should read this before writing or modifying tests.

## Commands

- **Run all tests:** `pytest`
- **Run one file:** `pytest tests/test_foo.py`
- **Run one test:** `pytest tests/test_foo.py::test_bar`
- **With coverage:** `pytest --cov={{PROJECT_NAME}} --cov-report=term-missing`
- **With output:** `pytest -s` (to see print statements)
- **Stop on first failure:** `pytest -x`

## Layout

- Tests live in `tests/`, mirroring the source tree: `src/foo/bar.py` → `tests/foo/test_bar.py`.
- One `test_*.py` file per source file, usually.
- Shared fixtures go in `conftest.py` — at the level they're needed, not all at the root.

## Naming

- Files: `test_*.py`
- Functions: `test_*`
- Classes (if used): `Test*` — but prefer plain functions unless grouping helps.
- Test names describe the behaviour: `test_empty_cart_returns_zero_total`, not `test_get_total`.

## Fixtures

- Use `@pytest.fixture` for setup/teardown.
- Scope appropriately: `function` (default) for most, `module` or `session` only when setup is genuinely expensive.
- Name fixtures by what they *are*, not what they *do*: `user`, not `create_user`.

## Parametrize

Use `@pytest.mark.parametrize` for table-driven tests:

```python
@pytest.mark.parametrize("input,expected", [
    ("",        0),
    ("a",       1),
    ("hello",   5),
])
def test_length(input, expected):
    assert len(input) == expected
```

## Assertions

- Use plain `assert` — pytest's assertion introspection will show you useful output.
- For exceptions: `with pytest.raises(ValueError, match="specific message")`.
- For approximate numeric comparisons: `pytest.approx`.

## Mocking

- Use `pytest-mock`'s `mocker` fixture (preferred) or `unittest.mock.patch`.
- Mock at the boundary, not in the middle of your code.
- Prefer fake implementations over MagicMock when the interface is small.

## Markers

Project-specific markers (register in `pyproject.toml` or `pytest.ini`):
- `@pytest.mark.slow` — takes > 1 second; skip in fast runs with `-m "not slow"`.
- `@pytest.mark.integration` — hits real external services.

## What not to do

- Don't use `unittest.TestCase` — use plain functions unless there's a specific reason.
- Don't commit `.skip` / `pytest.skip()` without a linked issue.
- Don't let test execution time creep up; mark slow tests and keep the default suite fast.
- Don't share mutable state between tests via module-level variables.
