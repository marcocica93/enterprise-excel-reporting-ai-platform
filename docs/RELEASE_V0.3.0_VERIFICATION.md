# v0.3.0 verification

- Date: 14 October 2026
- Scope: Cleaning and Business Rules Engine (BR-001, BR-002, BR-003)
- Reviewed development commit: `2a3bf2eaf23b1ea58b7256d875cd6396c8840b7c`
- Verification branch: `release/v0.3.0-verification`
- Result: local verification passed with the empty-input correction in this branch; publication is pending.

## Findings and correction

The merged development code passed all 80 existing tests. Additional release
verification found that a schema-correct dataset with no rows raised
`AttributeError` in `validate_tickets`: assigning an empty list inferred a
floating-point validation-error column, incompatible with `.str.len()`.

The correction explicitly creates an object-typed Series with the source index.
It preserves all twelve validation rules and public interfaces. Regression tests
cover an empty validator input and both empty and all-rejected inputs through
cleaning, lifecycle classification, elapsed-time calculation, and SLA classification.
Before the correction, the two empty-input tests failed and the all-rejected test
passed. After the correction, all three pass.

## Verification results

| Check | Result |
|---|---|
| Focused validator and business-rule tests | 74 passed |
| Full automated suite | 83 passed |
| Dependency versions | All 12 pins in requirements.txt match the test environment |
| Git diff whitespace checks | Passed |
| Original source data | Preserved |
| Repeated processing with the same report timestamp | Identical valid and rejected results |
| Independent scalar calculation | Elapsed hours and SLA classification agree for all 20 valid tickets |
| Empty pipeline | Zero output rows; derived output columns retained |
| All-rejected pipeline | Zero valid output rows; all 10 rejected records retained |

Tests ran with Python 3.12, pandas 3.0.3, NumPy 2.5.1, and pytest 9.1.1.
These are local results, not GitHub Actions results. No clean-environment install
was performed; dependency versions were checked in the existing test environment.

## Approved synthetic baseline

Source: `examples/input/synthetic_it_ticket_dataset.xlsx`.
Reference: `docs/DATASET_SPECIFICATION.md`.
Explicit report timestamp: `2026-07-01 12:00`.

| Measure | Expected | Observed |
|---|---:|---:|
| Input records | 30 | 30 |
| Valid records | 20 | 20 |
| Rejected records | 10 | 10 |
| Backlog | 10 | 10 |
| Completed | 10 | 10 |
| SLA met | 10 | 10 |
| SLA breached | 10 | 10 |
| SLA compliance | 50.0% | 50.0% |
| Average completed resolution time | 25.4 hours | 25.4 hours |

Backlog by team matches: Service Desk 3, Applications 3, Infrastructure 2,
Security 2. Backlog by priority matches: P1 2, P2 3, P3 3, P4 2.
These aggregates were calculated for verification; the planned KPI Engine
is not implemented by this release.

## Scope and operating contract

Process records in this order: loader, validation, cleaning of valid records,
lifecycle classification, elapsed-time calculation, and SLA classification.
Use the same explicit, non-missing report timestamp throughout. Datetimes must
be timezone-compatible. Business-rule functions consume validated and normalized
records; they are not replacements for input validation. SLA equality is `MET`,
with no rounding before comparison.

The release remains a set of Python processing components. KPI and report
generation, CLI/application orchestration, Flask, AI commentary, and deployment
are not delivered by this milestone. The complete MVP acceptance criteria are
therefore not all satisfied yet.

## Publication steps

1. Commit and publish this correction, regression tests, and documentation.
2. Review and merge into `feature/cleaning-business-rules-engine`.
3. Prepare release metadata in README and CHANGELOG, then review the development
   branch for merge into `main`.
4. Create `v0.3.0` only on the approved release commit.

Commit, push, merge, and tagging require Marco's authorization under `AGENTS.md`.
