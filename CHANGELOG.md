# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Cleaning Engine and controlled data normalization
- Business Rules Engine
- Traceable transformations and expanded automated coverage

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
