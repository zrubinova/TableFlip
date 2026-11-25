# TableFlip — Week 10 execution evidence

**Execution date:** 25 November 2026  
**Application commit:** [`e09b423f6c94df345eab907ad7d6c1c14f578711`](https://github.com/zrubinova/TableFlip/commit/e09b423f6c94df345eab907ad7d6c1c14f578711)  
**Environment:** Python 3.12.14, Streamlit 1.66.1, disposable SQLite databases, synthetic test records.

## Automated regression suite

From the application checkout, install `requirements.txt` and run:

```sh
python -m unittest discover -s tableflip/tests -v
```

Observed console summary:

```text
FAIL: test_no_data_or_queries_until_correct_password (test_staff.StaffAppTests.test_no_data_or_queries_until_correct_password)
AssertionError: 'Demo access - not secure' not found in ['Book a table', 'Demo staff access']
Ran 33 tests in 3.635s
FAILED (failures=1)
```

**Totals:** 33 executed, 32 passed, 1 failure, 0 errors. `test_cancel_updates_display_and_disables_both_actions` passed. The failed assertion stopped the staff access test before its credential checks, so those behaviors were exercised separately.

## Focused checks

### TC-007 and TC-008 — Last-table contention and exact boundary

For each of 30 trials, initialize a fresh SQLite database and set the test clock to 10:00 on Friday, 27 November 2026. Use two threads with independent database connections and a shared start barrier. Both request the 19:00–21:00 slot for eight guests. T12 is the only table that fits.

Inspect the stored reservations. Then book T12 for eight guests starting at 21:00 and inspect the rows again.

**Observed:** 30/30 trials produced one T12 confirmation, one handled unavailability response, and exactly one initial committed row. Every trial allowed the adjacent 21:00 reservation on T12. Zero overlaps were observed.

### QA-03 — Identical repeat requests

In a fresh database, submit the same two-person request twice using the same name, contact, date, and time. Compare the booking references, table assignments, and persisted row count.

**Observed:** Both calls committed. The first assigned T1 and the second assigned T2. The records had distinct references. Browser double-click behavior was not exercised in this run.

### QA-02 and QA-05 — Guest controls and demo staff access

In an isolated AppTest session, inspect the public booking tab. Open the staff view with an incorrect password, the configured demo password, and then a cleared password.

**Observed:** The public tab had no cancellation button. Incorrect and cleared credentials hid staff data. The configured demo password displayed the staff reservation and table views.

[Week 10 QA test report](../QA_Test_Report.md)
