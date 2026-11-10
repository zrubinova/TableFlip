"""Staff rules use temporary databases and fixed restaurant-local clocks."""

from contextlib import ExitStack
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from tableflip.allocation import load_settings, table_overview
from tableflip.database import (
    BookingStorageError, InvalidStatusChange, change_booking_status, connect,
    create_booking, initialize_database, list_reservations,
)


class StaffDatabaseTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "staff.db"
        initialize_database(self.path)
        self.settings = load_settings()
        self.start = datetime(2026, 10, 23, 19)

    def book(self, **changes):
        arguments = dict(name="Made-up Guest", phone="123", email="", party_size=2,
                         start=self.start, now=self.start - timedelta(hours=1))
        arguments.update(changes)
        return create_booking(self.path, self.settings, **arguments)

    def change(self, booking, status, now):
        change_booking_status(self.path, self.settings, booking["reference"], status, now=now)

    def test_list_is_date_filtered_ordered_and_preserves_all_statuses(self):
        late = self.book(start=self.start + timedelta(hours=1))
        early = self.book(start=self.start - timedelta(hours=1),
                          now=self.start - timedelta(hours=2))
        middle = self.book()
        self.change(early, "Cancelled", self.start)
        self.change(middle, "No-show", self.start + timedelta(minutes=15))
        self.book(start=self.start + timedelta(days=1))
        rows = list_reservations(self.path, self.start.date())
        self.assertEqual([row["reference"] for row in rows],
                         [early["reference"], middle["reference"], late["reference"]])
        self.assertEqual([row["status"] for row in rows], ["Cancelled", "No-show", "Confirmed"])
        self.assertEqual(rows[0]["name"], "Made-up Guest")
        self.assertEqual(rows[0]["phone"], "123")
        self.assertEqual(list_reservations(self.path, self.start.date() - timedelta(days=1)), [])

    def test_table_overview_start_end_and_numeric_order(self):
        booking = self.book()
        rows = list_reservations(self.path, self.start.date())
        before = table_overview(self.settings["tables"], rows, self.start - timedelta(seconds=1))
        start = table_overview(self.settings["tables"], rows, self.start)
        end = table_overview(self.settings["tables"], rows, self.start + timedelta(hours=2))
        self.assertEqual(len(start), 12)
        self.assertEqual([row["Table"] for row in start], [f"T{number}" for number in range(1, 13)])
        self.assertEqual(before[0]["Availability"], "Free")
        self.assertEqual(start[0]["Availability"], "Taken")
        self.assertEqual(start[0]["Booking reference"], booking["reference"])
        self.assertEqual(end[0]["Availability"], "Free")
        self.assertEqual(end[0]["Booking reference"], "")

    def test_cancel_releases_last_available_table_and_keeps_record(self):
        bookings = [self.book() for _ in range(12)]
        self.change(bookings[2], "Cancelled", self.start)
        rows = list_reservations(self.path, self.start.date())
        overview = table_overview(self.settings["tables"], rows, self.start)
        self.assertEqual(overview[2]["Availability"], "Free")
        self.assertEqual(self.book()["table_id"], "T3")
        rows = list_reservations(self.path, self.start.date())
        self.assertEqual(len(rows), 13)
        self.assertEqual(next(row for row in rows if row["reference"] == bookings[2]["reference"])
                         ["status"], "Cancelled")

    def test_cancellation_end_boundary(self):
        booking = self.book()
        for now in (self.start + timedelta(hours=2), self.start + timedelta(hours=3)):
            with self.subTest(now=now), self.assertRaises(InvalidStatusChange):
                self.change(booking, "Cancelled", now)
        self.change(booking, "Cancelled", self.start + timedelta(hours=2, microseconds=-1))

    def test_future_booking_can_be_cancelled(self):
        self.change(self.book(), "Cancelled", self.start - timedelta(days=1))
        self.assertEqual(list_reservations(self.path, self.start.date())[0]["status"], "Cancelled")

    def test_no_show_14_and_15_minute_boundary_and_reuse(self):
        booking = self.book()
        for offset in (timedelta(minutes=14), timedelta(minutes=15, microseconds=-1)):
            with self.subTest(offset=offset), self.assertRaises(InvalidStatusChange):
                self.change(booking, "No-show", self.start + offset)
        self.assertEqual(list_reservations(self.path, self.start.date())[0]["status"], "Confirmed")
        self.change(booking, "No-show", self.start + timedelta(minutes=15))
        rows = list_reservations(self.path, self.start.date())
        self.assertEqual(rows[0]["status"], "No-show")
        self.assertEqual(table_overview(self.settings["tables"], rows, self.start)[0]
                         ["Availability"], "Free")
        self.assertEqual(self.book(start=self.start + timedelta(minutes=30))["table_id"], "T1")
        self.assertEqual(len(list_reservations(self.path, self.start.date())), 2)

    def test_no_show_after_end_is_allowed_by_specification(self):
        self.change(self.book(), "No-show", self.start + timedelta(hours=3))
        self.assertEqual(list_reservations(self.path, self.start.date())[0]["status"], "No-show")

    def test_terminal_statuses_cannot_be_changed_or_reconfirmed(self):
        for initial in ("Cancelled", "No-show"):
            booking = self.book()
            self.change(booking, initial, self.start + timedelta(minutes=15))
            for target in ("Cancelled", "No-show", "Confirmed", "Invalid"):
                with self.subTest(initial=initial, target=target), self.assertRaises(InvalidStatusChange):
                    self.change(booking, target, self.start + timedelta(minutes=30))

    def test_missing_booking_and_unsupported_status(self):
        with self.assertRaises(InvalidStatusChange):
            change_booking_status(self.path, self.settings, "missing", "Cancelled", now=self.start)
        booking = self.book()
        for target in ("Confirmed", "Deleted", "", None):
            with self.subTest(target=target), self.assertRaises(InvalidStatusChange):
                self.change(booking, target, self.start)
        self.assertEqual(list_reservations(self.path, self.start.date())[0]["status"], "Confirmed")

    def test_failed_update_preserves_booking(self):
        booking = self.book()
        connection = connect(self.path)
        try:
            connection.execute("""CREATE TRIGGER fail_update BEFORE UPDATE ON reservations
                                  BEGIN SELECT RAISE(ABORT, 'simulated failure'); END""")
        finally:
            connection.close()
        with self.assertRaises(BookingStorageError):
            self.change(booking, "Cancelled", self.start)
        self.assertEqual(list_reservations(self.path, self.start.date())[0]["status"], "Confirmed")


class StaffAppTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "staff-ui.db"
        initialize_database(self.path)
        self.settings = load_settings()
        self.start = datetime(2026, 10, 23, 19)
        self.now = self.start + timedelta(minutes=14)
        self.booking = create_booking(
            self.path, self.settings, name="Protected Test Guest", phone="123",
            email="", party_size=2, start=self.start, now=self.start,
        )
        stack = self.enterContext(ExitStack())
        stack.enter_context(patch("tableflip.database.DEFAULT_DATABASE", self.path))
        stack.enter_context(patch("tableflip.database.initialize_database"))
        stack.enter_context(patch("tableflip.allocation.restaurant_now", side_effect=lambda settings: self.now))
        stack.enter_context(patch("tableflip.database.restaurant_now", side_effect=lambda settings: self.now))
        self.app = AppTest.from_file(str(Path(__file__).parents[1] / "app.py")).run()
        self.assertEqual(len(self.app.exception), 0)

    def button(self, label):
        return next(button for button in self.app.button if button.label == label)

    def unlock(self):
        self.app.text_input(key="staff_password").set_value(self.settings["staff_password"]).run()
        self.assertEqual(len(self.app.exception), 0)

    def test_no_data_or_queries_until_correct_password(self):
        self.assertIn("Demo access - not secure", [tab.label for tab in self.app.tabs])
        with patch("tableflip.database.list_reservations") as query:
            self.app.run()
            self.assertEqual(len(self.app.dataframe), 0)
            self.app.text_input(key="staff_password").set_value("wrong-password").run()
            self.assertEqual(len(self.app.dataframe), 0)
            query.assert_not_called()
        self.unlock()
        self.assertEqual(len(self.app.dataframe), 2)
        self.assertIn("Protected Test Guest", self.app.dataframe[0].value["Name"].tolist())
        self.app.text_input(key="staff_password").set_value("").run()
        self.assertEqual(len(self.app.dataframe), 0)

    def test_no_show_disabled_at_14_enabled_at_15_and_updates_display(self):
        self.unlock()
        self.assertTrue(self.button("Mark no-show").disabled)
        self.now = self.start + timedelta(minutes=15)
        self.button("Refresh staff overview").click().run()
        self.assertFalse(self.button("Mark no-show").disabled)
        self.button("Mark no-show").click().run()
        self.assertEqual(len(self.app.exception), 0)
        self.assertEqual(self.app.dataframe[0].value["Status"].tolist(), ["No-show"])
        self.assertTrue(self.button("Cancel reservation").disabled)
        self.assertTrue(self.button("Mark no-show").disabled)
        self.assertTrue(all(self.app.dataframe[1].value["Availability"] == "Free"))

    def test_cancel_updates_display_and_disables_both_actions(self):
        self.unlock()
        self.assertFalse(self.button("Cancel reservation").disabled)
        self.button("Cancel reservation").click().run()
        self.assertEqual(len(self.app.exception), 0)
        self.assertEqual(self.app.dataframe[0].value["Status"].tolist(), ["Cancelled"])
        self.assertTrue(self.button("Cancel reservation").disabled)
        self.assertTrue(self.button("Mark no-show").disabled)
        self.assertTrue(all(self.app.dataframe[1].value["Availability"] == "Free"))

    def test_selected_time_does_not_override_actual_action_clock(self):
        self.unlock()
        self.app.time_input(key="staff_time").set_value(self.start.replace(hour=22).time()).run()
        self.assertTrue(self.button("Mark no-show").disabled)
        self.now = self.start + timedelta(hours=2)
        self.button("Refresh staff overview").click().run()
        self.assertTrue(self.button("Cancel reservation").disabled)

    def test_date_filter_empty_day_and_manual_refresh(self):
        self.unlock()
        self.app.date_input(key="staff_date").set_value(self.start.date() + timedelta(days=1)).run()
        self.assertEqual(len(self.app.dataframe), 1)  # Tables only.
        self.assertTrue(all(self.app.dataframe[0].value["Availability"] == "Free"))
        self.app.date_input(key="staff_date").set_value(self.start.date()).run()
        create_booking(self.path, self.settings, name="New Test Guest", phone="456", email="",
                       party_size=2, start=self.start, now=self.start)
        self.button("Refresh staff overview").click().run()
        self.assertEqual(len(self.app.exception), 0)
        self.assertEqual(len(self.app.dataframe[0].value), 2)


if __name__ == "__main__":
    unittest.main()
