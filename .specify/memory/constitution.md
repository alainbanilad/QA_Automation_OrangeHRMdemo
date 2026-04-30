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

## Governance

This constitution defines the minimum automated testing standard for this repository. All pull requests and reviews MUST check compliance. Exceptions require written justification in the pull request.

**Version**: 1.0.0 | **Ratified**: 2026-04-30 | **Last Amended**: 2026-04-30
