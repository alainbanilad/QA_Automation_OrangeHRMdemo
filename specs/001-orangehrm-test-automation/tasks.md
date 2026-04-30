# Tasks: OrangeHRM Test Automation Foundation

**Input**: Design documents from `/specs/001-orangehrm-test-automation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are included because this feature explicitly delivers automated testing behavior.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Align project-level test execution settings and shared runtime configuration.

- [x] T001 Define smoke and orangehrm pytest markers in pytest.ini
- [x] T002 Create environment variable template for OrangeHRM credentials in .env.example
- [x] T003 Update authentication run instructions and required variables in specs/001-orangehrm-test-automation/quickstart.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build reusable OrangeHRM test infrastructure required by all user stories.

**⚠️ CRITICAL**: No user story work should begin until this phase is complete.

- [x] T004 Add environment-driven base URL and credential fixtures in conftest.py
- [x] T005 [P] Add centralized screenshot-on-failure pytest hook and artifact path handling in conftest.py
- [x] T006 [P] Add explicit wait-based helper methods for login state and error state in pages/orangehrm_login_page.py
- [x] T007 Remove hardcoded OrangeHRM URL from pages/orangehrm_login_page.py and consume fixture-driven navigation from conftest.py

**Checkpoint**: Foundation ready; user stories can now be implemented independently.

---

## Phase 3: User Story 1 - Validate Login Reliability (Priority: P1) 🎯 MVP

**Goal**: Validate successful and unsuccessful login behavior with stable and deterministic pytest coverage.

**Independent Test**: Run pytest tests/test_orangehrm_login.py -k "login_success or login_invalid" and verify both scenarios complete without relying on prior tests.

### Tests for User Story 1

- [x] T008 [US1] Add failing-first success and invalid login scenario tests in tests/test_orangehrm_login.py
- [x] T009 [US1] Add blank-credential boundary test in tests/test_orangehrm_login.py

### Implementation for User Story 1

- [x] T010 [US1] Implement invalid login error detection and blank-input handling methods in pages/orangehrm_login_page.py
- [x] T011 [US1] Update login success assertions to use explicit waits and stable locators in tests/test_orangehrm_login.py
- [x] T012 [US1] Mark critical login tests as smoke and orangehrm in tests/test_orangehrm_login.py
- [x] T013 [US1] Validate and document expected failure evidence output for login tests in specs/001-orangehrm-test-automation/contracts/test-execution-contract.md

**Checkpoint**: User Story 1 is independently functional and smoke-ready.

---

## Phase 4: User Story 2 - Confirm Session Exit Safety (Priority: P2)

**Goal**: Ensure logout reliably terminates authenticated sessions and blocks protected access.

**Independent Test**: Run pytest tests/test_orangehrm_login.py -k logout and verify logout completes and protected pages require re-authentication.

### Tests for User Story 2

- [x] T014 [US2] Add failing-first logout flow test in tests/test_orangehrm_login.py
- [x] T015 [US2] Add post-logout protected-route access test in tests/test_orangehrm_login.py

### Implementation for User Story 2

- [x] T016 [US2] Implement user-menu logout interaction methods with explicit waits in pages/orangehrm_login_page.py
- [x] T017 [US2] Implement post-logout login-page detection helper in pages/orangehrm_login_page.py
- [x] T018 [US2] Finalize logout assertions and cleanup behavior in tests/test_orangehrm_login.py

**Checkpoint**: User Stories 1 and 2 both pass independently.

---

## Phase 5: User Story 3 - Keep Tests Understandable and Maintainable (Priority: P3)

**Goal**: Improve readability, discoverability, and long-term maintainability of OrangeHRM tests.

**Independent Test**: A new contributor can run pytest tests/test_orangehrm_login.py and pytest -m smoke using only repository guidance.

### Tests for User Story 3

- [x] T019 [P] [US3] Reorganize OrangeHRM tests into clear scenario-focused test names in tests/test_orangehrm_login.py
- [x] T020 [P] [US3] Add fixture-level docstrings and intent comments for shared test setup in conftest.py

### Implementation for User Story 3

- [x] T021 [US3] Add maintainability guidance for test naming and marker usage in tests/README.md
- [x] T022 [US3] Add concise OrangeHRM page object usage notes in pages/orangehrm_login_page.py
- [x] T023 [US3] Add onboarding run examples and expected outcomes in specs/001-orangehrm-test-automation/quickstart.md

**Checkpoint**: All user stories are independently testable and maintainable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency, CI alignment, and regression hardening across all stories.

- [x] T024 [P] Update smoke command alignment for OrangeHRM auth checks in Jenkinsfile
- [x] T025 [P] Verify dependency completeness for pytest execution in requirements.txt
- [x] T026 Run full local validation commands documented in specs/001-orangehrm-test-automation/quickstart.md and record outcomes in specs/001-orangehrm-test-automation/quickstart.md
- [x] T027 Perform final selector stability and no-hardcoded-secrets audit across conftest.py and pages/orangehrm_login_page.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies; starts immediately.
- **Phase 2 (Foundational)**: Depends on Phase 1; blocks all user story work.
- **Phase 3 (US1)**: Depends on Phase 2; defines MVP.
- **Phase 4 (US2)**: Depends on Phase 2 and uses authenticated flow from US1.
- **Phase 5 (US3)**: Depends on Phase 2; can run in parallel with later US2 work after core helpers exist.
- **Phase 6 (Polish)**: Depends on completion of all desired user stories.

### User Story Dependencies

- **US1 (P1)**: No dependencies on other user stories.
- **US2 (P2)**: Uses login capability from US1 but remains independently testable once foundational + login helpers are in place.
- **US3 (P3)**: Depends on existing OrangeHRM test coverage from US1/US2 to standardize maintainability patterns.

### Within Each User Story

- Write failing-first tests before implementation methods.
- Add page-object capabilities before finalizing test assertions.
- Finish story-level smoke marker and evidence expectations before story checkpoint.

---

## Parallel Execution Examples

### User Story 1

- Run T009 and T013 in parallel (test boundary case in tests/test_orangehrm_login.py and contract updates in specs/001-orangehrm-test-automation/contracts/test-execution-contract.md).
- Run T011 and T013 in parallel (test assertion hardening in tests/test_orangehrm_login.py and contract updates in specs/001-orangehrm-test-automation/contracts/test-execution-contract.md).

### User Story 2

- Run T016 and T018 in parallel (page helper implementation in pages/orangehrm_login_page.py and test assertion refinement in tests/test_orangehrm_login.py).
- Run T017 and T018 in parallel (post-logout helper in pages/orangehrm_login_page.py and test assertion refinement in tests/test_orangehrm_login.py).

### User Story 3

- Run T019 and T020 in parallel (test naming clarity vs fixture documentation).
- Run T021 and T023 in parallel (test usage docs vs quickstart onboarding docs).

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1.
2. Complete Phase 2.
3. Complete Phase 3 (US1).
4. Validate with pytest tests/test_orangehrm_login.py -k "login_success or login_invalid".
5. Use this as the first mergeable increment.

### Incremental Delivery

1. Ship US1 for critical login reliability.
2. Add US2 for logout and session-safety protection.
3. Add US3 maintainability improvements without changing tested behavior.
4. Finish with Phase 6 cross-cutting polish.

### Parallel Team Strategy

1. One engineer completes setup/foundational tasks.
2. After Phase 2:
   - Engineer A drives US1 test and page updates.
   - Engineer B drives US2 logout coverage.
   - Engineer C drives US3 documentation and readability hardening.

---

## Notes

- All tasks follow the required checklist format with IDs and file paths.
- [P] indicates tasks that can run in parallel when no incomplete dependency exists.
- Story labels are applied only to user story phase tasks.
- Keep commits scoped to one task or one coherent task group.
