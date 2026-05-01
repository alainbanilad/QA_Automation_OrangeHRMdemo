# OrangeHRM Demo Test Constitution

## Core Principles

### I. Critical Flow Coverage
Automated tests MUST cover, at minimum:
- Successful login.
- Failed login with invalid credentials.
- Successful logout.

### II. Test Independence
Each test MUST be runnable alone and MUST NOT depend on test order or shared state from previous tests.

### III. Stable and Readable Locators
Tests MUST prefer stable selectors such as `id`, `name`, or dedicated attributes; fragile absolute XPath selectors SHOULD be avoided.

### IV. Reliable Synchronization
Tests MUST use explicit waits/assertions for UI state changes; fixed sleep calls SHOULD NOT be used unless no better option exists.

### V. Failure Evidence
On failure, the framework MUST capture enough evidence to debug quickly, including error message and screenshot.

## Minimum Technical Constraints

- Target scope is the OrangeHRM Demo web UI only.
- Base URL and credentials MUST come from configuration or environment variables.
- Secrets MUST NOT be hardcoded in test files.
- The minimum CI gate is one smoke test run for login flow.

## Workflow and Quality Gates

- Any change to login-related page behavior MUST include test updates when relevant.
- Pull requests MUST pass the configured automated smoke tests before merge.
- Flaky tests MUST be fixed or temporarily quarantined with a tracking item.

## Minimum CI/CD QA Pipeline Requirements

- CI MUST trigger on every pull request and on pushes to the default branch.
- The pipeline MUST install project dependencies from `requirements.txt` in a clean environment.
- The pipeline MUST run at least the OrangeHRM smoke suite (valid login, invalid login, logout).
- A test failure MUST fail the pipeline job and block merge until resolved or explicitly exempted.
- The pipeline MUST publish test artifacts for failed runs, at minimum: pytest output and screenshots (and Allure results when available).
- Secrets used by tests (for example credentials) MUST be provided by CI secret storage and MUST NOT be hardcoded.
- The default-branch pipeline SHOULD execute the full regression suite at least once daily.

## Governance

This constitution defines the minimum automated testing standard for this repository. All pull requests and reviews MUST check compliance. Exceptions require written justification in the pull request.

**Version**: 1.1.0 | **Ratified**: 2026-04-30 | **Last Amended**: 2026-05-01
