# Research: OrangeHRM Test Automation Foundation

## Decision 1: Use pytest as the test runner and assertion engine

- Decision: Use pytest as the primary testing framework for OrangeHRM UI automation.
- Rationale: It is already aligned with repository structure (`pytest.ini`, existing test files), supports readable tests, fixtures, markers, and smooth CI integration.
- Alternatives considered: unittest (more boilerplate), nose (legacy and less preferred for modern maintenance).

## Decision 2: Keep and strengthen Page Object Model organization

- Decision: Continue using page classes in `pages/` with focused methods for OrangeHRM login and logout interactions.
- Rationale: Current project already follows page object patterns; continuing this keeps tests easy to follow and reduces maintenance cost when UI selectors evolve.
- Alternatives considered: direct selectors in tests (faster initially but harder to maintain), keyword-driven abstraction (extra indirection not needed for current scope).

## Decision 3: Enforce explicit waits and remove fixed sleep dependence

- Decision: Use explicit waits/assertion-based synchronization for login and logout transitions.
- Rationale: Explicit waits reduce flaky behavior from timing variance and align with constitution reliability requirements.
- Alternatives considered: fixed sleep calls (simple but brittle and slower), aggressive implicit waits only (less targeted and harder to reason about).

## Decision 4: Standardize failure evidence capture

- Decision: Capture screenshot and failure context on UI test failure through centralized hooks/fixtures.
- Rationale: Centralized capture gives consistent evidence and avoids duplicated failure-handling logic across tests.
- Alternatives considered: per-test manual screenshots (inconsistent and repetitive), logs-only evidence (insufficient for UI debugging).

## Decision 5: Configuration-driven environment and credentials

- Decision: Read base URL and credentials from environment variables or centralized config.
- Rationale: Keeps secrets out of test code and supports local/CI variability.
- Alternatives considered: hardcoded credentials (security risk), ad-hoc local-only config files without convention (poor portability).

## Decision 6: Define a smoke subset for CI gate

- Decision: Keep a smoke subset centered on authentication-critical flows (valid login, invalid login, logout).
- Rationale: Fast and meaningful feedback preserves CI throughput while protecting high-value behavior.
- Alternatives considered: full-suite-only gate (slower feedback), single login-success check only (insufficient risk coverage).
