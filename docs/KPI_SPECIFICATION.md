# KPI Engine Specification

## Document status

- **Version:** 1.0
- **Status:** Approved for v0.4.0 implementation
- **Milestone:** v0.4.0 — KPI and Reporting Engine
- **Use case:** IT Ticket Backlog & SLA Reporting
- **Source requirements:** `docs/MVP_BUSINESS_REQUIREMENTS.md`
- **Baseline dataset:** `examples/input/synthetic_it_ticket_dataset.xlsx`

## 1. Business objective

The KPI Engine converts validated and enriched ticket records into deterministic,
auditable management indicators for an IT Operations Manager.

It must support decisions about:

- current workload and backlog;
- open tickets already outside SLA;
- completed-ticket SLA performance;
- workload and performance by operational team;
- workload and performance by priority;
- data-quality failures;
- reconciliation between input, valid, rejected, backlog, completed, and SLA totals.

The KPI Engine calculates facts only. Excel formatting and management commentary
belong to downstream components.

## 2. Scope

The v0.4.0 KPI Engine must produce:

1. an executive summary;
2. KPI results by assigned team;
3. KPI results by priority;
4. a data-quality summary by validation rule;
5. reconciliation checks.

The Reporting Engine will later consume these outputs and create the required Excel
worksheets.

## 3. Input contract

The logical operation receives two DataFrames:

- `valid_records`: validated, cleaned, and enriched ticket records;
- `rejected_records`: rejected records containing validation errors.

### 3.1 Required valid-record columns

- `ticket_id`
- `priority`
- `assigned_team`
- `lifecycle_status`
- `elapsed_hours`
- `sla_status`

The KPI Engine assumes that the upstream pipeline has already executed:

1. structural loading;
2. record validation;
3. cleaning;
4. lifecycle classification;
5. elapsed-hours calculation;
6. SLA classification.

### 3.2 Required rejected-record columns

- `validation_errors`

Each value must contain the list of applicable validation-rule identifiers.

### 3.3 Preconditions

- `lifecycle_status` contains only `BACKLOG` or `COMPLETED`;
- `sla_status` contains only `MET` or `BREACHED`;
- `elapsed_hours` is numeric, non-missing, and non-negative;
- `assigned_team` is non-missing and non-blank;
- `priority` contains only `P1`, `P2`, `P3`, or `P4`;
- source DataFrames are not mutated.

Team labels must be normalized upstream by trimming leading and trailing whitespace
before KPI grouping. Case and internal spacing are preserved because changing them
could merge distinct business labels without an approved mapping.

A violated precondition is an internal pipeline error and must fail fast. It is not
converted into a record-level rejection by the KPI Engine.

## 4. Output contract

The logical result contains:

- `executive_summary`;
- `kpi_by_team`;
- `kpi_by_priority`;
- `data_quality_summary`;
- `reconciliation_checks`.

The concrete Python result type will be immutable at the container level and will
preserve explicit DataFrame schemas for tabular outputs.

## 5. Executive-summary rules

| Rule | Output field | Definition |
|---|---|---|
| `KPI-001` | `total_input_records` | valid records + rejected records |
| `KPI-002` | `valid_ticket_count` | number of valid records |
| `KPI-003` | `rejected_record_count` | number of rejected records |
| `KPI-004` | `rejected_record_rate` | rejected / total input × 100 |
| `KPI-005` | `backlog_count` | valid records with lifecycle `BACKLOG` |
| `KPI-006` | `completed_count` | valid records with lifecycle `COMPLETED` |
| `KPI-007` | `sla_met_count` | valid records with SLA `MET` |
| `KPI-008` | `sla_breached_count` | valid records with SLA `BREACHED` |
| `KPI-009` | `current_sla_met_rate` | SLA met / valid tickets × 100 |
| `KPI-010` | `open_sla_breached_count` | backlog records with SLA `BREACHED` |
| `KPI-011` | `completed_sla_met_count` | completed records with SLA `MET` |
| `KPI-012` | `completed_sla_breached_count` | completed records with SLA `BREACHED` |
| `KPI-013` | `completed_sla_compliance_rate` | completed SLA met / completed × 100 |
| `KPI-014` | `average_resolution_hours` | mean elapsed hours for completed records |

### 5.1 SLA terminology

`current_sla_met_rate` is a point-in-time health measure across all valid tickets,
including active records.

`completed_sla_compliance_rate` is the final performance measure for completed
records only. These indicators must not be presented as interchangeable.

### 5.2 Zero-denominator behavior

- percentage outputs are `0.0` when their denominator is zero;
- `average_resolution_hours` is `None` when no completed record exists;
- zero is not used for a missing average because it would imply immediate resolution.

## 6. KPI by team

The output contains one row for each assigned team present in valid records.

