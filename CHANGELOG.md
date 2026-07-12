# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Validation Engine and record-level data-quality controls
- Structured rejection reasons
- Valid and rejected dataset separation

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

[Unreleased]: https://github.com/marcocica93/enterprise-excel-reporting-ai-platform/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/marcocica93/enterprise-excel-reporting-ai-platform/releases/tag/v0.1.0
