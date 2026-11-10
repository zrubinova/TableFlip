"""Programmatic Streamlit checks; these are not manual browser tests."""

from datetime import datetime
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from tableflip.database import (
    BookingStorageError, NoTableAvailable, TECHNICAL_MESSAGE, connect,
    initialize_database,
)


class AppTests(unittest.TestCase):
    def test_form_to_real_temporary_database(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ui-test.db"
            initialize_database(path)
            with patch("tableflip.database.DEFAULT_DATABASE", path), patch(
                "tableflip.database.initialize_database"
            ), patch("tableflip.allocation.restaurant_now",
                     return_value=datetime(2026, 10, 23, 10)):
                app = AppTest.from_file(str(Path(__file__).parents[1] / "app.py")).run()
                app.text_input[0].set_value("Test Guest")
                app.text_input[2].set_value("test@example.invalid")
                app.number_input[0].set_value(4)
                app.selectbox[0].set_value(datetime(2026, 10, 23, 19).time())
                app.button[0].click().run()
            self.assertEqual(len(app.exception), 0)
            self.assertEqual(app.success[0].value, "Booking confirmed")
            connection = connect(path)
            try:
                rows = connection.execute("SELECT * FROM reservations").fetchall()
            finally:
                connection.close()
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["table_id"], "T5")
            self.assertEqual(rows[0]["end_time"], "2026-10-23T21:00:00")
            self.assertTrue(any(rows[0]["reference"] in element.value for element in app.markdown))

    def submit(self, outcome):
        # Stub both database operations: never initialize or write demo data.
        with patch("tableflip.database.initialize_database"), patch(
            "tableflip.database.create_booking", side_effect=outcome
        ):
            app = AppTest.from_file(str(Path(__file__).parents[1] / "app.py")).run()
            app.text_input[0].set_value("Test Guest")
            app.text_input[1].set_value("123")
            app.button[0].click().run()
        self.assertEqual(len(app.exception), 0)
        return app

    def test_storage_failure_never_displays_confirmation(self):
        app = self.submit(BookingStorageError(TECHNICAL_MESSAGE))
        self.assertEqual(len(app.success), 0)
        self.assertEqual(app.error[0].value, TECHNICAL_MESSAGE)

    def test_unavailable_is_distinct_from_technical_failure(self):
        app = self.submit(NoTableAvailable("Sorry, no suitable table."))
        self.assertEqual(len(app.success), 0)
        self.assertEqual(len(app.error), 0)
        self.assertEqual(app.warning[0].value, "Sorry, no suitable table.")

    def test_success_displays_returned_confirmation(self):
        booking = dict(reference="TF-TEST", table_id="T5",
                       start_time="2026-10-23T19:00:00", end_time="2026-10-23T21:00:00")
        app = self.submit(lambda *args, **kwargs: booking)
        self.assertEqual(app.success[0].value, "Booking confirmed")
        text = "\n".join(element.value for element in app.markdown)
        for expected in ("TF-TEST", "Table T5", "23 October 2026", "19:00 - 21:00"):
            self.assertIn(expected, text)
