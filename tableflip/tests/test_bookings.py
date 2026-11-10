"""Run with python -m unittest discover -s tableflip/tests -v."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
import tempfile
from threading import Barrier
import unittest
from unittest.mock import patch

from tableflip.allocation import choose_table, load_settings, ValidationError
from tableflip.database import (
    BookingStorageError, NoTableAvailable, connect, create_booking,
    initialize_database,
)


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "test.db"
        self.settings = load_settings()
        initialize_database(self.path)
        # Fixed Friday and clock: historical acceptance examples remain repeatable.
        self.start = datetime(2026, 10, 23, 19)
        self.now = datetime(2026, 10, 23, 10)

    def book(self, **changes):
        arguments = dict(name="Test Guest", phone="123", email="", party_size=2,
                         start=self.start, now=self.now)
        arguments.update(changes)
        return create_booking(self.path, self.settings, **arguments)

    def rows(self):
        connection = connect(self.path)
        try:
            return connection.execute("SELECT * FROM reservations").fetchall()
        finally:
            connection.close()

    def occupy(self, tables, status="Confirmed"):
        """Create controlled fixtures without using any demonstration database."""
        connection = connect(self.path)
        try:
            for table in tables:
                connection.execute("""
                    INSERT INTO reservations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (f"fixture-{table}", "Fixture", "123", "", 2, table,
                      self.start.isoformat(), (self.start + timedelta(hours=2)).isoformat(), status))
        finally:
            connection.close()

    def test_layout_and_smallest_suitable_tables(self):
        self.assertEqual(len(self.settings["tables"]), 12)
        self.assertEqual(sum(self.settings["tables"].values()), 50)
        for party, expected in [(1, "T1"), (2, "T1"), (3, "T5"), (4, "T5"),
                                (5, "T9"), (6, "T9"), (7, "T12"), (8, "T12")]:
            with self.subTest(party=party):
                self.assertEqual(choose_table(self.settings["tables"], party, set()), expected)
        self.assertEqual(choose_table(self.settings["tables"], 6, {"T9"}), "T10")

    def test_default_duration_confirmation_and_persistence(self):
        booking = self.book(party_size=4)
        self.assertEqual(booking["table_id"], "T5")
        self.assertTrue(booking["reference"].startswith("TF-"))
        self.assertEqual(booking["end_time"], "2026-10-23T21:00:00")
        initialize_database(self.path)  # Reopening must not clear saved data.
        self.assertEqual(dict(self.rows()[0]), booking)

    def test_overlap_and_exact_boundary(self):
        first = self.book(start=self.start.replace(hour=18))
        self.assertEqual(first["table_id"], "T1")
        self.assertEqual(self.book(start=self.start.replace(hour=19, minute=45))["table_id"], "T2")
        self.assertEqual(self.book(start=self.start.replace(hour=20))["table_id"], "T1")

    def test_requested_stay_surrounds_existing_booking(self):
        self.book(duration=60)
        self.assertEqual(self.book(start=self.start.replace(hour=18, minute=30))["table_id"], "T2")

    def test_request_ending_at_existing_start(self):
        self.book()
        self.assertEqual(self.book(start=self.start.replace(hour=17))["table_id"], "T1")

    def test_no_suitable_table_and_no_combining(self):
        self.occupy([f"T{number}" for number in range(3, 13)])
        for party in (3, 4):
            with self.subTest(party=party), self.assertRaises(NoTableAvailable):
                self.book(party_size=party)
        self.assertEqual(len(self.rows()), 10)

    def test_inactive_statuses_do_not_block(self):
        self.occupy(["T1"], "Cancelled")
        self.occupy(["T2"], "No-show")
        self.assertEqual(self.book()["table_id"], "T1")
        self.assertEqual(self.book()["table_id"], "T2")

    def test_invalid_requests_save_nothing(self):
        invalid = [dict(name="  "), dict(phone="", email=" "), dict(party_size=9),
                   dict(party_size=0), dict(duration=150), dict(duration=75),
                   dict(start=datetime(2026, 10, 26, 19)),
                   dict(start=self.start.replace(hour=21, minute=30)),
                   dict(start=self.start.replace(hour=10, minute=45)),
                   dict(start=self.start.replace(minute=7))]
        for changes in invalid:
            with self.subTest(changes=changes), self.assertRaises(ValidationError):
                self.book(**changes)
        self.assertEqual(len(self.rows()), 0)

    def test_allowed_durations_contact_and_closing_boundary(self):
        for minutes in (60, 90, 120):
            with self.subTest(minutes=minutes):
                start = self.start.replace(hour=23) - timedelta(minutes=minutes)
                booking = self.book(phone="", email="test@example.invalid",
                                    start=start, duration=minutes)
                self.assertEqual(booking["end_time"], "2026-10-23T23:00:00")

    def test_walk_in_and_past_time_boundary(self):
        self.book(now=self.start.replace(minute=7))
        self.book(now=self.start.replace(minute=15))
        with self.assertRaises(ValidationError):
            self.book(start=self.start.replace(hour=18, minute=45),
                      now=self.start.replace(minute=7))
        with self.assertRaises(ValidationError):
            self.book(now=self.start.replace(minute=15, second=1))
        self.assertEqual(len(self.rows()), 2)

    def test_failed_insert_leaves_no_booking(self):
        connection = connect(self.path)
        connection.execute("""CREATE TRIGGER fail_save BEFORE INSERT ON reservations
                              BEGIN SELECT RAISE(ABORT, 'simulated write failure'); END""")
        connection.close()
        with self.assertRaises(BookingStorageError):
            self.book()
        self.assertEqual(len(self.rows()), 0)

    def test_failed_commit_rolls_back_insert(self):
        class FailingCommit(sqlite3.Connection):
            def execute(self, sql, parameters=()):
                if sql == "COMMIT":
                    raise sqlite3.OperationalError("simulated commit failure")
                return super().execute(sql, parameters)

        connection = sqlite3.connect(self.path, isolation_level=None, factory=FailingCommit)
        connection.row_factory = sqlite3.Row
        with patch("tableflip.database.connect", return_value=connection):
            with self.assertRaises(BookingStorageError):
                self.book()
        self.assertEqual(len(self.rows()), 0)
        self.assertEqual(self.book()["table_id"], "T1")  # Lock released too.

    def test_lock_timeout_is_technical_failure(self):
        connection = connect(self.path)
        try:
            connection.execute("BEGIN IMMEDIATE")
            with self.assertRaises(BookingStorageError):
                self.book(timeout=0.05)
        finally:
            connection.execute("ROLLBACK")
            connection.close()
        self.assertEqual(len(self.rows()), 0)

    def test_two_connections_compete_for_last_table(self):
        self.occupy([f"T{number}" for number in range(2, 13)])
        barrier = Barrier(2)

        def request():
            barrier.wait(timeout=5)
            try:
                return self.book()["table_id"]
            except NoTableAvailable:
                return "unavailable"

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(request) for _ in range(2)]
            results = [future.result(timeout=10) for future in futures]
        self.assertCountEqual(results, ["T1", "unavailable"])
        self.assertEqual(len(self.rows()), 12)


if __name__ == "__main__":
    unittest.main()
