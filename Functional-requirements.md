# TableFlip - Functional Requirements and Acceptance Criteria

Author: Zuzana Rubinová (BA) · Reviewed with: Eman Abdai (QA) · Sources: business requirements BR1-BR10, project charter, risk register

All requirements are mandatory. A requirement is finished when all its acceptance criteria pass in the test environment.

---

## 1. Decisions

| Decision | Value |
| :---- | :---- |
| Default and maximum stay duration (BR9, closes R2) | **120 minutes.** Used for every phone and walk-in booking, and for online bookings where the guest does not choose. No booking can be made for longer. |
| Durations a guest can choose online | 1 h, 1 h 30, 2 h |
| Tables (BR9, closes R8) | 12 tables, **50 seats**: T1-T4 = 2 seats, T5-T8 = 4 seats, T9-T11 = 6 seats, T12 = 8 seats |
| Opening hours (assumption) | Tuesday-Sunday 11:00-23:00, closed Mondays. A booking must start and end within opening hours. |
| Start times | Online: every 15 minutes. Staff: every 5 minutes. |
| Online bookings | At least 15 minutes before the start time, at most 30 days ahead |
| Largest group | 8 guests (the largest table). Larger groups are told to call. |

The tables, opening hours, closed days and the values above are kept in a **settings file**, not written into the program code, so the restaurant can change them later without a developer.

## 2. Basic rules

* A booking occupies **one table** from its start time until start + duration. A booking ending at 20:00 and one starting at 20:00 at the same table do **not** clash.
* Two bookings clash if one starts before the other ends.
* A booking has one of three statuses: **Confirmed** (occupies the table), **Cancelled** or **No-show** (both free the table).
* A table is suitable when it has at least as many seats as the party.
* **Never allowed:** two Confirmed bookings clashing at one table; a party at a table with too few seats; showing a confirmation before the booking is saved.
* Every booking gets a unique reference, e.g. `TF-7KQ3XM`.

---

## 3. Guest booking

### FR1. Booking form (BR1, BR9)
A public page, available at any time without staff, with fields in this order: date, party size (1-8), stay duration (optional, pre-set to 2 h), time, name, and phone or email (at least one).

The time list shows only times where:
* the whole stay fits within opening hours;
* for today, the start is at least 15 minutes from now;
* at least one suitable table is free for the whole stay (FR2 rules).

The list is recalculated whenever the date, party size or duration changes. If no time is left on that date, the guest sees "No free tables for <n> guests on this date. Please choose another date." Because another guest may take the last table while the page is open, the system checks again on "Book", and may still refuse (FR4). The server checks all rules again and saves nothing if any rule fails.

**Acceptance criteria**
* On a Wednesday with an empty restaurant and 2 h selected, times run from 11:00 to 21:00; with 1 h, until 22:00.
* All tables booked Friday 11:00-13:00: for 2 guests, the first time offered is 13:00.
* Only T12 booked, Friday 19:00-21:00: for 8 guests and 2 h, 17:00 and 21:00 are offered, but 17:15 to 20:45 are not. For 2 guests, all times are offered.
* Changing the party size from 2 to 8 updates the time list without reloading the page.
* All tables fully booked on a date: the "No free tables" message is shown instead of times.
* At 18:10, the first time offered for today is 18:30.
* Mondays and dates more than 30 days ahead cannot be chosen.
* Without phone and email, the booking is not accepted.
* A guest who does not choose a duration gets 120 minutes.
* A request sent directly to the server for 9 guests, 19:07, 2 h 30, or 21:30 with 2 h (ends after closing) is refused and nothing is saved.

### FR2. Table allocation (BR2, BR4) - critical component
The system gives the booking a table that is suitable and free for the **whole** stay. If several are free, it picks the **smallest** one; among equal sizes, the lowest number. It refuses only if no suitable table is free. Tables are never combined.

**Acceptance criteria** (empty restaurant unless stated)
* 2 guests → T1; 3 or 4 → T5; 5 or 6 → T9; 7 or 8 → T12.
* T1 booked 18:00-20:00: 2 guests at 20:00 → T1; at 19:45 → T2.
* T1 booked 20:00-22:00: 2 guests at 18:30 for 2 h → T2.
* T1-T4 booked 19:00-21:00: 2 guests at 19:30 → T5 (a bigger table, not a refusal).
* T5-T12 booked 19:00-21:00: 3 guests at 19:00 → refused.
* All tables booked 19:00-21:00: 2 guests at 19:00 → refused; at 21:00 → T1.
* A cancelled or no-show booking does not block its table.

