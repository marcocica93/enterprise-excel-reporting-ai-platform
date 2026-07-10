# MVP Business Requirements

## Document status

- **Version:** 0.1
- **Status:** Draft — core business rules confirmed
- **Use case:** IT Ticket Backlog & SLA Reporting

## 1. Business problem

IT Operations teams receive ticket data through Excel workbooks. Manual validation and reporting can be slow, inconsistent, difficult to audit, and dependent on individual knowledge.

The MVP will transform a ticket workbook into a validated, deterministic, and auditable Excel report.

## 2. Primary user

**IT Operations Manager**

The report must support the following decisions:

- identify the current operational backlog;
- identify tickets that breached SLA;
- compare workload and performance across teams;
- identify critical priorities;
- detect and isolate data-quality problems.

## 3. MVP scope

The MVP must:

1. load an Excel workbook;
2. verify the required worksheet and columns;
3. validate individual ticket records;
4. separate valid and rejected records;
5. classify backlog and completed tickets;
6. calculate SLA elapsed time in calendar hours;
7. calculate deterministic KPIs;
8. export a structured Excel report;
9. record basic processing audit information.

## 4. Input contract

### Workbook

- Supported format: `.xlsx`
- Required worksheet: `Tickets`
- Processing timestamp: explicit `report_datetime`

### Required columns

| Column | Description | Requirement |
|---|---|---|
| `ticket_id` | Unique ticket identifier | Required and unique |
| `created_at` | Ticket creation timestamp | Required valid datetime |
| `closed_at` | Completion timestamp | Conditional |
| `status` | Ticket lifecycle status | Required controlled value |
| `priority` | Business priority | Required controlled value |
| `assigned_team` | Responsible operational team | Required |
| `sla_target_hours` | Maximum allowed resolution time | Required positive number |

### Controlled values

Allowed statuses:

- `OPEN`
- `IN_PROGRESS`
- `RESOLVED`
- `CLOSED`

Allowed priorities:

- `P1`
- `P2`
- `P3`
- `P4`

## 5. Ticket classification rules

| Status | Included in backlog | Completed | `closed_at` rule |
|---|---:|---:|---|
| `OPEN` | Yes | No | Must be empty |
| `IN_PROGRESS` | Yes | No | Must be empty |
| `RESOLVED` | No | Yes | Required |
| `CLOSED` | No | Yes | Required |

Backlog formula:

```text
backlog = OPEN + IN_PROGRESS
```

## 6. SLA rules

The MVP uses calendar hours, 24 hours per day and 7 days per week. Business calendars, weekends, public holidays, and team-specific working schedules are out of scope.

For completed tickets:

```text
elapsed_hours = closed_at - created_at
```

For backlog tickets:

```text
elapsed_hours = report_datetime - created_at
```

SLA classification:

```text
SLA met:      elapsed_hours <= sla_target_hours
SLA breached: elapsed_hours > sla_target_hours
```

## 7. Record validation rules

A record must be rejected when one or more of the following conditions apply:

- `ticket_id` is missing;
- `ticket_id` is duplicated;
- `created_at` is missing or invalid;
- `created_at` is later than `report_datetime`;
- `closed_at` is earlier than `created_at`;
- `status` is not an allowed value;
- `priority` is not an allowed value;
- `assigned_team` is missing;
- `sla_target_hours` is missing, non-numeric, zero, or negative;
- an active ticket has a populated `closed_at`;
- a completed ticket has an empty `closed_at`.

A rejected record:

- must be excluded from all business KPIs;
- must be written to `Rejected_Records`;
- must contain a `rejection_reason`;
- may contain multiple rejection reasons.

## 8. Initial KPIs

- total valid tickets;
- current backlog;
- completed tickets;
- SLA breached tickets;
- SLA compliance rate;
- average resolution time for completed tickets;
- backlog by assigned team;
- backlog by priority;
- rejected record count;
- rejected record rate.

## 9. Output contract

The generated workbook will contain:

- `Executive_Summary`
- `Valid_Tickets`
- `Rejected_Records`
- `KPI_By_Team`
- `KPI_By_Priority`
- `Run_Audit`

## 10. Audit requirements

The processing run must record at least:

- input filename;
- `report_datetime`;
- processing timestamp;
- total input rows;
- valid row count;
- rejected row count;
- output filename;
- processing result.

## 11. Out of scope for the MVP

- business-hours calendars;
- public-holiday calendars;
- team-specific SLA calendars;
- databases;
- Flask API;
- authentication;
- AI-generated management commentary;
- real or confidential company data.

## 12. Pending approval

The definitive acceptance criteria and sample dataset specification must be approved before implementation begins.
