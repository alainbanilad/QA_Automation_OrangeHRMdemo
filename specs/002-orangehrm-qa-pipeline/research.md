# Phase 0 Research: OrangeHRM Jenkins QA Pipeline

## Decision 1: Use Jenkins Declarative Pipeline as the single orchestration entrypoint

- Decision: Keep one repository `Jenkinsfile` with clearly separated stages for setup, smoke execution, artifact publication, and scheduled regression.
- Rationale: A single declarative pipeline is easier to review and maintain, and stage naming keeps behavior easy to follow for new contributors.
- Alternatives considered:
  - Scripted Pipeline: more flexible but harder to read and maintain consistently.
  - Split pipelines across multiple Jenkins jobs: increases operational complexity and drift risk.

## Decision 2: Enforce PR quality gate via smoke scope only

- Decision: Run only OrangeHRM smoke tests on pull requests and fail the gate on any required test failure.
- Rationale: Fast feedback is essential for daily contribution flow; smoke scope directly covers constitution-critical authentication paths.
- Alternatives considered:
  - Full regression on every PR: higher confidence but too slow and harder to maintain for frequent merges.
  - No mandatory smoke gate: simpler setup but allows regressions into protected branches.

## Decision 3: Run regression on a daily schedule from default branch

- Decision: Configure Jenkins scheduled trigger for daily regression execution.
- Rationale: Balances confidence and runtime cost while meeting constitution guidance for regular full-suite validation.
- Alternatives considered:
  - Weekly regression only: insufficient for quick detection of latent failures.
  - Continuous regression on every push: expensive and noisy for this repository scope.

## Decision 4: Publish failure evidence as first-class pipeline outputs

- Decision: Always archive test logs and screenshots for failed runs; include Allure results when produced.
- Rationale: Reliable evidence shortens triage and removes dependence on local reproduction.
- Alternatives considered:
  - Console logs only: often insufficient for UI failures.
  - Manual artifact collection: inconsistent and high maintenance burden.

## Decision 5: Centralize secret usage through Jenkins credentials

- Decision: Inject credentials and sensitive runtime values from Jenkins credential storage and environment mapping.
- Rationale: Prevents plaintext leakage in repository and aligns with constitution secret-handling requirements.
- Alternatives considered:
  - `.env` committed defaults: insecure and policy-violating.
  - Manual per-agent secret setup without credentials binding: brittle and hard to maintain.

## Decision 6: Keep selection rules explicit and documented

- Decision: Document one canonical place to edit smoke scope and schedule behavior, with clear ownership in quickstart.
- Rationale: Reduces onboarding friction and limits accidental config divergence.
- Alternatives considered:
  - Implicit marker patterns spread across files: difficult for maintainers to trace.
  - Jenkins UI-only job config: less versioned transparency and harder peer review.
