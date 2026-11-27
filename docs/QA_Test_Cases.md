# TableFlip — QA Test Cases

**Project:** TableFlip  
**Phase:** Week 7  
**Status:** Draft — Not Executed

## 1. Objective

This document defines test cases for verifying the TableFlip restaurant reservation system against its documented requirements.

AI assistance is used to generate and review test scenarios. Actual test results will be recorded once the application is available for testing.

## 2. Reservation and Table Allocation Test Cases

### TC-001: Successful Table Reservation

**Priority:** High  
**Precondition:** A suitable table is available.

**Test Steps:**
1. Open the reservation interface.
2. Select a date and time.
3. Enter a party size of 2.
4. Submit the reservation.

**Expected Result:** The reservation is confirmed and displays the date, time, and allocated table number.

**Status:** Not Executed

### TC-002: Double-Booking Prevention

**Priority:** Critical  
**Precondition:** A table is already reserved from 18:00 to 20:00, and no alternative suitable table is available.

**Test Steps:**
1. Create a reservation for 18:00–20:00.
2. Attempt another reservation for 19:00–20:00.

**Expected Result:** The system must not allocate the occupied table to the second reservation. If no suitable table is available, the request must be rejected with a clear message.

**Status:** Not Executed

### TC-003: Table Capacity Validation

**Priority:** Critical  
**Precondition:** A 4-seat table is available.

**Test Steps:**
1. Request a reservation for 5 guests.
2. Submit the reservation.

**Expected Result:** The system must not assign the 4-seat table. It should allocate a larger suitable table if available, or reject the request.

**Status:** Not Executed

### TC-004: No Available Tables

**Priority:** High  
**Precondition:** All suitable tables are occupied during the requested period.

**Test Steps:**
1. Select a fully booked time slot.
2. Enter a valid party size.
3. Submit the reservation.

**Expected Result:** The reservation is rejected immediately with a clear message.

**Status:** Not Executed

### TC-005: Maximum Reservation Duration

**Priority:** High  
**Precondition:** The reservation system is accessible.

**Test Steps:**
1. Request a reservation lasting 121 minutes.
2. Submit the reservation.

**Expected Result:** The system rejects the reservation because it exceeds the 120-minute maximum.

**Status:** Not Executed

### TC-006: Reservation Cancellation

**Priority:** High  
**Precondition:** An existing confirmed reservation has an allocated table.

**Test Steps:**
1. Open the existing reservation.
2. Cancel the reservation.
3. Check table availability for the cancelled reservation period.

**Expected Result:** The reservation is cancelled and the allocated table becomes available again.

**Status:** Not Executed

### TC-007: Consecutive Reservations

**Priority:** High  
**Precondition:** A table is reserved from 18:00 to 20:00.

**Test Steps:**
1. Create a reservation ending at 20:00.
2. Attempt another reservation starting at 20:00.

**Expected Result:** The second reservation can use the same table if all other booking conditions are satisfied.

**Status:** Not Executed

### TC-008: Simultaneous Booking Requests

**Priority:** Critical  
**Precondition:** Only one suitable table is available.

**Test Steps:**
1. Prepare two reservation requests for the same time and party size.
2. Submit both requests simultaneously.
3. Check the resulting reservations.

**Expected Result:** Only one request may reserve the remaining table. No double booking occurs.

**Status:** Not Executed

## 3. Test Execution Summary

| Status | Count |
|---|---:|
| Total test cases | 8 |
| Passed | 0 |
| Failed | 0 |
| Blocked | 0 |
| Not Executed | 8 |

## 4. AI Usage

AI was used to assist in preparing test scenarios, test steps, and expected results based on the TableFlip requirements.

All test cases require review before execution. AI-generated scenarios do not represent actual test results.
----------------------------------------------------------------------------

# TableFlip — QA Test Cases

**Project:** TableFlip  
**Phase:** M2 — Week 8  
**Status:** Draft — Not Executed

## 1. Objective