### FR3. Simultaneous bookings (BR2, R4)
When several people book at the same moment, two of them can never get the same table for clashing times. The database itself must prevent this, not only the program code. A guest who loses the race gets another free table, or the normal refusal, never an error page. Clicking "Book" twice creates only one booking.

**Acceptance criteria**
* Only T1 is free; 20 requests for 2 guests arrive at the same moment → exactly 1 is confirmed, 19 are refused.
* Empty restaurant; 20 simultaneous requests for 2 guests at 19:00 → 12 confirmed on 12 different tables, 8 refused.
* After every test run, 0 clashing bookings and 0 parties at too-small tables exist.
* A double click on "Book" creates exactly one booking.

### FR4. Confirmation and refusal (BR3, BR4)
Immediately after saving, the guest sees: reference, date, start and end time, **table number**, party size and name, plus a note to keep the reference for cancelling. If no table is free, the guest sees "Sorry, we have no free table for <n> guests on <date> at <time>. Please try another time." The form keeps everything they entered and nothing is saved.

**Acceptance criteria**
* 4 guests, Friday 23 Oct 19:00, empty restaurant → shows the reference, "Friday, 23 October 2026", "19:00 - 21:00", "Table T5", "4 guests".
* The confirmation matches the booking in the staff view.
* When the restaurant is full, the refusal message is shown and the number of bookings does not change.
* If saving fails for a technical reason, no confirmation is shown and no booking exists.

### FR5. Guest cancellation (BR5)
On "Cancel a booking" the guest enters the reference and the phone or email they used. If both match, they can cancel after confirming; the table becomes free at once. Cancelling online is possible until the start time. A wrong reference or contact shows one general "not found" message.

**Acceptance criteria**
* With the right reference and phone, the booking is found and can be cancelled; with a wrong phone, "not found" is shown.
* All tables booked Friday 19:00-21:00; the guest at T3 cancels; the next request for 2 at 19:00 gets T3.
* A booking that started at 19:00 cannot be cancelled online at 19:00 or later.

---

## 4. Staff

### FR6. Staff login
Staff pages require a username and password. Staff accounts are created by the person installing the system, as described in the operating manual. Passwords are not stored in readable form.

**Acceptance criteria**
* Without logging in, no staff page and no booking data can be opened.

### FR7. Phone bookings (BR6, BR10)
Staff enter date, time, party size, name and phone or email. The duration is always 120 minutes. The table is chosen automatically, or staff pick one from a list that shows only suitable free tables. Unlike online bookings, a staff booking may start less than 15 minutes from now. Staff may also enter a time earlier today, to enter bookings written on paper while the system was down. Phone bookings follow exactly the same allocation rules as online bookings. If the chosen table is no longer free, nothing is saved and staff see which booking it clashes with. Rules can never be overridden.

**Acceptance criteria**
* A phone booking for 4 at Friday 19:00 gets T5; an online request for 4 at 19:30 then gets T6.
* T5 booked 19:00-21:00: for 4 guests at 19:30, the table list does not show T1-T5.
* A paper booking re-entered for T5 after an online guest took T5 is not saved; staff see the clash and can choose another table.
* At 20:00 staff can enter a booking for 20:05 today.
* A booking for yesterday cannot be entered.

### FR8. Walk-ins (BR6)
Each table that is free now has a "Seat walk-in" button. Staff enter only the party size; name and contact are optional. The booking starts now and lasts 120 minutes, or ends at closing time if that comes sooner. It is refused if the table is not free for that whole time.

**Acceptance criteria**
* At 19:00, a walk-in for 3 at T5 → booking at T5, 19:00-21:00.
* At 21:40, a walk-in gets 21:40-23:00.
* T1 is booked from 20:00: at 19:00 a walk-in at T1 is refused.

### FR9. Edit and cancel (BR5, BR8)
Staff can change a Confirmed booking's date, time, party size, table, name and contact, and can cancel it, until its end time. After a change, the booking keeps its table if that table still fits; otherwise it gets a new table by the FR2 rules. If no table fits, the change is refused and the booking stays as it was.

**Acceptance criteria**
* A booking at T5 19:00 for 4 moved to 19:30 stays at T5.
* Changed to 5 guests, it moves to T9 and staff see "Table changed from T5 to T9".
* With T9-T12 taken, a change to 6 guests is refused and the booking is unchanged.
* After staff cancel a booking, its table can be booked again for that time.

### FR10. End of stay (BR2, BR8)
Allocation always uses the planned end time, so future bookings never wait for staff to press anything.

**Guests left.** A Confirmed booking that has started has a **"Guests left"** button. Pressing it changes the end time to now, rounded down to 5 minutes, and marks the booking as "guests left". The status stays Confirmed. The table is free from that moment, so it can be given to walk-ins or new bookings at once.

