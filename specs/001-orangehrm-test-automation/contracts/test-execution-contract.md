# Contract: OrangeHRM Test Execution

## Purpose

Define the observable contract for running critical OrangeHRM automated tests in local and CI environments.

## Execution Entry Points

- Local full run: `pytest`
- Local smoke run: `pytest -m smoke`
- Targeted OrangeHRM login run: `pytest tests/test_orangehrm_login.py`

## Required Inputs

- `ORANGEHRM_BASE_URL`: Base URL for OrangeHRM Demo.
- `ORANGEHRM_USERNAME`: Valid username for successful login scenario.
- `ORANGEHRM_PASSWORD`: Valid password for successful login scenario.
- `ORANGEHRM_INVALID_PASSWORD` (or equivalent invalid credential input): Used to validate login rejection.

## Behavioral Guarantees

1. Critical flow checks MUST include:
   - successful login
   - failed login with invalid credentials
   - logout
2. Tests MUST be independently runnable.
3. Failing UI tests MUST capture screenshot evidence.
4. Authentication secrets MUST NOT be embedded in test source files.

## Output Contract

- Process exit code:
  - `0` when selected tests pass.
  - non-zero when any selected test fails or setup is invalid.
- Console output:
  - per-test pass/fail outcome
  - failure details with assertion context
- Artifacts:
  - screenshot for each failed critical-flow UI test (path reported in output/log)
  - default screenshot location pattern: `artifacts/screenshots/<pytest-nodeid>.png`

## Failure Evidence Example

- Expected pytest report section includes a line similar to:
  - `Saved screenshot: artifacts/screenshots/tests_test_orangehrm_login.py__test_login_success_with_valid_credentials.png`

## Non-Goals

- This contract does not define OrangeHRM application API behavior.
- This contract does not enforce browser matrix beyond configured project defaults.