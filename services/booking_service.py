# services/booking_service.py — Business logic for Booking module

from models.booking_model import get_all_bookings, create_booking, get_booking_stats
from models.show_model import get_show_by_id
from models.customer_model import get_or_create_customer


def fetch_all_bookings():
    return get_all_bookings()


def fetch_booking_stats():
    return get_booking_stats()


def make_booking(data):
    """
    End-to-end booking flow:
      1. Validate input
      2. Check seat availability
      3. Upsert customer
      4. Insert booking (DB trigger reduces available_seats)

    Returns: (success, message, booking_id|None)
    """
    show_id      = data.get('show_id')
    seats_booked = data.get('seats_booked', 0)
    name         = data.get('customer_name', '').strip()
    email        = data.get('customer_email', '').strip()
    phone        = data.get('customer_phone', '').strip()

    # ── Validate ──────────────────────────────────
    if not all([show_id, seats_booked, name, email, phone]):
        return False, "All fields are required.", None

    try:
        show_id      = int(show_id)
        seats_booked = int(seats_booked)
    except ValueError:
        return False, "Invalid numeric values.", None

    if seats_booked <= 0:
        return False, "Seats booked must be at least 1.", None

    # ── Check availability ─────────────────────────
    show = get_show_by_id(show_id)
    if not show:
        return False, "Show not found.", None

    if seats_booked > show['available_seats']:
        return False, (
            f"Only {show['available_seats']} seat(s) available. "
            f"You requested {seats_booked}."
        ), None

    # ── Compute total ──────────────────────────────
    total_amount = seats_booked * float(show['ticket_price'])

    # ── Upsert customer ────────────────────────────
    customer_id = get_or_create_customer(name, email, phone)
    if not customer_id:
        return False, "Could not create/retrieve customer.", None

    # ── Insert booking (trigger fires automatically) ─
    booking_id = create_booking(show_id, customer_id, seats_booked, total_amount)
    if booking_id:
        return True, (
            f"Booking confirmed! {seats_booked} seat(s) booked for ₹{total_amount:.2f}."
        ), booking_id

    return False, "Database error — booking failed.", None