Verify FR1–FR7 through structured test cases covering booking, allocation, saving, staff access and reservation statuses.

Expected results describe required behaviour. They are not actual test results.

## 2. Shared Test Setup

| Item | Configuration |
|---|---|
| Database | Isolated test database; reset between independent scenarios |
| Test date | D = a future Tuesday |
| Tables | T1–T4: 2 seats; T5–T8: 4 seats; T9–T11: 6 seats; T12: 8 seats |
| Opening hours | Tuesday–Sunday, 11:00–23:00 |
| Start intervals | Every 15 minutes |
| Durations | 60, 90 or 120 minutes; default 120 |
| Blocking status | Only Confirmed reservations block availability |
| Staff actions | Require authentication |
| Staff updates | Manual refresh is acceptable |

Unless stated otherwise, use valid required fields and available tables. Run each data variant independently.

## 3. Test Cases

**All cases below are Draft — Not Executed.**

| ID | Test / FR | Priority | Preconditions | Test Data | Steps | Expected Results |
|---|---|---|---|---|---|---|
| TC-001 | Successful reservation — FR1–FR4 | High | All tables available | D, 18:00, 2 guests, 120 min | 1. Complete form. 2. Submit. 3. Inspect confirmation and database. | One Confirmed booking saved for T1, 18:00–20:00. Correct date, time and table displayed only after saving. |
| TC-002 | Overlap prevention — FR2, FR4 | Critical | T12 booked on D, 18:00–20:00 | 8 guests; intervals: 17:30–18:30, 18:00–20:00, 18:30–19:30, 19:30–20:30 | 1. Submit each overlapping request independently. 2. Inspect response and records. | Every request refused clearly. No conflicting booking saved; original unchanged. |
| TC-003 | Capacity validation — FR2 | Critical | A: T5 and T9 available. B: Only tables with ≤4 seats available | D, 18:00, 5 guests, 120 min | 1. Submit under A. 2. Reset. 3. Submit under B. | A: Assign T9. B: Refuse. Never assign an undersized table or combine smaller tables. |
| TC-004 | No available tables — FR2, FR4 | High | All tables with ≥4 seats occupied, 18:00–20:00 | D, 18:00, 4 guests, 90 min | 1. Submit request. 2. Inspect response and database. | Clear unavailability message; no confirmation or new record. |
| TC-005 | Duration validation — FR1 | High | Suitable table available | Default; 60, 90, 120, 59, 61 and 121 min | 1. Check default. 2. Submit each duration independently; use a test interface if invalid values cannot be entered in the UI. | Default is 120. Only 60, 90 and 120 accepted. Invalid durations create no booking. |
| TC-006 | Staff cancellation — FR7 | High | Authenticated staff; T12 booked on D, 18:00–20:00 | Existing booking ID; replacement for 8 guests, same interval | 1. Cancel booking. 2. Refresh. 3. Submit replacement. | Original remains recorded as Cancelled. T12 is released and can be booked again. |
| TC-007 | Adjacent bookings — FR2 | High | T12 booked on D, 18:00–20:00 | 8 guests; 17:00–18:00 and 20:00–21:00 | 1. Submit each request independently. 2. Inspect assignment. | Both requests can use T12. Exact end/start equality is not an overlap. |
| TC-008 | Concurrent requests — FR2–FR4 | Critical | T12 available; two independent connections share one database; concurrency coordination available | Two requests: D, 18:00, 8 guests, 120 min | 1. Submit concurrently at the availability/save boundary. 2. Inspect responses and committed records. | Exactly one confirms. Other request receives handled refusal or contention response. No double booking, partial writes or exposed SQLite error. |
| TC-009 | Form and time validation — FR1 | High | Controlled date; suitable tables available | Invalid: blank required fields, past date, Monday, party sizes 0/-1/2.5/9, starts 10:45 or 18:07, 22:15 + 60 min. Valid boundaries: 11:00 or 22:00 + 60 min | 1. Change one input per scenario. 2. Submit. 3. Inspect validation and database. | Invalid requests rejected without saving. Valid boundary requests accepted when available. No stay extends beyond 23:00. |
| TC-010 | Allocation priority — FR2 | Critical | A: All free. B: T1 occupied. C: T1–T4 occupied | D, 18:00, 2 guests, 60 min | 1. Submit independently under A, B and C. 2. Inspect assignment. | Assign T1, T2 and T5 respectively: smallest suitable capacity, then lowest table number. |
| TC-011 | Save failure and rollback — FR3, FR4 | High | Failure injection available; initial database state recorded | Valid booking; insert failure and failure after write but before commit | 1. Inject failure. 2. Submit. 3. Inspect response and database. 4. Remove failure and submit a fresh request. | Clear technical error; no success confirmation or partial changes. Existing data unchanged. Fresh request succeeds after recovery. |
| TC-012 | Persistence — FR3 | High | Saved Confirmed, Cancelled and No-show records; details recorded | Existing IDs, times, tables and statuses | 1. Restart using the same database. 2. Inspect records and availability. | All committed details persist. Confirmed bookings block overlap; Cancelled and No-show bookings do not. |
| TC-013 | Staff access — FR5 | High | Fresh unauthenticated session; bookings exist | No password, wrong password, valid demo password | 1. Open staff interface. 2. Try each access condition. 3. Inspect data and controls. | Booking data and staff actions hidden until valid authentication. Wrong password grants no access. |
| TC-014 | Staff view — FR6 | High | Authenticated staff; mixed dates/statuses; records inserted out of time order; sorting rule agreed | D and another date; selected times 18:00, 19:00, 20:00 | 1. Select D. 2. Check order/statuses/availability. 3. Change booking elsewhere. 4. Refresh. | Correct selected-day records, required ordering and statuses. Only Confirmed intervals block tables. Changes appear after refresh. |
| TC-015 | No-show timing — FR7 | High | Authenticated staff; T12 booked 18:00–20:00; controllable clock | 18:14:59, 18:15:00, 18:15:01; replacement: 18:15, 8 guests, 60 min | 1. Restore booking for each time. 2. Attempt No-show. 3. Check status. 4. Attempt replacement after eligible transition. | Before 18:15: refused. At/after 18:15: allowed. Status saved and remaining interval released; replacement can book T12. |
| TC-016 | Phone/walk-in bookings — FR1, FR2 | High | Authenticated staff; shared form; T12 available | Separate phone and walk-in scenarios: D, 18:00, 8 guests, 120 min | 1. Create staff booking. 2. Refresh. 3. Attempt overlapping guest booking. | Same validation/allocation rules apply. Staff booking appears and blocks the conflicting guest request. |

