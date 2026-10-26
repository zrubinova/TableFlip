# TableFlip - Functional Requirements and Acceptance Criteria

Author: Zuzana Rubinová (BA) · Reviewed with: Eman Abdai (QA) · Sources: business requirements BR1-BR10, project charter, risk register, revised scope proposal (24 October 2026)

Status: version 2, follows the revised scope proposal "original scope, small build". Pending team approval.

TableFlip is a small local prototype, not a deployed restaurant service. All requirements in section 3 are mandatory. A requirement is finished when all its acceptance criteria pass in the test environment. The AC numbers refer to the agreed acceptance checks AC01-AC10. Section 5 lists what is deliberately not built.

---

## 1. Decisions

| Decision | Value |
| :---- | :---- |
| Default and maximum stay duration (BR9, closes R2) | **120 minutes.** Used when no duration is chosen. No booking can be longer. |
| Durations that can be chosen | 1 h, 1 h 30, 2 h |
| Tables (BR9, closes R8) | 12 tables, **50 seats**: T1-T4 = 2 seats, T5-T8 = 4 seats, T9-T11 = 6 seats, T12 = 8 seats |
| Opening hours (assumption) | Tuesday-Sunday 11:00-23:00, closed Mondays. A booking must start and end within opening hours. |
| Start times | Every 15 minutes |
| Largest group | 8 guests (the largest table). Larger groups are told to call. |
| Staff access | One demo password, not real security (FR5) |
| Bookings while the system is down (BR10) | Out of scope, as in the charter. Staff keep a paper record outside the system; there is no later re-entry (FR4). |

The tables, opening hours, durations and the staff password are kept in a **settings file**, not written into the program code.

## 2. Basic rules

* A booking occupies **one table** from its start time until start + duration. A booking ending at 20:00 and one starting at 20:00 at the same table do **not** clash.
* Two bookings clash if one starts before the other ends.
* A booking has one of three statuses: **Confirmed** (occupies the table), **Cancelled** or **No-show** (both free the table).
* A table is suitable when it has at least as many seats as the party. Tables are never combined.
* Every booking has a unique reference (e.g. `TF-7KQ3XM`), one table, a start and end time, guest details and a status.
* The system never marks a table as "taken" by hand. To know whether a table is free at a certain time, it checks whether a Confirmed booking for that table covers that time. So a table can be taken at 19:30 and free at 22:00, and a cancelled booking frees its table automatically.
* **Never allowed:** two Confirmed bookings clashing at one table; a party at a table with too few seats; showing a confirmation before the booking is saved.

---

## 3. Requirements

### FR1. Booking form (BR1, BR6, BR9)
One booking form with the fields name, phone or email, party size (1-8), date, start time and stay duration (optional, 120 minutes if left empty). Guests use it to book without staff. Staff use the same form for phone bookings and walk-ins, so these count exactly like guest bookings. A walk-in is entered with the current quarter-hour as the start time.

The form is checked when it is submitted. A booking is refused, with a message saying what is wrong, and nothing is saved, if:
* name or contact is missing, or the party size is not 1-8;
* the date is a Monday, or the start time is more than 15 minutes in the past;
* the stay does not start and end within opening hours;
* the duration is not one of the allowed durations.

**Acceptance criteria**
* A booking without phone and email, for 9 guests, on a Monday, for 2 h 30, or at 21:30 for 2 h (ends after closing) is refused with a message, and nothing is saved. (AC06)
* A booking with no duration chosen gets 120 minutes.
* At 19:07, a walk-in entered for 19:00 is accepted; a booking for 18:45 is refused.

### FR2. Table allocation (BR2, BR4) - critical component
The system gives the booking a table that is suitable and free for the **whole** stay. If several are free, it picks the **smallest** one; among equal sizes, the lowest number. It refuses only if no suitable table is free.

**Acceptance criteria** (empty restaurant unless stated)
* 2 guests → T1; 4 → T5; 6 → T9; 8 → T12. (AC01)
* T1 booked 18:00-20:00: 2 guests at 19:45 → T2; T5-T12 booked 19:00-21:00: 3 guests at 19:00 → refused. (AC02)
* T1 booked 18:00-20:00: 2 guests at 20:00 → T1. (AC03)
* All 4-, 6- and 8-seat tables taken, two 2-seat tables free: 4 guests → refused. (AC04)
* A cancelled or no-show booking does not block its table.

