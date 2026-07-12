# Enterprise Excel Reporting & AI Platform

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](CHANGELOG.md)

An enterprise-oriented Python platform for validating operational Excel data, applying deterministic business rules, calculating KPIs, producing auditable reports, and later generating AI-assisted management commentary.

## Project purpose

Many business teams manage operational data through Excel workbooks. Manual validation and reporting can be slow, inconsistent, difficult to audit, and dependent on individual knowledge.

This project progressively transforms that workflow into a modular, testable, and deployable Python application.

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

**v0.1.0 — Project foundation and Excel Loader baseline**

Completed capabilities:

- approved MVP business requirements;
- pragmatic hexagonal architecture and ADR-001;
- verified 30-record synthetic IT ticket dataset;
- controlled Excel loading from the `Tickets` worksheet;
- required-column validation;
- explicit errors for missing files, worksheets, and columns;
- four automated tests covering the loader foundation;
- initial dependency and repository structure.

See [CHANGELOG.md](CHANGELOG.md) for release history.

## Planned evolution

The project will grow incrementally through the following capabilities:

- Validation Engine
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

Marco — Business Analyst transitioning toward Data Analysis, AI Automation, and Applied AI Engineering.
