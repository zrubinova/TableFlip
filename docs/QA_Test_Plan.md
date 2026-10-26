# TableFlip — QA Test Plan

**Project:** TableFlip — Restaurant Table Reservation System   
**Project Phase:** Week 7  
**Status:** Draft

## 1. Objective

The objective of Quality Assurance is to verify that the TableFlip reservation system meets the documented business requirements and operates reliably.

AI tools will assist in reviewing requirements, generating test cases, creating automated tests, analyzing code, and identifying potential defects.

The primary QA focus is the table allocation engine, ensuring that no table is double-booked and every confirmed reservation respects table capacity.

## 2. Scope of Testing

The following features will be verified against the project requirements:

- **Online reservations:** Guests can request reservations at any time without staff assistance.
- **Table allocation:** Each confirmed reservation receives one table with sufficient capacity.
- **Double-booking prevention:** No table is assigned to overlapping reservations.
- **Booking confirmation:** Guests immediately receive the confirmed date, time, and table number.
- **Unavailable tables:** Requests are rejected with a clear message when no suitable table is available.
- **Cancellation:** Cancelled reservations release their allocated tables.
- **Staff dashboard:** Staff can view current reservations and table availability, with changes appearing without manual refresh.
- **No-show handling:** Staff can release tables when guests have not arrived 15 minutes after their scheduled booking time.
- **Capacity and duration:** The restaurant supports a maximum of 50 seats, and reservations cannot exceed 120 minutes.
- **Staff-created reservations:** Phone and walk-in reservations will be tested if confirmed within the implementation scope.

## 3. AI-Assisted Testing Approach

AI will be used to support the QA process throughout development and testing.

### 3.1 AI-Assisted Requirements Analysis

AI will analyze the project requirements to identify missing acceptance criteria, contradictions, and potential edge cases.

### 3.2 AI-Generated Test Cases

AI will generate test scenarios based on the documented requirements, including normal, invalid, boundary, and simultaneous reservation scenarios.

Each generated test case will be reviewed against the requirements before execution.

### 3.3 AI-Assisted Automated Testing

AI will help create automated test scripts using testing frameworks compatible with the application's technology stack.

The scripts will verify reservation creation, allocation, cancellation, capacity limits, and other implemented features.

### 3.4 AI-Assisted Code Review

AI will analyze available source code to identify potential logical errors, particularly in table allocation, overlapping time calculations, and concurrent reservation handling.

Potential defects identified by AI will be verified before being reported as confirmed bugs.

### 3.5 AI-Assisted Regression Testing

AI will help update and rerun automated tests after changes or bug fixes to detect unintended behavior.

### 3.6 AI-Assisted Defect Analysis

AI will help analyze failed test results, investigate possible causes, and prepare structured bug reports.

The QA responsible will review findings and confirm actual defects.

## 4. Critical Test Scenarios

The following scenarios have the highest priority:

1. Two guests attempt to reserve the same table for overlapping periods.
2. Two guests submit simultaneous reservations for the last available table.
3. A reservation ends at 20:00 and another begins at 20:00.
4. A group requests a table smaller than its party size.
5. The restaurant reaches its maximum capacity of 50 seats.
6. A guest requests a reservation longer than 120 minutes.
7. A guest cancels a reservation, releasing its table.
8. A staff member releases a table after the 15-minute no-show threshold.
9. A guest requests a reservation when no suitable table is available.
10. A reservation is created, changed, or cancelled and the staff dashboard updates correctly.

## 5. Testing Process

1. Review project requirements using AI assistance.
2. Generate test cases and expected results.
3. Review AI-generated tests for correctness.
4. Prepare automated tests using AI assistance.
5. Execute tests when the application becomes available.
6. Compare actual results with documented requirements.
7. Investigate failed tests and verify suspected defects.
8. Report confirmed bugs through GitHub Issues or the agreed defect log.
9. Retest fixed defects and run regression tests.
10. Document final testing results.

## 6. Test Environment and Tools

- **GitHub:** Repository management, issue tracking, and QA documentation.
- **AI assistant:** Requirements analysis, test generation, code review, and defect analysis.
- **Automated testing framework:** To be selected according to the implemented technology stack.
- **Test environment:** To be provided by the development team.

Only free tools will be used, consistent with the project charter.

## 7. Entry Criteria

Testing can begin when:

- The relevant feature is implemented.
- The test environment is available.
- Acceptance criteria are defined.
- Required test data is prepared.
- AI-generated test scripts have been reviewed.

## 8. Exit Criteria

QA testing will be considered complete when:

- All agreed critical test cases have been executed.
- No double-booking or undersized-table allocation occurs in executed tests.
- No unresolved critical defects remain.
- Reported critical defects have been fixed and successfully retested.
- Test results and known limitations are documented.

## 9. QA Deliverables

- QA Test Plan
- AI-Assisted Test Cases
- Automated Test Scripts
- Defect Reports
- Test Execution Results
- Final QA Summary Report
- AI Usage Log

## 10. Open Decisions and Requirement Clarifications

The following items require confirmation:

- **Default reservation duration:** The maximum is 120 minutes, but the risk register records the default duration as undecided.
- **Offline booking recovery:** The requirements include re-entering bookings after an outage, but the project charter excludes this functionality.
- **Staff-created bookings:** The requirements include phone and walk-in reservations, while the charter's implementation scope needs clarification.
- **Testing framework:** Selection depends on the technology stack implemented by the developers.
- **Test environment:** Access and configuration must be confirmed with the development team.

## 11. AI Usage and Verification

AI-generated test cases, code, and defect analyses will be reviewed before acceptance.

AI-generated content will not be treated as proof that a feature works. Test results must come from actual execution against the application.

Significant AI assistance will be documented in the project's AI usage log, consistent with the risk register.

## 12. QA Schedule

| Week | QA Activity |
|---|---|
| 7 | Review requirements, prepare QA plan and allocation edge cases |
| 8–9 | Generate and review test cases, prepare automated tests |
| 10 | Execute tests, document defects and retest fixes |
| 11 | Verify critical defects are resolved |
| 12–13 | Support final verification and project handover |
