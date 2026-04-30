# Data Model: OrangeHRM Test Automation Foundation

## Entity: Credential Input

- Purpose: Represents configured login data used for authentication tests.
- Fields:
  - username (string, required)
  - password (string, required)
  - credential_type (enum: valid, invalid)
- Validation Rules:
  - username and password must be non-null strings for valid and invalid scenarios.
  - Valid credential set must map to an account with dashboard access.

## Entity: Test Case

- Purpose: Defines one independently runnable verification of behavior.
- Fields:
  - id (string, unique)
  - title (string)
  - priority (enum: P1, P2, P3)
  - preconditions (list of strings)
  - steps (list of strings)
  - expected_result (string)
  - marker (string, optional; e.g., smoke)
- Validation Rules:
  - Must have clear expected_result.
  - Must run without dependency on prior test execution.

## Entity: Test Run

- Purpose: Captures execution of one or more test cases in a run context.
- Fields:
  - run_id (string)
  - started_at (datetime)
  - finished_at (datetime)
  - scope (enum: smoke, full)
  - status (enum: passed, failed)
  - case_results (list of Test Case Result)
- Validation Rules:
  - finished_at must be >= started_at.
  - status is failed if any case result is failed.

## Entity: Test Case Result

- Purpose: Stores outcome data for a single test case within a run.
- Fields:
  - test_case_id (string)
  - outcome (enum: passed, failed, skipped)
  - failure_message (string, optional)
  - evidence_refs (list of Failure Artifact references)
- Validation Rules:
  - On failed outcome, failure_message must be present.

## Entity: Failure Artifact

- Purpose: Preserves debug evidence for failed UI checks.
- Fields:
  - artifact_type (enum: screenshot, log)
  - path (string)
  - created_at (datetime)
  - linked_test_case_id (string)
- Validation Rules:
  - At least one screenshot artifact is required for each failed critical-flow UI test.

## Relationships

- One Test Run has many Test Case Results.
- One Test Case Result references one Test Case.
- One Test Case Result has zero or more Failure Artifacts.
- Credential Input is consumed by Test Cases for authentication behavior.

## State Transitions

- Test Case Result: passed -> (terminal), failed -> (terminal), skipped -> (terminal).
- Test Run: started -> passed or failed.