**Over time.** If the end time has passed and staff have not pressed "Guests left", the table card on the table board turns red: **"Over time - guests still here?"** It offers "Guests left" and "Extend stay". The warning stays until staff press one of them, or until closing time. The system never decides on its own that the guests have gone.

**Extend stay.** If guests stay longer, staff choose a new end time, in 15-minute steps up to closing time. This works even after the end time has passed. If the table is free until the new end time, the extension is saved. If another booking on that table clashes, nothing is saved and staff see that booking. Staff can then move it to another table (FR9) and try again.

**Acceptance criteria**
* T2 booked 19:00-21:00; at 20:32 staff press "Guests left": the booking now ends 20:30, T2 shows "Free", and a walk-in can be seated at T2 at once.
* After "Guests left", no "Over time" warning appears for that booking.
* T2 booked 19:00-21:00 and nothing pressed: at 21:00 the T2 card turns red with "Over time - guests still here?", and it is still red at 21:30.
* The "Over time" warning does not stop online guests from being given T2 for later times.
* T2 booked 19:00-21:00, nothing after it: extending to 21:30 is saved, and online guests can no longer get T2 at 21:00.
* T2 booked 19:00-21:00 and again from 21:00: extending to 21:30 is refused and the 21:00 booking is shown. After staff move that booking to T3, the extension is saved.
* At 21:10, a booking that ended at 21:00 can still be extended.

### FR11. No-show (BR7)
Staff can mark a Confirmed booking as no-show from **15 minutes after its start time**. Before that, the button is disabled. Marking a no-show frees the table at once for the rest of the booking time.

**Acceptance criteria**
* Booking at 19:00: the button is disabled at 19:14 and enabled at 19:15.
* After the no-show is marked at 19:20, the table shows as free and a walk-in can be seated there.

### FR12. Staff view (BR8)
After login, staff see today's bookings and can switch to any other day. The view has:
* **Booking list**, in start-time order: time, table, guests, name, contact, status and reference. It also shows the number of bookings and guests for the day. A booking whose start time has passed and is not marked as no-show is labelled "Late", and from 15 minutes after the start "No-show possible".
* **Table board**: one card per table, showing whether it is free, taken or over time now (FR10), its next booking, and its free periods for the rest of the day.

**Acceptance criteria**
* 5 bookings today, 1 cancelled: the list shows 4 active bookings in time order with the correct number of guests.
* At 18:00, T2 with bookings 18:30-20:30 and 21:00-23:00 shows "Free", next booking 18:30, free "18:00-18:30, 20:30-21:00".

### FR13. Search (BR8)
One search box above the booking list. Searching starts after 2 characters and updates while staff type:
* **Name:** matches any part of the name. Upper/lower case and accents are ignored, so "zoe" finds "Zoë".
* **Phone:** matches any part of the number. Spaces, dashes and "+" are ignored, so "621123" finds "+352 621 123 456".
* **Reference:** with or without "TF-", any case.

The search covers **today and all future dates**. It shows **every** matching booking, sorted by date and time, with date, time, table, guests, contact and status, so staff can tell bookings under the same name apart. Today's matches are also **highlighted on the table board**. Clearing the box returns to the normal view.

**Acceptance criteria**
* Three bookings under "Novak" (two today at T3 and T7, one next week): searching "nov" lists all three, and T3 and T7 are highlighted on the board.
* Searching "zoe", "621123" or "tf-7kq3xm" finds the matching booking.
* Yesterday's bookings are not found by the search.

### FR14. Live updates (BR8)
Every new, changed, extended or cancelled booking, every "guests left" and every no-show appears in every open staff view **within 5 seconds**, without refreshing the page. An update never closes a form that staff are filling in.

**Acceptance criteria**
* With the staff view open on two devices, an online booking appears on both within 5 seconds.
* In a test run of at least 20 changes, each one appears in the staff view within 5 seconds.
* Staff typing a phone booking keep their form when an online booking arrives.

---

## 5. Open issues

BR10 says staff can keep taking bookings while the system is down, but the charter lists this as out of scope. **Proposal:** follow the charter. Paper bookings are entered later through FR7, which flags every clash instead of saving it. *Decision: Illia Nykytiak, end of week 6.*

BR9 limits each reservation to 120 minutes, but FR10 lets staff extend a stay when guests are still at the table. **Proposal:** keep it. Nobody can book longer than 120 minutes, and the extension only records that guests have not left yet, so the table is not given away while they are still there. *Decision: Eman Abdai, end of week 7.*
