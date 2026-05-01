# Tasks: OrangeHRM QA Pipeline Baseline

**Input**: Design documents from `specs/002-orangehrm-qa-pipeline/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/jenkins-qa-pipeline-contract.md, quickstart.md

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (touches a different file from concurrent tasks)
- **[US1/US2/US3]**: User story this task serves
- File paths are relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Extend existing configuration to support smoke/regression scope separation and safe artifact storage.

- [X] T001 Add `regression` marker definition to `pytest.ini` `markers =` block
- [X] T002 [P] Add `artifacts/` entry to `.gitignore` so captured screenshots are never committed

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Secure credential injection and a correct Allure workflow — these MUST be complete before any pipeline stage can run safely and produce trustworthy results.

**⚠️ CRITICAL**: No user-story pipeline work can begin until this phase is complete.

- [X] T003 Add `withCredentials` / `environment` block to `Jenkinsfile` binding `ORANGEHRM_BASE_URL`, `ORANGEHRM_USERNAME`, and `ORANGEHRM_PASSWORD` from Jenkins credential storage (replace hardcoded `VENV` environment block)
- [X] T004 Fix `Allure Report` stage in `Jenkinsfile` to run `allure generate allure-results -o allure-report --clean` only — remove the duplicate `pytest` call from that stage so tests execute exactly once per build

**Checkpoint**: Credentials flow from Jenkins store; Allure stage never re-runs tests.

---

## Phase 3: User Story 1 — Block Unsafe Changes Early (Priority: P1) 🎯 MVP

**Goal**: Every pull request triggers the smoke gate; any smoke failure blocks merge.

**Independent Test**: Open a PR with an intentional smoke failure — verify Jenkins marks the check as failed and merge is blocked. Open a passing PR — verify the gate passes.

- [X] T005 [US1] Add `triggers` block to `Jenkinsfile` with a `githubPullRequests` (or `pollSCM`/multibranch PR trigger) entry so pull requests automatically start a build
- [X] T006 [US1] Verify `tests/test_orangehrm_login.py` contains all three critical flows (valid login, invalid login, logout) and all three test functions carry `@pytest.mark.smoke` — add any missing marker decorators
- [X] T007 [US1] Confirm `Run Tests (Headless)` stage in `Jenkinsfile` propagates pytest non-zero exit as a build failure; add `set -e` or `returnStatus` guard if the current `sh` call could swallow the exit code

**Checkpoint**: Pull requests receive a required Jenkins smoke check; failure blocks merge.

---

## Phase 4: User Story 2 — Diagnose Failures Quickly (Priority: P2)

**Goal**: Every failed build automatically publishes evidence: logs, screenshots, and reporting artifacts.

**Independent Test**: Trigger a failing build; confirm `artifacts/screenshots/`, `allure-results/`, and `report.html` are all accessible from the Jenkins build page.

- [X] T008 [US2] Add `archiveArtifacts artifacts: 'artifacts/screenshots/**', allowEmptyArchive: true` to `post { failure { } }` block in `Jenkinsfile`
- [X] T009 [US2] Add `archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true` to `post { failure { } }` block in `Jenkinsfile`
- [X] T010 [US2] Move `archiveArtifacts artifacts: 'report.html'` into a dedicated `post { always { } }` block and add `archiveArtifacts artifacts: 'allure-report/**', allowEmptyArchive: true` alongside it in `Jenkinsfile`

**Checkpoint**: Failed builds expose screenshots, allure-results, allure-report, and HTML report without manual collection.

---

## Phase 5: User Story 3 — Keep the Pipeline Easy to Maintain (Priority: P3)

**Goal**: A clearly structured pipeline where scope, schedule, and credentials configuration are each findable in one documented place.

**Independent Test**: Ask a new contributor to locate (a) where to change smoke scope, (b) where to adjust the daily schedule, and (c) how credentials are referenced — all using only `Jenkinsfile` inline comments and `quickstart.md`.

- [X] T011 [US3] Add a `Regression` stage to `Jenkinsfile` that runs `pytest -m "orangehrm or regression"` with an explicit `timeout(time: 30, unit: 'MINUTES')` wrapper — keep it structurally separate from the smoke stage
- [X] T012 [US3] Add a `triggers { cron('H 2 * * *') }` block to `Jenkinsfile` for daily scheduled regression; scope the regression stage to run only on scheduled or default-branch builds using a `when` condition
- [X] T013 [US3] Add maintainer-facing inline comments to `Jenkinsfile` at: (a) the smoke marker selector line, (b) the cron schedule line, (c) each credential ID — format as `// MAINTAINER: <instruction>` for easy grep
- [X] T014 [P] [US3] Update `specs/002-orangehrm-qa-pipeline/quickstart.md` section 4 (Scope Selection Guidance) to reference the exact `Jenkinsfile` line location and marker name for smoke; add section 9 with credential ID naming convention

