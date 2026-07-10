# ADR-001: Adopt pragmatic hexagonal architecture

- **Status:** Accepted
- **Decision date:** 2026-07-10
- **Scope:** Ticket Reporting MVP

## Context

The application must initially process Excel workbooks but is expected to evolve toward APIs, automation, and AI-assisted reporting. Coupling ticket rules directly to Pandas Excel operations would make unit testing and future integrations unnecessarily difficult.

A simple script would be fast initially but would not demonstrate the modularity, maintainability, and testability expected from the target enterprise portfolio.

A fully distributed enterprise architecture would be disproportionate for this MVP.

## Decision

Use a pragmatic hexagonal architecture with:

- domain rules and KPIs at the core;
- an application use case for orchestration;
- reader and writer ports;
- Excel-specific infrastructure adapters;
- a command-line inbound interface;
- a Python `src` project layout.

Pandas may be used inside domain services for deterministic, vectorized transformations. Excel-specific behavior must remain in infrastructure adapters.

## Consequences

### Positive

- business rules can be unit-tested without files;
- Excel can later be complemented by REST or database adapters;
- Flask and AI integrations will not require rewriting SLA logic;
- module responsibilities are explicit;
- the repository demonstrates enterprise engineering practices.

### Trade-offs

- more files and concepts than a single Python script;
- ports add modest upfront design work;
- contributors must respect dependency-direction rules.

## Rejected alternatives

### Single-script pipeline

Rejected because loading, validation, KPI calculation, and export would become tightly coupled and difficult to test independently.

### Technology-based modules only

A structure such as `loader.py`, `pandas_processing.py`, and `excel_export.py` was not sufficient because it organized the system mainly by technology rather than business responsibility.

### Full microservices architecture

Rejected because the MVP has one local processing use case and no independent deployment or scaling requirements.
