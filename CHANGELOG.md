# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### In development

- v0.3.0 — Cleaning and Business Rules Engine
- Ticket Cleaning foundation with deterministic datetime and SLA-target normalization
- `BR-001` lifecycle classification into `BACKLOG` and `COMPLETED`
- `BR-002` deterministic `elapsed_hours` calculation for active and completed tickets
- `BR-003` SLA classification into `MET` and `BREACHED`, including the exact-threshold boundary
- Fractional-hour preservation without premature rounding
- Fail-fast protection for unsupported statuses reaching the Business Rules Engine

### Quality

- Source DataFrames remain unchanged during cleaning, lifecycle classification, elapsed-hours calculation, and SLA classification
- Automated suite expanded from 57 to 83 passing tests
- BR-003 coverage includes fractional-hour boundaries, zero duration, empty input, determinism, and source/index preservation
- Synthetic pipeline verification confirms 20 valid and 10 rejected records, with 10 SLA met and 10 SLA breached
- Existing Excel Loader and Validation Engine behavior remains regression-safe

### Fixed

- Empty datasets retain an object-typed validation-error column, preventing the Pandas string accessor from failing on an inferred floating-point column
- Empty and all-rejected datasets are covered through the cleaning and business-rule pipeline

### Remaining before release

- Publish the verified empty-input correction and verification documentation
- Merge the approved development branch into `main` and tag `v0.3.0`

## [0.2.0] - 2026-07-28

### Added

- Deterministic Ticket Validation Engine
- `ValidationResult` contract separating valid and rejected records
- Twelve explicit validation rules (`VAL-001`–`VAL-012`) covering required identifiers, duplicate tickets, datetime validity and ordering, supported statuses and priorities, status/closure consistency, assigned teams, and positive numeric SLA targets
- Collection of all applicable validation errors on rejected records
- Automated tests for normal, invalid, and exact-boundary behavior
- Repository workflow and architecture guidance in `AGENTS.md`

### Changed

- Expanded the automated suite from 4 to 57 tests
- Updated project documentation to identify the Validation Engine as the current completed release
- Advanced the development focus to v0.3.0 — Cleaning and Business Rules Engine

### Quality

- Source DataFrames remain unchanged during validation
- Existing Excel Loader behavior remains covered and regression-safe
- Acceptance dataset verified at 30 total records: 20 valid and 10 rejected
- Designed-invalid records produce the expected `VAL-001`–`VAL-012` reason sets
- Full automated suite passed before release

## [0.1.0] - 2026-07-12

### Added

- Enterprise-oriented repository foundation
- Approved MVP business requirements for IT ticket reporting
- Pragmatic hexagonal architecture and ADR-001
- Verified 30-record synthetic IT ticket dataset
- Dataset specification with expected KPI and SLA baseline
- Controlled Excel Loader for the `Tickets` worksheet
- Required-column validation
- Explicit errors for missing files, worksheets, and columns
- Four automated pytest tests for the Excel Loader
- Initial dependency, source, test, configuration, data, and reporting structure
- Flask REST API and AI Reporting Agent included in the planned platform evolution

### Quality

- Synthetic data only; no confidential company information
- Deterministic calculations remain separated from future AI commentary
- Business logic is designed to remain independent from future Flask delivery interfaces

[Unreleased]: https://github.com/marcocica93/enterprise-excel-reporting-ai-platform/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/marcocica93/enterprise-excel-reporting-ai-platform/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/marcocica93/enterprise-excel-reporting-ai-platform/releases/tag/v0.1.0
