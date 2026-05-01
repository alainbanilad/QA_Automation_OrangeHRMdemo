# Jenkins QA Pipeline Contract

## Purpose

Defines the minimum contract for Jenkins-based CI/CD QA execution for OrangeHRM automation tests.

## Trigger Contract

- Pull request trigger:
  - MUST execute required smoke scope.
  - MUST publish pass/fail status back to pull request checks.
- Default branch push trigger:
  - MUST execute smoke scope at minimum.
- Scheduled trigger:
  - MUST execute full regression scope at least daily.

## Input Contract

### Required Environment Inputs

- `BASE_URL`: OrangeHRM target URL.
- `ORANGEHRM_USERNAME`: test account username.
- `ORANGEHRM_PASSWORD`: test account password.

### Secret Handling

- Sensitive inputs MUST be injected from Jenkins credentials.
- Plaintext credentials MUST NOT appear in repository files or job logs.

## Execution Contract

- Dependency setup:
  - Install dependencies from `requirements.txt` in a clean workspace.
- Test execution:
  - Smoke scope MUST include successful login, invalid login, and logout flows.
  - Any required scope failure MUST fail the run.
- Timeout behavior:
  - Scope timeouts MUST mark the run as failed/timeout and must not be interpreted as pass.

## Output Contract

### Status Outputs

- Required check status for pull requests: `pass` or `fail`.
- Build summary MUST include counts for passed, failed, and skipped tests.

### Artifact Outputs

- On failure, archive at minimum:
  - pytest execution log/output
  - screenshots captured by framework
- When available, archive:
  - Allure results directory
  - generated HTML report

## Quality Gate Contract

- Merge to protected branches MUST require a successful required QA check.
- Waiver/exemption (if used) MUST be explicit, time-bounded, and documented in pull request records.

## Observability Contract

- Build logs MUST identify:
  - trigger source
  - execution scope (`smoke` or `regression`)
  - failed test identifiers
- Artifact retention MUST be configured to support failure triage.

## Maintenance Contract

- Scope selection rules and schedules MUST be editable in one documented location.
- Pipeline documentation MUST identify maintainers and update process.
