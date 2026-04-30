# Quickstart: OrangeHRM Test Automation Foundation

## 1. Prepare Environment

1. Ensure Python and project dependencies are installed.
2. Copy `.env.example` values into your shell or CI secret store.
3. Configure required environment variables:
   - `ORANGEHRM_BASE_URL`
   - `ORANGEHRM_USERNAME`
   - `ORANGEHRM_PASSWORD`
   - `ORANGEHRM_INVALID_PASSWORD`

## 2. Run Critical Flows Locally

1. Run OrangeHRM auth tests:
   - `pytest tests/test_orangehrm_login.py`
2. Run smoke subset:
   - `pytest -m "smoke and orangehrm"`
3. Run only invalid and blank-login negative scenarios:
   - `pytest tests/test_orangehrm_login.py -k "invalid or blank"`
4. Run logout coverage only:
   - `pytest tests/test_orangehrm_login.py -k "logout"`

## 3. Expected Results

1. Successful login test passes with valid credentials.
2. Invalid login test passes by confirming access denial and error visibility.
3. Logout test passes by confirming session invalidation and login requirement.

## 4. Failure Evidence

1. On failure, inspect pytest output for failure context.
2. Open generated screenshot artifacts for UI-state diagnosis.

## 5. CI Gate Expectation

1. Pull requests must pass smoke authentication checks before merge.
2. Flaky tests must be fixed or quarantined with a tracked follow-up item.

## 6. Validation Log

- Date: 2026-04-30
- Command: `pytest tests/test_orangehrm_login.py`
- Result: passed (5 passed in 51.61s)
- Command: `pytest -m "smoke and orangehrm"`
- Result: passed (3 passed, 4 deselected in 27.91s)