**Checkpoint**: New maintainer can explain trigger rules, scope, and credential setup in under 15 minutes using only in-repo documentation.

---

## Final Phase: Polish & Cross-Cutting Concerns

- [X] T015 [P] Verify no plaintext credentials or tokens exist in any committed file by running `git grep -i 'password\|secret\|token' -- '*.py' '*.ini' 'Jenkinsfile'` and confirming zero matches on literal values
- [X] T016 Run the `quickstart.md` section 8 validation scenario end-to-end: smoke-pass gate, smoke-fail gate block, and artifact review from a build page

---

## Analysis Remediation Phase: Gap Coverage

**Purpose**: Close gaps identified by `/speckit.analyze` — branch-protection docs, API key support, regression-marker alignment, smoke timing, and preflight checks.

- [X] T017 [US1] Document Jenkins required-status-check setup for FR-005 (branch protection): add section 10 to `quickstart.md` with step-by-step GitHub → Settings → Branches → Add required status check instructions referencing the Jenkins job name
- [X] T018 [P] [US3] Add a note to `quickstart.md` prerequisites (section 1) about the Jenkins GitHub Branch Source / Multibranch Pipeline plugin requirement needed for `changeRequest()` PR detection (resolves A1 ambiguity)
- [X] T019 [US1] Add `SECONDS=0` / `echo "Smoke suite completed in ${SECONDS}s"` to `Smoke Tests` stage in `Jenkinsfile` so SC-002 (smoke under 10 min / 600s) can be tracked from build logs
- [X] T020 [US3] Add `pip check` after `pip install` in the `Setup Python Environment` stage of `Jenkinsfile` to satisfy FR-012 (dependency preflight with clear errors) — resolves U2 underspecification
- [X] T021 [US3] Align regression marker: update `Jenkinsfile` Regression stage to `-m "orangehrm or regression"` and update MAINTAINER comment so `@pytest.mark.regression` tests are actually collected — resolves I1 mismatch between T011 description and prior implementation

---

## CI Agent Hardening Phase: Docker Image & Build Reliability

**Purpose**: Close three verified gaps that would cause all Jenkins builds to fail with the previous `python:3.11-slim` agent: missing Chrome for Selenium, missing Allure CLI for report generation, and inaccurate smoke timing due to bash-only `SECONDS` builtin not working under `dash` (`/bin/sh` on Debian slim).

- [X] T022 Create `Dockerfile.jenkins` extending `python:3.11-slim` with Google Chrome stable, OpenJDK 17 JRE, and Allure CLI 2.30.0 — these three tools are absent from the base image and required for the pipeline to run end-to-end
- [X] T023 Update `Jenkinsfile` agent block from `docker { image 'python:3.11-slim' }` to `dockerfile { filename 'Dockerfile.jenkins' }` so the pipeline uses the hardened image
- [X] T024 Fix smoke timing in `Jenkinsfile`: replace `SECONDS=0` / `${SECONDS}` (bash-only builtin, silently outputs 0 under `/bin/sh`) with POSIX-compatible `SMOKE_START=$(date +%s)` / `SMOKE_ELAPSED=$(( $(date +%s) - SMOKE_START ))` arithmetic
- [X] T025 [P] Fix `conftest.py` Chrome options: replace `--start-maximized` (no-op in headless mode) with `--window-size=1920,1080` and add `--disable-gpu` for Docker container compatibility
- [X] T026 [P] Update `.env.example` to document `REQRES_API_KEY` optional variable with a hint to app.reqres.in, and populate the OrangeHRM demo public values so new contributors can run immediately

