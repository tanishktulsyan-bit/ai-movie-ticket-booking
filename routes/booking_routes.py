# routes/booking_routes.py — Booking Blueprint

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.booking_service import fetch_all_bookings, make_booking, fetch_booking_stats
from services.show_service import fetch_all_shows

booking_bp = Blueprint('bookings', __name__, url_prefix='/bookings')


@booking_bp.route('/')
def list_bookings():
    bookings = fetch_all_bookings()
    shows    = fetch_all_shows()
    stats    = fetch_booking_stats()
    return render_template('booking.html', bookings=bookings,
                           shows=shows, stats=stats)


@booking_bp.route('/book', methods=['POST'])
def book_ticket():
    success, message, _ = make_booking(request.form)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('bookings.list_bookings'))