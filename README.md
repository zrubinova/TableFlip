# TableFlip — local prototype

A local university project for **IT in a Real Organization**, implementing FR1–FR7
of Functional Requirements version 2: guest booking, automatic table allocation,
persistent SQLite storage, confirmation/refusal, demonstration staff access,
staff overview, cancellation and no-show handling.

## Run locally

Use Python 3.14. From the repository root, with the existing environment:

```sh
.venv/bin/python -m streamlit run tableflip/app.py
```

Open the local URL printed by Streamlit. Stop with Ctrl+C. For PyCharm, use the
project's `.venv` interpreter, module `streamlit`, parameters
`run tableflip/app.py`, and the repository root as the working directory.

For a fresh checkout on another computer:

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run tableflip/app.py
```

On Windows, use `py -3.14 -m venv .venv` and replace `.venv/bin/python` with
`.venv\Scripts\python.exe`. SQLite, TOML reading and unittest are included in Python.

No package installation or upgrade was performed during this development step.

## Try a booking

Use made-up details. Choose a future Tuesday–Sunday, an available quarter-hour,
and a stay ending by 23:00. For example, four guests at 19:00 with the default
duration receive T5 until 21:00 in an empty database. Submitting another overlapping
four-person booking uses T6. Confirmation includes the saved reference and table.

The database is created automatically at `tableflip/data/tableflip.db`, regardless
of the working directory, and survives application restarts. It is ignored by Git.
The staff tab uses the same database; no schema migration or data reset is required.

## Try the staff functionality

1. Open **Demo access - not secure**. No reservation list or table information
   appears with an empty or incorrect password.
2. Enter `tableflip-demo` in **Staff password** and press Enter. This is the shared
   `staff_password` in `tableflip/settings.toml`, deliberately demonstration-only.
   Clear the password field and press Enter to hide the staff information again.
3. Select **Staff date** and **Table availability at**. Reservations appear in
   start-time order with reference, table, party size, name, phone, email, start/end
   and status. The second table shows all 12 tables, including the occupying
   booking reference when taken. A reservation ending at 20:30 is free at 20:30.
4. Choose a reference under **Reservation to update**, then **Cancel reservation**.
   A Confirmed reservation can be cancelled before its end, including before its
   start. The record remains visible as Cancelled and its table becomes free for
   that slot. A new request can reuse it if it is the smallest suitable free table.
5. For a no-show demonstration, create a made-up booking on an open day at a
   quarter-hour near the current restaurant time. At start + 14 minutes,
   **Mark no-show** is disabled. At start + 15 minutes, click **Refresh staff
   overview**: it becomes enabled. Mark it and verify the saved No-show status,
   free table and disabled actions. No system-clock change is needed; the
   automated tests cover these boundaries using a fixed clock.
6. Create another booking in a second browser session, then click **Refresh staff
   overview** to see it in the first session. No automatic synchronization is used.

Only perform these actions on made-up demonstration bookings you intend to change.
The selected overview date/time is for viewing availability; action eligibility
always uses the actual restaurant clock. Hover over a disabled action for its reason.

## Files and booking rules

- `tableflip/app.py`: guest form, confirmation/refusal and password-gated staff tab.
- `tableflip/allocation.py`: input rules, settings, table selection, table overview
  and shared status-change eligibility checks.
- `tableflip/database.py`: schema initialization, transaction-protected creation,
  date-filtered reservation listing and protected status updates.
- `tableflip/settings.toml`: table capacities, opening hours, duration choices,
  timezone and demonstration staff password.
- `tableflip/tests/`: standard-library unittest tests, including Streamlit AppTest checks.

T1–T4 seat 2 each, T5–T8 seat 4, T9–T11 seat 6, and T12 seats 8: 50 seats total.
Choose the smallest available suitable table, then the lowest numeric table number.
Tables cannot be combined. Only Confirmed reservations block availability.
Two bookings overlap when `existing_start < requested_end` **and**
`existing_end > requested_start`; an exact end/start boundary is allowed.

`create_booking` validates input, starts `BEGIN IMMEDIATE`, checks availability,
inserts and commits, then returns confirmation data. Each call opens its own
connection with a five-second lock timeout. Failures roll back; lock timeouts are
technical errors, distinct from no available table. Phone bookings and walk-ins
use the same form/function. A unique reference uses a `TF-` prefix and a full UUID hex string.

`change_booking_status` also uses `BEGIN IMMEDIATE`: it reads the saved status,
checks the current restaurant clock after acquiring the lock, updates and commits.
Invalid or stale requests are rejected and rolled back. UI buttons use the same
eligibility rules, but the database operation always checks again. Records are
never deleted or changed back to Confirmed. The staff list and table overview
use one freshly loaded reservation list, with no cached booking data.

## Assumptions and scope

- Restaurant time is Europe/Luxembourg, stored as local wall-clock timestamps.
  Current opening hours do not cross the overnight daylight-saving transition.
- Name and at least one phone/email must be nonblank; no additional format rules
  are imposed. All durations are 60, 90 or 120 minutes; omitted means 120.
- Walk-ins use the same form, manually choosing the quarter-hour rounded down.
  Exactly 15 minutes in the past is permitted; more than 15 minutes is refused.
- The historical 23 October 2026 acceptance example uses a fixed clock in tests.
  Live demos should use a valid future date.
- Treat the agreed table settings as fixed once bookings exist. Do not change the
  layout while using an existing demonstration database.
- Cancellation is permitted strictly before the end time. No-show is permitted
  from start + 15 minutes, including after the end: version 2 gives no upper limit.
  Both actions require the saved status to be Confirmed.
- The shared staff password is plain text in settings. It is demonstration access,
  not production security; use made-up data and run locally.
- No editing, live refresh, guest self-cancellation, outage re-entry, table combining,
  duplicate-click protection, hosting or other excluded features are implemented.

## Tests and verification

From the repository root:

```sh
.venv/bin/python -B -m unittest discover -s tableflip/tests -v
```

Tests use disposable temporary databases, never the demonstration database.
They cover allocation, validation, overlap boundaries, persistence, inactive
statuses, failed inserts/commits, lock timeouts and confirmation/error paths.
The integrated AppTest submits the form and verifies a real temporary SQLite row.
Staff tests cover password-gated queries and information, date filtering,
chronological lists, table availability, cancellation and reuse, no-show at 14/15
minutes, disabled actions, invalid status transitions, failed updates and manual
refresh. On 9 November 2026, all **33 tests passed** (the original 18 plus 15 new).

The concurrency check preoccupies T2–T12, releases two threads together using a
barrier, and makes each open its own connection. It expects one T1 confirmation,
one availability refusal and exactly one new row. This is a basic local check,
not load testing or proof for every possible scheduling/crash scenario.
Persistence is checked through closed/reopened connections and schema initialization;
the team independently verified application launch, booking creation, allocation
of overlapping bookings, restart persistence and all original 18 tests before
this staff development phase.

The team has now also manually checked the staff interface in a browser:
the demonstration password works, previously saved reservations are visible,
cancellation works, and no-show handling works for eligible past reservations.
The overview's selected availability time does not change the actual restaurant
clock used for staff actions. The precise 14/15-minute no-show boundary is
covered by automated tests rather than a real-time manual wait.

Injected write/commit failures check rollback; catastrophic disk/process failures
are not simulated. A Streamlit bare-mode ScriptRunContext warning can appear
during AppTest without causing a failure. A fresh checkout on another team
member's computer has not yet been verified.

## AI assistance

Codex assisted with planning, code, documentation and tests. See
`docs/AI_Usage_Log.md`. Team members must review and understand the implementation;
generated code alone is not evidence that a requirement passes.