**Checkpoint**: `Dockerfile.jenkins` builds successfully; full test suite (6 passed, 1 skipped) confirmed green after all changes; Allure report generated without CLI errors in CI.

**Checkpoint**: All CRITICAL and HIGH analysis findings resolved; coverage reaches ≥ 94 %.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately; T001 and T002 are parallel.
- **Foundational (Phase 2)**: Depends on Phase 1. T003 and T004 are independent and can proceed in parallel. Blocks all user story phases.
- **User Story phases (3–5)**: All depend on Phase 2 completion. Stories can proceed in priority order or in parallel if team capacity allows.
- **Polish (Final Phase)**: Depends on all user story phases being complete.

### User Story Dependencies

- **US1 (P1)**: Depends on Foundational. T005, T006, T007 are sequential within the story (credentials must exist before trigger; marker must exist before gate test).
- **US2 (P2)**: Depends on Foundational. T008–T010 are sequential edits to the same `Jenkinsfile` post block; no dependency on US1 completion.
- **US3 (P3)**: Depends on Foundational. T011–T012 must precede T013 (comment existing lines); T014 is parallel to T011–T013.

### Parallel Opportunities

| Parallel group | Tasks |
|---|---|
| Phase 1 | T001 (pytest.ini) and T002 (.gitignore) |
| Phase 2 | T003 (Jenkinsfile env) and T004 (Jenkinsfile stage) — different sections |
| Phase 3 start | T006 (test file markers) can begin while T005 (Jenkinsfile trigger) is in review |
| Phase 5 | T014 (quickstart.md) runs in parallel with T011–T013 (Jenkinsfile edits) |
| Polish | T015 (grep check) is parallel to T016 (manual validation) |

---

## Parallel Example: Phase 1

```text
In parallel:
  T001 — edit pytest.ini: add regression marker
  T002 — edit .gitignore: add artifacts/ entry
```

## Parallel Example: Phase 5

```text
In parallel:
  Thread A: T011 → T012 → T013  (Jenkinsfile: regression stage, cron, comments)
  Thread B: T014                  (quickstart.md: scope/maintenance docs)
Then merge and proceed to T015/T016.
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001, T002)
2. Complete Phase 2: Foundational (T003, T004)
3. Complete Phase 3: US1 — PR smoke gate (T005, T006, T007)
4. **STOP and VALIDATE**: Run the PR gate scenario. Smoke gate passes on green, fails on red.
5. Ship MVP — contributors now have a required quality check on every PR.

### Incremental Delivery

1. Phase 1 + 2 → secure, correct baseline
2. Phase 3 (US1) → PR gates enforced — **MVP deliverable**
3. Phase 4 (US2) → failure diagnosis artifacts — faster triage
4. Phase 5 (US3) → daily regression + maintainable structure — long-term health
5. Polish → validation and hygiene sweep

---

## Notes

- All three critical authentication flows must carry `@pytest.mark.smoke` before the gate can be trusted.
- The existing `Jenkinsfile` runs pytest twice (once in the test stage, once in the Allure stage); T004 eliminates this duplication — it is foundational before any result counts can be trusted.
- `[P]` tasks touch different files; they can be assigned to different contributors without merge conflicts.
- `artifacts/screenshots/` is written by `conftest.py` automatically on any driver-using test failure.
- Keep `Jenkinsfile` readable: one clear stage per concern, no logic beyond invoking venv + pytest.
