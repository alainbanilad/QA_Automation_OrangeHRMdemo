# Implementation Plan: OrangeHRM QA Pipeline Baseline

**Branch**: `002-create-spec-branch` | **Date**: 2026-05-01 | **Spec**: `specs/002-orangehrm-qa-pipeline/spec.md`
**Input**: Feature specification from `specs/002-orangehrm-qa-pipeline/spec.md`

## Summary

Build a Jenkins-based CI/CD QA baseline that is simple to maintain and enforces mandatory OrangeHRM smoke validation (valid login, invalid login, logout) on pull requests and default-branch updates. The plan adds clear run separation for smoke versus regression, publishable failure evidence, and concise maintainer documentation so QA gates remain predictable and easy to evolve.

## Technical Context

**Language/Version**: Python 3.x for tests; Jenkins Declarative Pipeline (Jenkinsfile) for orchestration  
**Primary Dependencies**: pytest, Selenium-based page-object framework in `pages/` and `drivers/`, Jenkins pipeline steps, Allure/pytest HTML reporting already present in repo  
**Storage**: N/A for application data; pipeline stores logs/artifacts in Jenkins build records  
**Testing**: pytest (smoke and regression selection via markers or test paths)  
**Target Platform**: Jenkins agents (Windows/Linux capable) executing OrangeHRM UI automation against demo environment
**Project Type**: Test automation repository with CI pipeline orchestration  
**Performance Goals**: Smoke gate run completes in <=10 minutes for >=95% of normal runs; daily regression runs complete within configured Jenkins timeout  
**Constraints**: No hardcoded secrets, required smoke checks must block merge on failure, failure evidence must be retained, pipeline config must remain easy to follow and maintain  
**Scale/Scope**: One repository-level Jenkins pipeline covering PR gating and daily regression for OrangeHRM test suites

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Pre-Phase 0 Gate Review (PASS):

- Critical Flow Coverage: PASS. Smoke gate explicitly includes valid login, invalid login, and logout.
- Test Independence: PASS. Pipeline executes tests without order dependency assumptions.
- Stable and Readable Locators: PASS. Existing locator standards remain enforced by test framework conventions.
- Reliable Synchronization: PASS. No design introduces fixed waits as pipeline policy.
- Failure Evidence: PASS. Failed runs require artifact publishing (logs + screenshots, with Allure results when present).
- Minimum Technical Constraints: PASS. Configuration/env based URL and credentials; no hardcoded secrets.
- Minimum CI/CD QA Pipeline Requirements: PASS. Trigger strategy, gate behavior, artifact and secret handling, and daily regression are included.

Post-Phase 1 Re-check (PASS):

- `research.md` captures Jenkins-specific decisions for maintainability and gate behavior.
- `data-model.md` defines entities needed to reason about run status, scopes, and artifacts.
- `contracts/jenkins-qa-pipeline-contract.md` defines execution and quality-gate contract.
- `quickstart.md` provides maintainable operational steps for contributors and maintainers.
- No constitution violations or unresolved clarifications remain.

## Project Structure

### Documentation (this feature)

```text
specs/002-orangehrm-qa-pipeline/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── jenkins-qa-pipeline-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
api/
├── base_api.py
└── reqres_api.py

drivers/

pages/

tests/

conftest.py
pytest.ini
requirements.txt
Jenkinsfile
```

**Structure Decision**: Keep the existing single-repository pytest automation structure and implement CI orchestration through `Jenkinsfile`, while documenting behavior and contracts under `specs/002-orangehrm-qa-pipeline/` for maintainability.

## Complexity Tracking

No constitution violations requiring justification.
