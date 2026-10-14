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

# TableFlip \- Project charter

### Purpose

This charter authorizes the TableFlip project: an online table booking and capacity management system for one partner restaurant. Today the restaurant takes reservations by phone and assigns tables by hand. At about 20 reservations a day and 2–3 minutes per call, that costs roughly an hour of staff time daily. Busy hours lead to double-booked tables, lost reservations and groups seated at tables that are too small, and guests can only book while someone answers the phone.TableFlip lets guests book online at any time and assigns a suitable table automatically, so staff save time and no table is ever given to two overlapping bookings.  
Critical component \- the capacity and table allocation engine. A wrong answer either double-books a table or leaves a free table unused

### Objectives

| № | Objective | How will we know |
| :---- | :---- | :---- |
| O1 | Guests can book a table without staff | A test user completes a booking end to end with no staff help |
| O2 | No table is assigned to two overlapping bookings | 0 overlaps across all executed allocation test cases |
| O3 | Staff always see the current state of the day | Every create, change and cancel appears in the staff view during the test run |
| O4 | Another team can run the system | The receiving team installs and runs it from the operating manual alone in week 12 |

### Scope

In scope

* Guest booking form: name, contact, party size, date, time, optional stay duration  
* Capacity and table allocation engine (one table per booking)  
* On-screen booking confirmation with table number, date and time  
* Staff view: all reservations and which tables are taken  
* Cancellation, and marking a no-show 15 minutes after the booking time

Out of scope

* Payments and cancellation fees  
* Menu display  
* Combining tables for large groups  
* Waitlist or queue when no table is free  
* SMS or email notifications  
* More than one restaurant, or integration with a POS system  
* Staff can keep taking bookings when the system is down, and enter them later without creating a double-booking

### Team

Sponsor: Prof. Nasyrov  
Team: Illia Nykytiak(PM), Zuzana Rubinova (business analyst), Dylan Almeida and Abdourrahmane Makni (developers), Eman Abdai (QA)

### Budget

No money: free tools only. Our real cost is time: about 210 person-hours (11 weeks, 11 working days, 5 people \* 4h per work day)

### Phases and milestones

| Phase | Week | Milestone | Must be true before it starts | Owner |
| :---- | :---- | :---- | :---- | :---- |
| Inception/Planning | 5 | Charter, plan, risk register accepted | Team formed, roles declared, problem statement and business requirements presented | Illia Nykytiak |
| Planning | 6 | Functional requirements \+ acceptance criteria, default stay duration decided | Charter accepted, in-scope and out-of-scope lists agreed by the team | Zuzana Rubinova with Eman Abdai |
| Launching | 7 | Solution blueprint | Functional requirements and acceptance criteria accepted, default stay duration decided | Dylan Almeida and Abdourrahmane Makni |
| Launching | 8-9 | All in-scope features built, feature freeze at the end of week 9 | Blueprint reviewed, shared repo and dev environment set up, edge-case test list for the allocation engine exists | Dylan Almeida and Abdourrahmane Makni |
| Launching | 10 | Test cases executed, defect log | Feature freeze reached, all in-scope features running in a test environment | Eman Abdai |
| Landing | 11 | Operating manual, dry run by someone outside the team | No open critical defects in the allocation engine, test run complete  | Abdourrahmane Makni |
| Landing | 12-13 | Handover and report on the system we receive | Dry run passed: the system was installed and run from the manual | Illia Nykytiak |

# Risks

| ST | № | Risk | Chance | Impact | Response | Owner |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
|  | R1 | Scope grows (menu, fees, waitlist come back) | High | High | Out-of-scope list in the charter, any addition needs sponsor approval  | Illia Nykytiak |
|  | R2 | Default stay duration still undecided, blocking the allocation engine | High | High | Decision closed in week 6 | Zuzana Rubinova |
|  | R3 | Allocation error at boundaries (one booking ends 20:00, the next starts 20:00) | Medium | High | Edge-case test list written in week 6, before the build | Eman Abdai |
|  | R4 | Two guests book the same table at the same moment | Medium | High | Database-level constraint or transaction plus a dedicated test | Dylan Almeida |
|  | R5 | Integration conflicts between the two developers | Medium | Medium  | Clear split of work, pull-request review before merge | Abdourrahmane Makni |
|  | R6 | A team member is unavailable (exams, illness) | Medium | High | Shared repo and docs, a named backup for each role | Illia Nykytiak |
|  | R7 | Receiving team cannot run the system in week 12 | Medium | High | Simple setup, dry run by someone outside the team in week 11 | Illia Nykytiak |
|  | R8 | No real table layout or input from the restaurant | Low | Medium | Team defines a realistic layout and documents it as an assumption | Zuzana Rubinova |
|  | R9 | AI-generated code or text accepted without checking | Medium | Medium | Review before merge, entries in the AI use log | Illia Nykytiak |

