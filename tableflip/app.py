"""Guest booking and demonstration staff interface. See README.md to run."""

from datetime import datetime, time, timedelta

import streamlit as st

from tableflip.allocation import (
    load_settings, restaurant_now, status_change_error, table_overview, ValidationError,
)
from tableflip.database import (
    DEFAULT_DATABASE, TECHNICAL_MESSAGE, BookingStorageError, NoTableAvailable,
    InvalidStatusChange, change_booking_status, create_booking, initialize_database,
    list_reservations,
)


def main():
    st.title("TableFlip")
    st.caption("Local only prototype")
    try:
        settings = load_settings()
        initialize_database()
    except (BookingStorageError, OSError, ValueError):
        st.error(TECHNICAL_MESSAGE)
        return

    now = restaurant_now(settings)
    guest_tab, staff_tab = st.tabs(["Book a table", "Demo access - not secure"])
    with guest_tab:
        booking_form(settings, now)
    with staff_tab:
        staff_view(settings, now)


def booking_form(settings, now):
    st.write("Tuesday–Sunday, 11:00–23:00. Groups of 1–8; one table per booking.")
    st.caption(f"Restaurant time: {now:%d %B %Y %H:%M} ({settings['timezone']}). "
               "For a walk-in, choose the current quarter-hour rounded down.")
    opening = datetime.combine(now.date(), time.fromisoformat(settings["opening_time"]))
    closing = datetime.combine(now.date(), time.fromisoformat(settings["closing_time"]))
    times = []
    slot = opening
    while slot < closing:
        times.append(slot.time())
        slot += timedelta(minutes=settings["start_interval_minutes"])

    with st.form("reservation"):
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        party_size = st.number_input("Guests", min_value=1, max_value=8, value=2, step=1)
        date = st.date_input("Date", value=now.date())
        start_time = st.selectbox("Start time", times, format_func=lambda value: value.strftime("%H:%M"))
        duration = st.selectbox("Duration", [None] + settings["allowed_durations"],
                                format_func=lambda value: "Default (120 minutes)" if value is None else f"{value} minutes")
        submitted = st.form_submit_button("Book a table")

    if submitted:
        try:
            booking = create_booking(
                DEFAULT_DATABASE, settings, name=name, phone=phone, email=email,
                party_size=party_size, start=datetime.combine(date, start_time),
                duration=duration,
            )
        except ValidationError as error:
            st.error(str(error))
        except NoTableAvailable as error:
            st.warning(str(error))
        except BookingStorageError:
            st.error(TECHNICAL_MESSAGE)
        else:
            # create_booking returns only after a successful database commit.
            start = datetime.fromisoformat(booking["start_time"])
            end = datetime.fromisoformat(booking["end_time"])
            st.success("Booking confirmed")
            st.write(f"Reference: {booking['reference']}")
            st.write(f"Table {booking['table_id']}")
            st.write(start.strftime("%d %B %Y").lstrip("0"))
            st.write(f"{start:%H:%M} - {end:%H:%M}")


def staff_view(settings, now):
    st.subheader("Staff overview")
    st.caption("Demo access - not secure. Use made-up guest details only.")
    password = st.text_input("Staff password", type="password", key="staff_password")
    # Streamlit executes both tabs. Do not query or render booking data until
    # this session's input matches the settings password.
    if not settings.get("staff_password") or password != settings["staff_password"]:
        if password:
            st.error("Incorrect demo password.")
        return

    date = st.date_input("Staff date", value=now.date(), key="staff_date")
    selected_time = st.time_input(
        "Table availability at", value=now.time().replace(second=0, microsecond=0),
        step=timedelta(minutes=15), key="staff_time",
    )
    st.button("Refresh staff overview")  # A button click reruns and reloads the data.
    st.caption("Refresh to load new bookings and recheck action times. "
               "Action eligibility uses the actual restaurant time, not the selected time.")
    try:
        bookings = list_reservations(DEFAULT_DATABASE, date)
        if bookings:
            by_reference = {booking["reference"]: booking for booking in bookings}
            reference = st.selectbox("Reservation to update", list(by_reference),
                                     key="staff_reservation")
            selected = by_reference[reference]
            cancel_reason = status_change_error(selected, "Cancelled", now)
            no_show_reason = status_change_error(selected, "No-show", now)
            cancel = st.button("Cancel reservation", disabled=cancel_reason is not None,
                               help=cancel_reason)
            no_show = st.button("Mark no-show", disabled=no_show_reason is not None,
                                help=no_show_reason)
            if cancel or no_show:
                change_booking_status(DEFAULT_DATABASE, settings, reference,
                                      "Cancelled" if cancel else "No-show")
                # Rerun after commit so the list, availability and disabled
                # buttons all reflect the new status immediately.
                st.session_state["staff_notice"] = "Reservation status updated."
                st.rerun()
        notice = st.session_state.pop("staff_notice", None)
        if notice:
            st.success(notice)
        st.write("Reservations")
        if bookings:
            st.dataframe([
                {"Reference": booking["reference"], "Table": booking["table_id"],
                 "Guests": booking["party_size"], "Name": booking["name"],
                 "Phone": booking["phone"], "Email": booking["email"],
                 "Start": datetime.fromisoformat(booking["start_time"]).strftime("%H:%M"),
                 "End": datetime.fromisoformat(booking["end_time"]).strftime("%H:%M"),
                 "Status": booking["status"]}
                for booking in bookings
            ], hide_index=True)
        else:
            st.info("No reservations for this date.")
        st.write("Tables")
        st.dataframe(table_overview(settings["tables"], bookings,
                                    datetime.combine(date, selected_time)), hide_index=True)
    except InvalidStatusChange as error:
        st.warning(str(error))
    except BookingStorageError as error:
        st.error(str(error))


if __name__ == "__main__":
    main()
