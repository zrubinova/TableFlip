# Problem Statement

Restaurants take every reservation by phone and assign tables by hand, and during busy hours this loses staff time, loses bookings and puts guests at tables that are already taken or too small.

### Who is affected:

Front-of-house staff \- answer the phone while serving guests, keep the reservation book by hand, and fix seating mistakes on the spot

Guests \- can only book while someone answers the phone, and sometimes arrive to find no record of their booking

Restaurant owner \- loses revenue from empty tables and missed calls, and loses reputation after double-bookings

### What it costs to do nothing 

The direct cost is 40–60 minutes of staff time every day, the larger cost is lost revenue and reputation.

### What they cannot do today?

1\) Guests cannot book outside opening hours, or when staff are too busy to pick up the phone.

2\) Staff cannot see at a glance which tables are free for the rest of the evening, so they work it out from the book each time.

3\) Nobody can be sure a booking was recorded, a reservation taken during a rush can be written in the wrong slot or not at all.

4\) Staff cannot reliably tell whether a table promised to one party has already been promised to another for an overlapping time.

5\) Staff cannot match party size to table size reliably, so groups are sometimes seated at tables that are too small.

# Business Requirements

### Critical component

The table allocation must be trusted by the guest, who travels to the restaurant counting on a table being there, and by the staff, who seat parties according to it without re-checking the book

### Requirements

1\. A guest can request a table for a date, time and party size at any time of day, without speaking to staff, and can say how long they plan to stay. (A booking made at 23:00 is confirmed with no staff involved)

2\. Every confirmed party has a table that seats the whole group, and no table is promised to two parties for overlapping times. (Across all test cases: 0 overlaps, and 0 parties placed at a table smaller than their group)

3\. A guest knows at once whether the booking is confirmed, and for which date, time and table. (The confirmation shows date, time and table number immediately after booking)

4\. When no suitable table is free, the guest is told at once that the requested time is unavailable. (A request for a fully booked time is refused with a clear message, never silently accepted)

5\. A guest can cancel their booking, and the table becomes available to others. (After a cancellation, the same table can be booked for that time)

6\. Staff can record bookings taken by phone and walk-in guests, and these count exactly like online bookings. (A phone booking blocks its table for online guests at the same time)

7\. Staff can release a table when a party has not arrived 15 minutes after its booking time. (A booking marked as a no-show frees its table for the rest of its time slot)

8\. Staff can see, at any moment, all of the day's bookings and which tables are taken. (Every new, changed or cancelled booking appears in the staff view without a manual refresh of the book)

9\. Staff can keep taking bookings when the system is down. (Re-entering a paper booking that clashes with an online one is flagged, not saved silently)

