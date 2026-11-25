# TableFlip QA test report — Week 10

**Execution date:** 25 November 2026  
**QA owner:** Eman Abdai, per the project charter  
**QA documentation baseline:** `QA/test-plan`  
**Application tested:** Developer commit 
**Release sign-off:** Pending

## Executive summary

The automated suite ran 33 tests. **32 passed, one failed, and zero ended in error.** The failure was a staff tab label mismatch between the application and the test expectation. The staff cancellation test that timed out in the prior QA report passed in this run.

Table allocation remained consistent in the exercised scenarios. In 30 additional trials, two requests competed for the only eight-seat table. Each trial produced one confirmed booking, one handled refusal, and zero overlapping reservations.

Proceed with the local prototype dry run once the team confirms the approved scope and reviews the open findings. Release acceptance remains pending until the team records its scope decision, completes regression testing on the handover build, and verifies the receiving team can operate the system.

## Test strategy and scope

Prioritize the allocation engine because booking conflicts and undersized assignments directly affect guests and staff. Verify the committed SQLite record as well as the UI response. Combine allocation rule tests, database integration and rollback checks, Streamlit AppTest, and manual acceptance by the receiving team. Include invalid input, exact time boundaries, concurrent requests, and regression cases.

Use the QA test plan and test cases for detailed steps. The Week 10 milestone records the remaining gates and owners.

The v2 prototype requirements are marked pending team approval. They specify manual refresh for staff and staff-assisted cancellation. The business requirements call for automatic staff updates (BR8) and guest self-cancellation (BR5). The PM and BA should confirm which baseline governs handover. The charter’s O1 measures unaided guest **booking**, so guest cancellation is tracked separately under BR5.

## Test environment and results

The application ran from an isolated copy of the pinned Developer commit using Linux, Python 3.12.14, Streamlit 1.66.1, disposable SQLite databases, and synthetic records. The Developer README recommends Python 3.14. The results below apply to the Python 3.12.14 environment used for this run.

Run the following commands from the root of the Developer checkout in a virtual environment.

~~~sh
python -m pip install -r requirements.txt
python -m unittest discover -s tableflip/tests -v
~~~

**Result:** 32/33 passed (97.0%) in 3.635 seconds. See the Week 10 execution evidence.

| Requirement or risk | Tests and observations | Result |
| --- | --- | --- |
| O1 / BR1, BR3 — unaided booking | TC-001. AppTest submitted a guest booking and verified the saved SQLite record. | Pass in AppTest. Representative guest UAT pending. |
| O2 / BR2, BR4 / R3, R4 — allocation | TC-002–004, TC-007, TC-008, TC-010. Checked capacity, overlap, refusal, allocation priority, exact end/start boundaries, and contention. The supplemental T12 check ran 30 times. | Pass in exercised scenarios. Zero observed same-table overlaps or undersized assignments. |
| BR9 / R2 — capacity and duration | TC-005, TC-009. Verified the 120-minute default, allowed durations, invalid input, and closing-time boundary. The configured layout totals 50 seats. | Pass for the tested rules and layout. |
| FR3 / R4 — safe persistence | TC-011. Injected insert and commit failures to check rollback. Held a write lock to verify technical-error handling. | Pass under the simulated failures. |
| BR5, BR7 / v2 FR7 — cancel and no-show | TC-006, TC-015. Staff cancellation released the table. No-show was blocked before 15 minutes and allowed at the threshold. The guest tab had no self-cancellation control. | Staff flow passed. BR5 gap logged as QA-02. |
| O3 / BR8 / v2 FR6 — staff visibility | A new booking appeared after manual refresh. Staff cancellation updated the same session. Source and README describe refresh-on-demand for changes from another session. | Prototype behavior verified. BR8 gap logged as QA-01. |
| v2 FR5 — demo staff access | A focused AppTest hid staff data with incorrect or cleared credentials and displayed it after entering the configured demo password. | Focused check passed. Suite label assertion failed under QA-05. |
| O4 / R7 — handover | Receiving team independently installs and operates the system from the manual. | Pending. |

Browser end-to-end testing, representative UAT, response-time benchmarks, sustained load, and infrastructure recovery remain unverified in this run.

## Defect log

IDs follow the prior QA report. Severity reflects impact. Priority reflects the proposed fix order. Assignees are proposed for team confirmation.

| ID | Expected and observed behavior | Severity | Priority | Status | Reporter | Proposed assignee |
| --- | --- | --- | --- | --- | --- | --- |
| QA-01 | BR8 expects staff to see updates automatically. A booking from another session appears after refreshing the staff view. | High | P1 | Business gap. v2 concession pending approval. | Eman Abdai (QA) | Abdourrahmane Makni |
| QA-02 | BR5 expects guests to cancel and release their tables. The guest tab has no cancellation control. v2 routes cancellation through staff. | High | P1 | Business gap. v2 concession pending approval. | Eman Abdai (QA) | Dylan Almeida |
| QA-03 | An accidental repeat submission should avoid creating a second booking. Two identical sequential calls to the booking function committed distinct references on T1 and T2. Confirm how legitimate repeat bookings should be handled. | Medium | P2 | Reproduced at the booking function. Browser double-click retest pending. | Eman Abdai (QA) | Dylan Almeida |
| QA-04 | A guest should be able to retrieve the confirmation reference long enough to record it. The prior report observed it disappearing after another interaction. Source renders it only during the submit run. | Medium | P2 | Prior finding supported by source review. Browser retest and retention criteria pending. | Eman Abdai (QA) | Dylan Almeida |
| QA-05 | The test and README expect `Demo access - not secure`. The UI renders `Demo staff access`. | Low | P3 | Reproduced. Align the agreed wording and rerun the full suite. | Eman Abdai (QA) | Abdourrahmane Makni |

## Sign-off and AI disclosure

Record the approved baseline, the disposition of each open finding, the regression results for the handover build, and the receiving team’s UAT decision before sign-off. See the handover milestone.

The Week 10 lecture slides informed the strategy, plan, test case traceability, defect log, and release recommendation. AI assisted with probe design and evidence compilation. The results are based on execution and source review. Human sign-off remains pending.