| Column | Definition |
|---|---|
| `assigned_team` | operational team label |
| `total_tickets` | valid tickets assigned to the team |
| `backlog_count` | team backlog |
| `completed_count` | team completed tickets |
| `open_sla_breached_count` | team backlog already outside SLA |
| `completed_sla_met_count` | completed tickets within SLA |
| `completed_sla_breached_count` | completed tickets outside SLA |
| `completed_sla_compliance_rate` | completed SLA met / completed × 100 |
| `average_resolution_hours` | mean elapsed hours for completed team tickets |

Team rows are ordered deterministically by `assigned_team` in ascending order.
An empty valid dataset returns an empty DataFrame with the complete schema.

## 7. KPI by priority

The output uses the fixed business order:

1. `P1`
2. `P2`
3. `P3`
4. `P4`

| Column | Definition |
|---|---|
| `priority` | controlled priority value |
| `total_tickets` | valid tickets with the priority |
| `backlog_count` | priority backlog |
| `completed_count` | completed tickets |
| `open_sla_breached_count` | backlog already outside SLA |
| `completed_sla_met_count` | completed tickets within SLA |
| `completed_sla_breached_count` | completed tickets outside SLA |
| `completed_sla_compliance_rate` | completed SLA met / completed × 100 |
| `average_resolution_hours` | mean elapsed hours for completed tickets |

All four priorities remain present in the result, including priorities with zero
records. This produces a stable reporting schema and makes comparisons explicit.

## 8. Data-quality summary

Rejected records are excluded from all operational KPI calculations.

The data-quality output contains one row for each validation rule
`VAL-001` through `VAL-012`.

| Column | Definition |
|---|---|
| `validation_rule` | validation-rule identifier |
| `affected_record_count` | rejected records containing the rule |
| `affected_input_rate` | affected records / total input × 100 |

Because one rejected record may contain multiple validation errors, the sum of
`affected_record_count` may exceed `rejected_record_count`.

The executive result also identifies `most_frequent_rejection_rules`:

- an empty tuple when no record is rejected;
- otherwise, every rule tied for the highest affected-record count;
- ties are ordered by validation-rule identifier.

## 9. Reconciliation rules

| Rule | Reconciliation |
|---|---|
| `REC-001` | total input = valid + rejected |
| `REC-002` | valid = backlog + completed |
| `REC-003` | valid = SLA met + SLA breached |
| `REC-004` | backlog = sum of backlog by team |
| `REC-005` | backlog = sum of backlog by priority |
| `REC-006` | completed = sum of completed by team |
| `REC-007` | completed = sum of completed by priority |
| `REC-008` | completed = completed SLA met + completed SLA breached |

A failed reconciliation raises a clear application error. The engine must not return
a result that it knows to be internally inconsistent.

## 10. Precision and presentation rules

- KPI calculations preserve full numeric precision;
- no rounding occurs inside the KPI Engine;
- the Reporting Engine owns display rounding and percentage formatting;
- repeated execution with identical inputs produces identical results;
- row order is deterministic;
- source indexes do not affect aggregate results;
- source DataFrames remain unchanged.

## 11. High-value extensions after the core engine

The following indicators may be added after the mandatory rules pass:

- oldest backlog age;
- average backlog age;
- median completed resolution time;
- P1/P2 backlog outside SLA;
- SLA-consumption percentage;
- SLA-risk bands based on approved threshold ranges.

Risk-band thresholds require explicit business approval before implementation and
must not be invented in code.

## 12. Out of scope

The current dataset cannot support:

- first-response time;
- reopened-ticket rate;
- reassignment count;
- customer satisfaction;
- team capacity utilization;
- backlog growth over time;
- weekly or monthly trends;
- created-versus-resolved throughput.

These require additional fields, historical snapshots, or both.

## 13. Acceptance criteria

The KPI Engine is accepted when:

1. all mandatory executive KPIs follow the approved formulas;
2. current SLA health and completed SLA compliance are reported separately;
3. rejected records do not contribute to operational KPIs;
4. team results use deterministic alphabetical ordering;
5. priority results use the fixed `P1`–`P4` order;
6. empty and all-rejected inputs return valid, stable output schemas;
7. zero denominators follow the approved behavior;
8. missing averages return `None`;
9. multi-error rejected records are counted correctly by validation rule;
10. all reconciliation rules pass or processing fails clearly;
11. the synthetic baseline retains 30 input, 20 valid, 10 rejected, 10 backlog,
    10 completed, 10 SLA met, 10 SLA breached, 50.0% current SLA met rate, and
    25.4 average completed resolution hours;
12. source DataFrames are preserved;
13. calculations are deterministic;
14. focused and full automated test suites pass.

The completed-ticket SLA compliance baseline will be measured from the approved
synthetic dataset during the first integration test and then recorded here. It must
not be guessed.

## 14. Planned implementation sequence

1. validate the KPI input contract;
2. implement executive counts and reconciliations;
3. implement SLA rates and completed resolution time;
4. implement team aggregation;
5. implement priority aggregation;
6. implement data-quality aggregation;
7. verify the full synthetic baseline;
8. review and refactor;
9. implement the Reporting Engine using only approved KPI outputs.
