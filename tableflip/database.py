"""Persistent storage. Every booking writer must use create_booking."""

from datetime import datetime, time, timedelta
from pathlib import Path
import sqlite3
from uuid import uuid4

from .allocation import choose_table, restaurant_now, status_change_error, validate_booking

DEFAULT_DATABASE = Path(__file__).parent / "data" / "tableflip.db"
TECHNICAL_MESSAGE = "Booking unavailable, please try again later or call the restaurant"


class NoTableAvailable(Exception):
    """Valid request, but all suitable tables overlap this stay."""


class BookingStorageError(Exception):
    """A technical failure prevented a database operation."""


class InvalidStatusChange(ValueError):
    """The booking does not exist or a requested staff action is not permitted."""


def connect(database_path, timeout=5.0):
    # Explicit SQL controls transactions: do not rely on implicit BEGIN behavior.
    connection = sqlite3.connect(database_path, timeout=timeout, isolation_level=None)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(database_path=DEFAULT_DATABASE):
    connection = None
    try:
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        connection = connect(database_path)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                reference TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                party_size INTEGER NOT NULL CHECK (party_size BETWEEN 1 AND 8),
                table_id TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Confirmed'
                    CHECK (status IN ('Confirmed', 'Cancelled', 'No-show')),
                CHECK (start_time < end_time)
            )
        """)
    except (sqlite3.Error, OSError) as error:
        raise BookingStorageError(TECHNICAL_MESSAGE) from error
    finally:
        if connection is not None:
            connection.close()


def create_booking(database_path, settings, *, name, phone, email, party_size,
                   start, duration=None, now=None, timeout=5.0):
    """Return confirmation data ONLY after COMMIT. Never return tentative data."""
    end = validate_booking(name, phone, email, party_size, start, duration, settings, now)
    connection = None
    try:
        connection = connect(database_path, timeout)
        # Take the write lock BEFORE reading availability. A competing writer
        # waits, then sees this booking after its commit.
        connection.execute("BEGIN IMMEDIATE")
        occupied = connection.execute("""
            SELECT table_id FROM reservations
            WHERE status = 'Confirmed' AND start_time < ? AND end_time > ?
        """, (end.isoformat(), start.isoformat())).fetchall()
        table = choose_table(settings["tables"], party_size,
                             {row["table_id"] for row in occupied})
        if table is None:
            date_text = start.strftime("%d %B %Y").lstrip("0")
            raise NoTableAvailable(
                f"Sorry, we have no free table for {party_size} guests on "
                f"{date_text} at {start:%H:%M}. Please try another time."
            )
        booking = {
            "reference": "TF-" + uuid4().hex.upper(),
            "name": name.strip(), "phone": phone.strip(), "email": email.strip(),
            "party_size": party_size, "table_id": table,
            "start_time": start.isoformat(), "end_time": end.isoformat(),
            "status": "Confirmed",
        }
        connection.execute("""
            INSERT INTO reservations
                (reference, name, phone, email, party_size, table_id,
                 start_time, end_time, status)
            VALUES (:reference, :name, :phone, :email, :party_size, :table_id,
                    :start_time, :end_time, :status)
        """, booking)
        connection.execute("COMMIT")
        return booking
    except sqlite3.Error as error:
        raise BookingStorageError(TECHNICAL_MESSAGE) from error
    finally:
        if connection is not None:
            try:
                # Also rolls back the no-availability path and failed writes.
                if connection.in_transaction:
                    connection.execute("ROLLBACK")
            finally:
                connection.close()


def list_reservations(database_path, date):
    """Return every status for the selected day, in chronological order."""
    start = datetime.combine(date, time.min)
    end = start + timedelta(days=1)
    connection = None
    try:
        connection = connect(database_path)
        return [dict(row) for row in connection.execute("""
            SELECT * FROM reservations
            WHERE start_time >= ? AND start_time < ?
            ORDER BY start_time, reference
        """, (start.isoformat(), end.isoformat())).fetchall()]
    except sqlite3.Error as error:
        raise BookingStorageError("Staff overview unavailable. Please try again.") from error
    finally:
        if connection is not None:
            connection.close()


def change_booking_status(database_path, settings, reference, new_status, *, now=None):
    """Check the saved status/time under a write lock, then commit the change.

    The UI's displayed time may be stale. Check again here after acquiring the
    lock, using the restaurant clock (or a fixed clock supplied by tests).
    """
    connection = None
    try:
        connection = connect(database_path)
        connection.execute("BEGIN IMMEDIATE")
        booking = connection.execute(
            "SELECT * FROM reservations WHERE reference = ?", (reference,)
        ).fetchone()
        if booking is None:
            raise InvalidStatusChange("Reservation not found. Please refresh the overview.")
        current_time = restaurant_now(settings) if now is None else now
        reason = status_change_error(booking, new_status, current_time)
        if reason:
            raise InvalidStatusChange(reason)
        connection.execute(
            "UPDATE reservations SET status = ? WHERE reference = ?",
            (new_status, reference),
        )
        connection.execute("COMMIT")
    except sqlite3.Error as error:
        raise BookingStorageError("Reservation update unavailable. Please try again.") from error
    finally:
        if connection is not None:
            try:
                if connection.in_transaction:
                    connection.execute("ROLLBACK")
            finally:
                connection.close()
