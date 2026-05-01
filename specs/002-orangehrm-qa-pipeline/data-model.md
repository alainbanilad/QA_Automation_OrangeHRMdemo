# Data Model: OrangeHRM Jenkins QA Pipeline

## Entity: PipelineRun

- Description: One Jenkins-triggered QA execution instance.
- Fields:
  - runId (string, required): Unique build identifier.
  - triggerType (enum, required): `pull_request`, `push_default_branch`, `scheduled_regression`, `manual`.
  - branchName (string, required): Source branch for run.
  - commitSha (string, required): Commit under test.
  - startTime (datetime, required)
  - endTime (datetime, optional until completion)
  - status (enum, required): `running`, `passed`, `failed`, `aborted`, `timeout`.
  - gateRequired (boolean, required): Whether run affects merge gate.

## Entity: ExecutionScope

- Description: Named test subset executed by a run.
- Fields:
  - scopeName (enum, required): `smoke`, `regression`.
  - selectorRule (string, required): Marker/path rule used to collect tests.
  - timeoutMinutes (integer, required): Max allowed runtime for scope.
  - requiredForMerge (boolean, required)

## Entity: QualityGateResult

- Description: Gate decision for pull-request merge eligibility.
- Fields:
  - gateId (string, required)
  - runId (string, required, relation to PipelineRun)
  - decision (enum, required): `pass`, `fail`, `waived`.
  - evaluatedAt (datetime, required)
  - reason (string, required): Human-readable decision reason.

## Entity: TestOutcomeSummary

- Description: Aggregated result counts emitted by test runner.
- Fields:
  - runId (string, required)
  - passedCount (integer, required)
  - failedCount (integer, required)
  - skippedCount (integer, required)
  - durationSeconds (integer, required)

## Entity: FailureArtifact

- Description: Debug evidence associated with a run.
- Fields:
  - artifactId (string, required)
  - runId (string, required)
  - artifactType (enum, required): `pytest_log`, `screenshot`, `allure_results`, `html_report`.
  - artifactPath (string, required)
  - retentionDays (integer, required)
  - published (boolean, required)

## Entity: SecretReference

- Description: Mapping between required secret and Jenkins credentials binding.
- Fields:
  - secretName (string, required): Logical name used by tests.
  - credentialId (string, required): Jenkins credential key.
  - injectedAs (enum, required): `environment_variable`, `file_binding`.
  - scope (enum, required): `pipeline`, `stage`.

## Relationships

- PipelineRun 1..* ExecutionScope: each run executes one or more scopes.
- PipelineRun 1..1 QualityGateResult for pull-request runs where gateRequired=true.
- PipelineRun 1..1 TestOutcomeSummary.
- PipelineRun 0..* FailureArtifact.
- ExecutionScope *..* SecretReference (through stage usage).

## Validation Rules

- Pull-request runs MUST include `smoke` scope and set `gateRequired=true`.
- Any required scope failure MUST force QualityGateResult.decision=`fail` unless waiver exists.
- Failed runs MUST publish at least one `pytest_log` artifact and screenshots when generated.
- SecretReference values MUST not contain raw secret values in versioned files.
- Scheduled regression runs MUST include `regression` scope.

## State Transitions

- PipelineRun.status: `running` -> `passed|failed|aborted|timeout`.
- QualityGateResult.decision: `pass|fail`, with optional transition to `waived` only by approved exception process.
- FailureArtifact.published: `false` -> `true` once archive/upload step succeeds.
