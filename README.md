# Enterprise Excel Reporting & AI Platform

[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](CHANGELOG.md)

An enterprise-oriented Python platform for validating operational Excel data, applying deterministic business rules, calculating KPIs, producing auditable reports, and later generating AI-assisted management commentary.

## Project purpose

Many business teams manage operational data through Excel workbooks. Manual validation and reporting can be slow, inconsistent, difficult to audit, and dependent on individual knowledge.

This project progressively transforms that workflow into a modular, testable, and deployable Python application.

## Project context

This repository is both a working software product and a professional portfolio project. It demonstrates the progressive transition from Business Analysis toward Data Analysis, AI Automation, and Applied AI Engineering through an enterprise-oriented delivery lifecycle.

Each increment connects a learning objective to a production-relevant component. Python, Pandas, NumPy, Excel automation, testing, Flask, REST APIs, JSON, and AI workflows are introduced only when the previous foundations are sufficiently stable.

The objective is not merely to produce code, but to demonstrate:

- translation of business requirements into technical specifications;
- explicit and testable business rules;
- data-quality and auditability controls;
- modular software architecture;
- automated testing and code review;
- versioned, documented, and traceable delivery;
- responsible use of AI throughout the development lifecycle.

## MVP business objective

Build an MVP that can:

1. load an operational Excel workbook;
2. validate its structure and required data;
3. separate valid and rejected records;
4. apply explicit business rules;
5. calculate deterministic KPIs;
6. export a structured Excel report.

The approved initial use case is IT ticket management, backlog monitoring, SLA validation, and operational KPI reporting.

## Current release

**v0.2.0 — Validation Engine and data-quality controls**

Completed capabilities:

- controlled Excel loading from the `Tickets` worksheet;
- required-column and workbook-structure validation;
- deterministic record-level Ticket Validation Engine;
- separation of valid and rejected records through the `ValidationResult` contract;
- collection of all applicable validation errors on rejected records;
- twelve explicit data-quality rules covering identifiers, timestamps, statuses, priorities, assigned teams, and SLA targets;
- preservation of the source DataFrame;
- automated coverage for normal, invalid, and boundary cases;
- verified synthetic acceptance dataset: 30 total records, 20 valid and 10 rejected;
- 57 automated tests covering the Excel Loader and Validation Engine.

See [CHANGELOG.md](CHANGELOG.md) for the detailed release history.

## Validation rules

| Rule | Validation |
|---|---|
| `VAL-001` | `ticket_id` is required |
| `VAL-002` | Every occurrence of a duplicated `ticket_id` is rejected |
| `VAL-003` | `created_at` must be a valid datetime |
| `VAL-004` | `created_at` must not be later than the report datetime |
| `VAL-005` | Status must be `OPEN`, `IN_PROGRESS`, `RESOLVED`, or `CLOSED` |
| `VAL-006` | Completed tickets require `closed_at` |
| `VAL-007` | Active tickets must not contain `closed_at` |
| `VAL-008` | `closed_at` must not precede `created_at` |
| `VAL-009` | `closed_at`, when present, must be a valid datetime |
| `VAL-010` | Priority must be `P1`, `P2`, `P3`, or `P4` |
| `VAL-011` | `assigned_team` is required |
| `VAL-012` | `sla_target_hours` must be present, numeric, and greater than zero |

## Current development focus

The next planned milestone is **v0.3.0 — Cleaning and Business Rules Engine**.

The next increment will focus on:

- controlled normalization of validated records;
- explicit separation between data cleaning and business rules;
- deterministic business-rule outputs;
- preservation of traceability between source and processed data;
- automated tests for transformations, boundaries, and invalid inputs;
- documentation of cleaning decisions and business assumptions.

## Planned evolution

The project will grow incrementally through the following capabilities:

- Cleaning Engine
- Business Rules Engine
- KPI Engine
- Reporting Engine
- Logging and audit
- Automated testing
- Configuration management
- Flask REST API
- AI Reporting Agent
- Deployment

## Release roadmap

| Version | Planned milestone |
|---|---|
| `0.1.0` | Foundation, synthetic dataset, and Excel Loader baseline |
| `0.2.0` | Validation Engine and data-quality controls |
| `0.3.0` | Cleaning and Business Rules Engine |
| `0.4.0` | KPI and Reporting Engine |
| `0.5.0` | Logging, configuration, and expanded testing |
| `0.6.0` | Flask REST API |
| `0.7.0` | AI Reporting Agent |
| `0.8.0`–`0.9.0` | Hardening, security, and deployment preparation |
| `1.0.0` | Stable, documented, deployable MVP |

The roadmap is outcome-based: version numbers are assigned only when the corresponding functionality is completed and verified.

## Engineering principles

- Business requirements before code
- Deterministic calculations before AI commentary
- Clear separation of responsibilities
- Modular, readable, and testable Python
- Explicit data-quality controls
- Synthetic or anonymized sample data only
- Documentation as part of the deliverable
- Business logic independent from Flask and other delivery interfaces

## AI-assisted development approach

AI is used as an engineering copilot for planning, implementation support, code review, debugging, testing, and documentation. It does not replace ownership of requirements or technical decisions.

The development workflow keeps human responsibility over:

- business meaning and acceptance criteria;
- architecture and scope decisions;
- review of generated code;
- validation of tests and outputs;
- approval of release checkpoints.

Deterministic Python and Pandas components calculate and validate operational results. The future AI Reporting Agent will interpret only validated outputs and will never invent KPI values.

## Delivery approach

Work is organized into small, reviewable increments:

1. define the business problem;
2. specify inputs, outputs, and business rules;
3. design the solution;
4. implement the smallest useful component;
5. test and review;
6. refactor and document;
7. publish a traceable release checkpoint.

## Versioning policy

The project follows Semantic Versioning:

- **MAJOR** for incompatible architectural or API changes;
- **MINOR** for completed functionality;
- **PATCH** for backward-compatible fixes.

During active development, the project remains in the `0.x.x` series. Version `1.0.0` will identify the first stable and deployable MVP.

## Author

Marco Cicatiello — Business Analyst transitioning toward Data Analysis, AI Automation, and Applied AI Engineering.
