# Codex Repository Instructions

## Project mission

Build the Enterprise Excel Reporting & AI Platform as a professional,
portfolio-ready Python application. Preserve deterministic business logic,
auditability, modularity, testability, and clear traceability from approved
requirements to implementation.

## Required workflow

Before changing code:

1. Read the relevant business requirement, issue, and architecture document.
2. State the input, output, business rule, boundary cases, and acceptance criteria.
3. Inspect the current implementation and tests.
4. Propose the smallest coherent change and identify the files it will touch.

During implementation:

1. Add or update an automated test before the production change when practical.
2. Implement only the approved rule; do not invent data, columns, KPIs, or policy.
3. Keep business logic independent from Excel formatting, Flask, and AI services.
4. Do not mutate source DataFrames unless the public contract explicitly requires it.
5. Prefer readable Pandas operations; use NumPy only when it adds a concrete benefit.
6. Preserve public interfaces unless a requirement explicitly authorizes a change.

Before handoff:

1. Run the focused tests and then the full test suite.
2. Run `git diff --check` and inspect the complete diff.
3. Report changed files, verified behavior, test results, assumptions, and residual risks.
4. Do not commit, push, merge, tag, or close an issue without Marco's approval.

## Project commands

From the repository root, with the virtual environment activated:

```text
python -m pip install -r requirements.txt
python -m pytest
python -m pytest tests/test_ticket_validator.py
git diff --check
git status
```

## Architecture constraints

- Business rules belong in the application core and must be testable with in-memory
  DataFrames.
- Structural workbook failures stop processing; record-level validation failures
  reject only the affected records.
- Rejected records must retain every applicable validation reason and must never
  contribute to business KPIs.
- Identical input and `report_datetime` values must produce identical results.
- Flask is introduced only after the Python/Pandas pipeline is stable and remains an
  inbound adapter rather than a home for business logic.
- AI may interpret validated outputs later, but must never calculate or invent KPIs.

## Scope and quality rules

- Keep increments small and reviewable, normally one approved validation rule at a
  time during Sprint 2.
- Avoid unrelated refactoring in feature changes.
- Use synthetic or anonymized data only.
- Update documentation when a public contract, business rule, workflow, or release
  state changes.
- Treat the Definition of Done as: implementation complete, tests green,
  documentation aligned, diff reviewed, and repository state traceable.
