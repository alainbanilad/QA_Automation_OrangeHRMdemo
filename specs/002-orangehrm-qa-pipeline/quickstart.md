# Quickstart: Jenkins CI/CD QA Pipeline for OrangeHRM

## Goal

Set up and maintain a simple Jenkins pipeline that enforces OrangeHRM smoke quality gates and runs daily regression.

## 1. Prerequisites

- Jenkins controller and at least one available build agent.
- Repository connected to Jenkins multibranch pipeline or equivalent PR-aware job.
- Jenkins credentials configured for three **Secret text** entries (see section 9 for required IDs).
- `allure` CLI available on the build agent or Docker image used by the pipeline.
- Network access from agent to OrangeHRM demo URL.

## 2. Minimum Pipeline Behavior

- Pull requests:
  - Run smoke scope only.
  - Fail check on any required test failure.
- Default branch pushes:
  - Run smoke scope at minimum.
- Scheduled run:
  - Run regression scope daily.

## 3. Suggested Stage Order

1. Checkout source
2. Set up Python environment
3. Install dependencies from `requirements.txt`
4. Execute selected scope (`smoke` or `regression`)
5. Publish results and archive artifacts
6. Mark build status for PR gate

## 4. Scope Selection Guidance

**One canonical location for each scope:**

- **Smoke scope marker** — controlled by the `-m "smoke and orangehrm"` expression in the `Smoke Tests` stage of `Jenkinsfile`.
  - To add a test to smoke: add `@pytest.mark.smoke` to the test function in the test file.
  - To change all smoke tests at once: update the marker expression in `Jenkinsfile` in the `Smoke Tests` stage `sh` block (look for the `# MAINTAINER:` comment).
- **Regression scope marker** — controlled by `-m "orangehrm"` in the `Regression Tests` stage of `Jenkinsfile`.
  - To add a test to regression-only runs: add `@pytest.mark.regression` to the test function.
- **Daily schedule** — controlled by the `cron('H 2 * * *')` entry in the `triggers` block at the top of `Jenkinsfile` (look for the `# MAINTAINER:` comment on the line above it).
- Change one side only (marker expression OR decorator) to avoid scope drift.

## 5. Failure Evidence

- Always archive on failure:
  - pytest console/log output
  - screenshots directory
- Also archive when available:
  - `allure-results/`
  - generated HTML report (for example `report.html`)

## 6. Secrets and Safety

- Use Jenkins credentials binding for all sensitive values.
- Never commit test credentials or tokens.
- Avoid printing sensitive environment values to logs.

## 7. Maintenance Checklist

- Verify PR gate still maps to smoke scope.
- Verify schedule still triggers daily regression.
- Review flaky tests and quarantine only with tracked action item.
- Keep this feature spec and contract updated when pipeline behavior changes.

## 8. Validation Run

- Open a pull request with an intentional smoke failure and confirm gate blocks merge.
- Open a pull request with passing smoke tests and confirm gate passes.
- Confirm failed run artifacts are available in Jenkins build outputs.

## 9. Credential ID Naming Convention

The `Jenkinsfile` `environment` block references three Jenkins credential IDs. Create matching **Secret text** credentials under **Jenkins > Manage Jenkins > Credentials**:

| Credential ID | What it holds |
|---|---|
| `orangehrm-base-url` | OrangeHRM demo base URL (no trailing slash) |
| `orangehrm-username` | Test account username |
| `orangehrm-password` | Test account password |

- If you need to rename a credential ID, update both the Jenkins credential record and the matching `credentials('...')` call in the `environment` block of `Jenkinsfile` (look for `# MAINTAINER:` comments).
- Never store raw values in repository files. Confirm with: `git grep -i 'password\|secret\|token' -- '*.py' '*.ini' 'Jenkinsfile'` — expect zero literal value matches.
