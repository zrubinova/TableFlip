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