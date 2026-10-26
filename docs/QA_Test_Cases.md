# TableFlip — QA Test Cases

**Project:** TableFlip  
**QA Approach:** AI-Assisted Testing  
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
