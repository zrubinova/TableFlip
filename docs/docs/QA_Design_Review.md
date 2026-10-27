# TableFlip — QA Design Review

**Project:** TableFlip  
**Phase:** Week 7 — Pre-development  
**Date:** 27 October 2026  
**Status:** Draft — pending team review

## 1. Purpose

Review the proposed solution architecture before implementation to identify quality risks, verify alignment with the functional requirements, and define the evidence required during testing.

## 2. Reference Documents

- Functional Requirements Version 2 (`zuzka-func-requirements` branch)
- TableFlip Week 7 Solution Blueprint, updated 27 October 2026
- Project Charter
- Business Requirements
- Risk Register

The functional requirements Version 2 is the working QA baseline; its formal team approval must be confirmed.

## 3. Architecture Under Review

- **User interface:** Streamlit
- **Business logic:** Python
- **Database:** SQLite
- **Configuration:** Local settings file
- **Deployment:** Local demonstration application
- **Interfaces:** Browser to Streamlit, direct Python function calls, SQLite via `sqlite3`

The prototype covers FR1–FR7.

## 4. Critical Component — Table Allocation

The allocation process must:

1. Validate the reservation request.
2. Find tables with sufficient capacity.
3. Exclude tables with overlapping confirmed reservations.
4. Select the smallest suitable available table, using the lowest table ID for ties.
5. Save the reservation safely before displaying confirmation.

### Required invariants

- No two confirmed reservations overlap on the same table.
- No confirmed reservation is assigned to an undersized table.
- A reservation ending at 20:00 does not conflict with one starting at 20:00.
- Cancelled and no-show reservations do not block tables.
- A failed database transaction never produces a successful confirmation.

## 5. QA Review Findings

| ID | Area | Finding / Risk | Priority | Proposed Action | Status |
|---|---|---|---|---|---|
| QA-DR-01 | SQLite concurrency | The blueprint requires protected saving but does not specify the transaction strategy. | Critical | Developers explain how concurrent check-and-insert operations are serialized. | Open |
| QA-DR-02 | Error handling | Database failures must not leave partial reservations or produce false confirmations. | High | Design rollback and failure-injection tests. | Open |
| QA-DR-03 | Access control | Staff booking data must not be accessible before entering the demo password. | High | Define and test access behavior across independent sessions. | Open |
| QA-DR-04 | Time boundaries | Start/end comparisons, quarter-hour handling and no-show timing must be consistent. | High | Confirm time representation and rounding rules. | Open |
| QA-DR-05 | Persistence | Bookings must survive application restart. | High | Verify persistence using a temporary SQLite database and restart test. | Open |
| QA-DR-06 | Requirements baseline | Functional Requirements v2 is marked pending team approval. | High | Confirm approval and record any accepted deviations from business requirements. | Open |

These are pre-development review findings, not confirmed software defects.

## 6. Planned Verification

| Component | Proposed Test Type |
|---|---|
| Python validation | Unit tests |
| Table allocation | Unit and boundary tests |
| SQLite saving | Integration and concurrency tests |
| Streamlit booking form | UI/system tests |
| Staff access | Access-control tests |
| Staff booking view | Functional tests |
| Cancellation and no-show | State-transition tests |

**Proposed tools:** pytest, temporary SQLite databases and Streamlit AppTest, subject to implementation structure.

## 7. Questions for Developers

1. Which Python function will perform table allocation?
2. How will SQLite transactions prevent simultaneous double-bookings?
3. How will database failures and rollbacks be handled?
4. How will Streamlit guest and staff sessions be separated?
5. How will tests control the current time for boundary scenarios?
6. Will configuration and database paths be injectable for isolated tests?

## 8. QA Status

**Requirements review:** In progress  
**Architecture review:** In progress  
**Test design:** Draft  
**Automated test execution:** Not started  
**Defect confirmation:** Not applicable before implementation

## 9. Next Actions

- Review findings with the business analyst and developers.
- Confirm the approved functional requirements baseline.
- Update the QA Test Plan and Test Cases.
- Complete the requirements traceability matrix.
- Prepare test fixtures and future automated testing interfaces.

## 10. AI Assistance Disclosure

AI assistance was used to help structure this design review and identify potential QA risks. The findings require manual verification against the project documents and review with the project team.
