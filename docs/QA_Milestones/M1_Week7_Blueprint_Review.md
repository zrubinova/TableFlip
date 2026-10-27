# TableFlip — QA Milestone M1: Week 7 Solution Blueprint Review

**Project:** TableFlip — Restaurant Table Reservation System  
**Milestone:** M1 — Week 7  
**Date:** 27 October 2026  
**Phase:** Pre-development / Solution Design  
**Status:** QA Design Review

## 1. Milestone Objective

Evaluate the Week 7 Developer Solution Blueprint from a Quality Assurance perspective, focusing on testability, reservation correctness, data integrity, failure handling and alignment with Functional Requirements Version 2.

This milestone supplements the original QA Test Plan and records the QA analysis of the proposed technical solution.

## 2. Documents Reviewed

- Original QA Test Plan
- Functional Requirements Version 2 (24 October 2026)
- Developer Solution Blueprint (27 October 2026)
- Project Risk Register

## 3. Developer Blueprint — QA Perspective

The proposed solution consists of:

| Component | Technology | QA Focus |
|---|---|---|
| User interface | Streamlit | Input validation and displayed results |
| Booking logic | Python | Allocation rules and booking state transitions |
| Database | SQLite | Transaction safety and data persistence |
| Database access | Python `sqlite3` | Correct reads, writes and rollback |
| Configuration | Local settings file | Table capacities, opening hours and durations |
| Staff interface | Streamlit with demo password | Restricted access to booking information |

The application is a local prototype. Testing will focus on the documented functionality and its interfaces rather than production deployment.

## 4. Critical Component — QA Analysis

The table allocation and saving process is the highest-priority testing area.

### 4.1 Allocation Correctness

QA will verify that:

1. Each confirmed reservation receives exactly one table.
2. The assigned table has sufficient capacity for the party.
3. The smallest suitable available table is selected.
4. When suitable tables have equal capacity, the lowest table number is selected.
5. Existing Confirmed reservations block overlapping time intervals.
6. Cancelled and No-show reservations do not block availability.
7. Adjacent bookings are permitted when one reservation ends exactly as another begins.
8. A party cannot be allocated across multiple smaller tables.

### 4.2 Database Integrity

QA will verify that:

- Availability checking and reservation saving occur within a protected transaction.
- Two concurrent requests cannot confirm overlapping reservations on the same table.
- Failed database operations do not leave partially saved reservations.
- Booking confirmation is displayed only after successful saving.
- Reservation records persist after application restart.

### 4.3 Time and Capacity Boundaries

QA test design will use the documented configuration:

- T1–T4: 2 seats each.
- T5–T8: 4 seats each.
- T9–T11: 6 seats each.
- T12: 8 seats.
- Total: 12 tables and 50 seats.
- Opening hours: Tuesday–Sunday, 11:00–23:00.
- Reservation durations: 60, 90 or 120 minutes.
- Reservation start intervals: 15 minutes.

Boundary tests will cover exact start/end equality, invalid durations, unsuitable capacities, opening-hour limits and no-show eligibility.

## 5. QA Risk Assessment

| Risk ID | Potential Failure | Priority | Planned Verification |
|---|---|---|---|
| M1-R01 | Concurrent requests create overlapping confirmed bookings. | Critical | Simultaneous booking integration tests |
| M1-R02 | Incorrect overlap logic rejects valid bookings or allows conflicts. | Critical | Time-boundary and overlap tests |
| M1-R03 | The system allocates an undersized table or ignores selection priority. | Critical | Capacity and allocation-order tests |
| M1-R04 | A failed database operation leaves partial data or displays a false confirmation. | High | Failure simulation and rollback tests |
| M1-R05 | Reservations disappear after restarting the application. | High | Persistence tests |
| M1-R06 | Staff booking information is displayed before password entry. | High | Staff access tests |
| M1-R07 | Cancellation or no-show fails to release a table. | High | Reservation state-transition tests |

These are design-stage risks requiring verification, not confirmed defects.

## 6. Functional Requirements — QA Coverage

| Requirement | Verification Focus | Planned Test Level |
|---|---|---|
| FR1 — Booking Form | Required fields, valid dates, party sizes, opening hours and durations | Unit / System |
| FR2 — Table Allocation | Capacity, selection priority, overlap prevention and adjacent bookings | Unit / Integration |
| FR3 — Safe Saving | Transaction safety, concurrent requests and persistence | Integration |
| FR4 — Confirmation / Refusal | Correct confirmation, refusal and technical-error handling | Integration / System |
| FR5 — Staff Access | Password requirement and booking-data visibility | System |
| FR6 — Staff View | Reservation ordering, statuses and availability at selected date/time | System |
| FR7 — Cancellation / No-show | Status changes, release of tables and 15-minute threshold | Unit / Integration / System |

## 7. Differences Affecting the Original QA Test Plan

The revised requirements and developer blueprint clarify the expected behavior of several features:

- **Staff view:** Manual refresh is acceptable; live cross-device updates are not required.
- **Cancellation:** Staff cancel reservations; guest self-cancellation is not included.
- **Staff-created reservations:** Phone and walk-in bookings use the shared form.
- **Duration:** Allowed stays are 60, 90 and 120 minutes, with a default of 120 minutes.
- **Database:** SQLite transaction safety and persistence require explicit verification.
- **Staff access:** A demo password is used; production authentication is not part of the prototype.
- **Offline operation:** Paper bookings are an external fallback and are not automatically re-entered.

These differences will guide future test-case design and prevent testing against outdated expectations.

## 8. QA Questions for Implementation Verification

The following technical details should be established before automated testing:

1. What transaction strategy protects SQLite availability checks and reservation insertion against concurrent requests?
2. How are failed database writes rolled back?
3. Which Python functions expose validation, allocation, saving and status updates for isolated testing?
4. How are date/time values represented and compared?
5. How does the Streamlit interface prevent staff booking data from appearing before password entry?
6. Can automated tests use a separate SQLite database and configuration file?

## 9. QA Conclusion and Next Phase

The Week 7 blueprint identifies the major application components, allocation rules, data model and expected failure behavior.

From a QA perspective, the most important verification areas are **allocation correctness, concurrency protection, database integrity, time boundaries and reservation state transitions**.

This milestone establishes the technical basis for the next QA phase: detailed test-case design, requirement traceability and preparation of automated tests.

**Execution status:** No application tests executed at this stage.

## 10. AI Usage Disclosure

AI assistance was used to structure the technical review, identify potential failure scenarios and organize verification objectives. The analysis is based on the supplied project requirements and developer blueprint. AI-generated observations are not considered evidence of implementation defects.