### FR3. Safe saving (BR2, R4)
Checking for a free table and saving the booking happen in **one protected database transaction**, so two requests at the same moment can never get the same table. Bookings are stored in a local database and survive a restart of the application.

**Acceptance criteria**
* Only T1 is free; two requests for 2 guests are sent at the same moment → one is confirmed, the other gets the refusal. How the test was run and its limits are recorded. (AC09)
* After closing and restarting the application, all saved bookings are still there. (AC05)

### FR4. Confirmation and refusal (BR3, BR4)
After a successful save, the screen shows the reference, table, date, start and end time. If no suitable table is free, it shows "Sorry, we have no free table for <n> guests on <date> at <time>. Please try another time." If allocation or saving fails for a technical reason, it shows "Booking unavailable, please try again later or call the restaurant" and no booking exists. Staff then keep a paper record outside the system.

**Acceptance criteria**
* 4 guests, Friday 23 October 19:00, empty restaurant → reference, "Table T5", "23 October 2026", "19:00 - 21:00". The same booking appears in the staff view. (AC05)
* When no table is free, the refusal is shown and the number of bookings does not change. (AC06)
* When the database cannot save, no confirmation is shown and no booking exists. (AC06)

### FR5. Staff access (demo only)
The staff view is on a separate tab, opened with one password from the settings file. The tab is labelled "Demo access - not secure". Demos use made-up guest data only.

**Acceptance criteria**
* Without the password, the staff tab shows no booking data.

### FR6. Staff view (BR8)
Staff choose a date and a time. The view shows:
* **Booking list** for that date, in start-time order: time, table, guests, name, contact, status and reference.
* **Tables** at the chosen time: for each table, free or taken, and by which booking.

The view shows the bookings saved at the moment it is opened or refreshed.

**Acceptance criteria**
* 5 bookings on a day, 1 cancelled: the list shows all 5 with their status in time order, and the cancelled one does not make its table taken. (AC07)
* T2 booked 18:30-20:30: at 19:00 T2 is shown as taken by that booking; at 20:30 it is free. (AC07)

### FR7. Cancel and no-show (BR5, BR7)
In the staff view, staff can **cancel** a Confirmed booking until its end time. Guests who want to cancel call the restaurant. From **15 minutes after the start time**, staff can mark a Confirmed booking as **no-show**; before that the button is disabled. Both free the table at once for new bookings.

**Acceptance criteria**
* All tables booked Friday 19:00-21:00; staff cancel the booking at T3; the next request for 2 at 19:00 gets T3. (AC08)
* Booking at 19:00: the no-show button is disabled at 19:14 and enabled at 19:15. After the no-show is marked, a booking for 2 at 19:30 can get that table. (AC08)

---

## 4. Open issues

**BR5** says *a guest* can cancel. In this build only staff cancel, after the guest calls. **Proposal:** accept this for the prototype. *Decision: Illia Nykytiak, week 7.*

**BR8** says bookings appear in the staff view *without a manual refresh*. In this build staff see new bookings when they open or refresh the view. **Proposal:** accept this for the prototype; if the developers can add an automatic refresh cheaply, do it. *Decision: Illia Nykytiak with the developers, week 7.*

**Charter:** the scope wording stays valid, but the charter should note that TableFlip is a local prototype with demo-only staff access. *Owner: Illia Nykytiak, week 7.*

---

## 5. Not built in this version

These were in the earlier version of this document and were removed to keep the build small. They may be listed as possible future work in the final report.

* Live time list in the booking form that shows only free times; checks happen on submit instead.
* Load testing with many simultaneous requests and double-click protection beyond the database transaction.
* Guest self-cancellation with reference and contact.
* Real staff accounts with hashed passwords and roles; online deployment.
* Separate staff booking form, walk-ins with shorter stays, and Rebook.
* Editing bookings.
* "Guests left", "Over time" warnings, extending stays and moving later bookings to other tables.
* Free periods per table, search, and automatic updates across devices.
* A margin between bookings, waitlist, payments, menu, SMS, email and POS integration.
