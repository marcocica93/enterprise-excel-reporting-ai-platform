# Synthetic Ticket Dataset Specification

## Status

- **Version:** 1.0
- **Dataset:** `examples/input/synthetic_it_ticket_dataset.xlsx`
- **Report datetime:** `2026-07-01 12:00`
- **Data classification:** Synthetic
- **Purpose:** MVP validation, SLA, KPI, and regression-test baseline

## Workbook structure

### `Dataset_Guide`

Human-readable description of the approved assumptions and expected aggregate results.

### `Tickets`

Input worksheet consumed by the future Excel adapter.

Required columns:

- `ticket_id`
- `created_at`
- `closed_at`
- `status`
- `priority`
- `assigned_team`
- `sla_target_hours`

## Dataset composition

| Classification | Rows |
|---|---:|
| Total | 30 |
| Designed valid | 20 |
| Designed invalid | 10 |

The first 20 ticket records are valid according to the approved MVP requirements. The final 10 records deliberately exercise validation failures.

## Expected valid-data baseline

| KPI | Expected result |
|---|---:|
| Valid tickets | 20 |
| Backlog | 10 |
| Completed | 10 |
| SLA met | 10 |
| SLA breached | 10 |
| SLA compliance rate | 50.0% |
| Average completed resolution time | 25.4 hours |

### Backlog by team

| Team | Expected backlog |
|---|---:|
| Service Desk | 3 |
| Applications | 3 |
| Infrastructure | 2 |
| Security | 2 |

### Backlog by priority

| Priority | Expected backlog |
|---|---:|
| P1 | 2 |
| P2 | 3 |
| P3 | 3 |
| P4 | 2 |

## Designed-invalid records

| Worksheet row | Ticket | Expected validation condition |
|---:|---|---|
| 22 | blank identifier | missing `ticket_id`; active ticket has `closed_at` |
| 23 | `TKT-DUP` | duplicated identifier; completed ticket missing `closed_at` |
| 24 | `TKT-DUP` | duplicated identifier; active ticket has `closed_at` |
| 25 | `TKT-024` | invalid `created_at` |
| 26 | `TKT-025` | `created_at` later than `report_datetime` |
| 27 | `TKT-026` | `closed_at` earlier than `created_at` |
| 28 | `TKT-027` | unsupported status `PENDING` |
| 29 | `TKT-028` | unsupported priority `P5` |
| 30 | `TKT-029` | missing `assigned_team` |
| 31 | `TKT-030` | non-positive `sla_target_hours` |

A record may contain more than one rejection reason. The Validation Engine must retain all applicable reasons.

## SLA boundary coverage

The dataset includes tickets whose elapsed time is:

- below the SLA target;
- exactly equal to the SLA target;
- greater than the SLA target.

Exact equality must be classified as SLA met.

## Usage rules

- Do not manually correct the invalid records.
- Do not use the invalid records in business KPI calculations.
- Pass `report_datetime` explicitly during tests.
- Version this dataset together with changes to business rules and test expectations.
- Do not replace synthetic values with confidential company data.

## Quality verification

The workbook was checked for:

- correct row and column counts;
- typed date and numeric values, except intentional invalid cases;
- required worksheet and headers;
- readable formatting and filters;
- visual integrity of both worksheets;
- absence of spreadsheet formula errors;
- reconciliation of the approved KPI baseline.
