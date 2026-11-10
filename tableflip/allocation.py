"""Booking rules and table selection, independent of Streamlit and SQLite."""

from datetime import datetime, time, timedelta
from pathlib import Path
import tomllib
from zoneinfo import ZoneInfo


class ValidationError(ValueError):
    """Guest input breaks a booking rule."""


def load_settings():
    with Path(__file__).with_name("settings.toml").open("rb") as file:
        return tomllib.load(file)


def restaurant_now(settings):
    # Reservations use wall-clock times in this one restaurant's timezone.
    return datetime.now(ZoneInfo(settings["timezone"])).replace(tzinfo=None)


def validate_booking(name, phone, email, party_size, start, duration, settings, now=None):
    """Return the end time, or raise an explanation suitable for the form."""
    if not name.strip():
        raise ValidationError("Please enter your name.")
    if not phone.strip() and not email.strip():
        raise ValidationError("Please enter a phone number or email address.")
    if type(party_size) is not int or not 1 <= party_size <= settings["maximum_party_size"]:
        raise ValidationError("Please book for 1–8 guests. For larger groups, call the restaurant.")
    duration = settings["default_duration"] if duration is None else duration
    if type(duration) is not int or duration not in settings["allowed_durations"]:
        raise ValidationError("Please choose a duration of 60, 90 or 120 minutes.")
    if start.weekday() not in settings["open_days"]:
        raise ValidationError("The restaurant is closed on Mondays.")
    if start.minute % settings["start_interval_minutes"] or start.second or start.microsecond:
        raise ValidationError("Start times must be on a quarter-hour.")
    now = restaurant_now(settings) if now is None else now
    if start < now - timedelta(minutes=settings["past_tolerance_minutes"]):
        raise ValidationError("The start time is more than 15 minutes in the past.")
    end = start + timedelta(minutes=duration)
    opens = datetime.combine(start.date(), time.fromisoformat(settings["opening_time"]))
    closes = datetime.combine(start.date(), time.fromisoformat(settings["closing_time"]))
    if start < opens or end > closes:
        raise ValidationError("Your stay must start and end between 11:00 and 23:00.")
    return end


def choose_table(tables, party_size, occupied_tables):
    """Smallest suitable free table; break ties by numeric table number."""
    ordered = sorted(tables, key=lambda table: (tables[table], int(table[1:])))
    for table in ordered:
        if tables[table] >= party_size and table not in occupied_tables:
            return table
    return None


def table_overview(tables, bookings, at):
    """Describe each table at one instant; an end time itself is already free."""
    occupied = {
        booking["table_id"]: booking["reference"]
        for booking in bookings
        if booking["status"] == "Confirmed"
        and datetime.fromisoformat(booking["start_time"]) <= at
        < datetime.fromisoformat(booking["end_time"])
    }
    return [
        {"Table": table, "Seats": tables[table],
         "Availability": "Taken" if table in occupied else "Free",
         "Booking reference": occupied.get(table, "")}
        for table in sorted(tables, key=lambda value: int(value[1:]))
    ]


def status_change_error(booking, new_status, now):
    """Shared UI/database rules. None means the change is currently permitted."""
    if new_status not in ("Cancelled", "No-show"):
        return "Only cancellation or no-show changes are allowed."
    if booking["status"] != "Confirmed":
        return "Only Confirmed reservations can be changed."
    if new_status == "Cancelled" and now >= datetime.fromisoformat(booking["end_time"]):
        return "Cancellation is only allowed before the reservation ends."
    if new_status == "No-show" and now < (
        datetime.fromisoformat(booking["start_time"]) + timedelta(minutes=15)
    ):
        return "No-show is only allowed from 15 minutes after the start time."
    return None