## 4. Requirements Coverage

| Requirement | Test Cases |
|---|---|
| FR1 — Booking Form | TC-001, TC-005, TC-009, TC-016 |
| FR2 — Table Allocation | TC-001–TC-004, TC-007, TC-008, TC-010, TC-016 |
| FR3 — Safe Saving | TC-001, TC-008, TC-011, TC-012 |
| FR4 — Confirmation / Refusal | TC-001, TC-002, TC-004, TC-008, TC-011 |
| FR5 — Staff Access | TC-013 |
| FR6 — Staff View | TC-014 |
| FR7 — Cancellation / No-show | TC-006, TC-015 |

## 5. Execution Summary

| Status | Count |
|---|---:|
| Total test cases | 16 |
| Passed | 0 |
| Failed | 0 |
| Blocked | 0 |
| Not Executed | 16 |

Record each scenario separately during execution, including application version, date, actual result, status and evidence.

## 6. Clarifications Before Execution

Confirm required form fields, staff-view sorting, permitted status transitions, SQLite contention behaviour and test mechanisms for failures/concurrency/controlled time.

These are preparation questions, not confirmed defects.

## 7. AI Usage

AI assisted with test design and coverage. All cases require review against approved requirements.

**No tests have been executed. No verified results or confirmed defects are reported.**
