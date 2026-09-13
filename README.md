# Lab 1 — Requirements Engineering & UML Use-Case Modelling

**Problem Statement #26 — Peer-to-Peer Carpooling & Expense Splitter**

A commuter ridesharing portal that matches drivers and passengers with overlapping daily routes, enforces detour tolerance thresholds, and calculates automated fuel cost share splits.

**Actors:** Rider Commuter, Driver Host, Payment Gateway (external system)

## Repo Contents

| File | Description |
|---|---|
| `SELab1_Report.docx` | Combined report: problem overview, requirements table, use-case diagram, and use-case flow in one document |
| `Lab1_Requirements_Table.docx` | Requirements table — 5 FRs (FR-001–FR-005) and 2 NFRs (NFR-001–NFR-002), each with priority, measurable acceptance criteria, and rationale |
| `Lab1_UseCase_Diagram.pdf` | UML use-case diagram with 3 actors, 7 use cases, one `<<include>>` relation (Book Ride → Calculate Fuel Cost Split), and one `<<extend>>` relation (Apply Promo Code → Make Payment) |
| `Lab1_UseCase_Flow.docx` / `use_case_flow.pdf` | Use-case flow for UC-03: Book Ride — main success scenario plus two alternate flows (driver declines request, payment declined) |

## Requirements Summary

- **FR-001** (given): Route compatibility within 1.5 km detour tolerance
- **FR-002**: Driver Host trip listing creation
- **FR-003**: Rider Commuter route search
- **FR-004**: Automated fuel cost split calculation
- **FR-005**: Post-trip rating between Rider and Driver
- **NFR-001** (given): Encrypted storage of sensitive user data
- **NFR-002**: Search results returned within 3 seconds under normal load

## Status

- [x] Requirements table drafted
- [ ] Peer critique completed (swap with classmate, fill Comments column)
- [x] Use-case diagram created
- [x] Use-case flow documented
- [x] Files exported to PDF/Word
