# Test Suite Notes

## Naming Guidance

- Use behavior-first names, for example `test_login_fails_with_invalid_credentials`.
- Keep one user-observable outcome per test.
- Prefer scenario grouping by feature file (for example, OrangeHRM auth in `tests/test_orangehrm_login.py`).

## Marker Guidance

- `@pytest.mark.smoke`: critical checks required for CI gate.
- `@pytest.mark.orangehrm`: OrangeHRM-specific coverage.

## Recommended Commands

- Run all OrangeHRM auth scenarios:
  - `pytest tests/test_orangehrm_login.py`
- Run smoke-only OrangeHRM scenarios:
  - `pytest -m "smoke and orangehrm"`
