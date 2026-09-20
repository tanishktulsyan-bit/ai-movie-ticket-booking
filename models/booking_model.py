# models/booking_model.py — Data access layer for BOOKING table

from database.db import execute_query


def get_all_bookings():
    """Return bookings with customer + show + movie info (JOIN report)."""
    sql = """
        SELECT
            b.booking_id,
            c.name         AS customer_name,
            c.email,
            m.title        AS movie_title,
            t.name         AS theatre_name,
            sd.show_date,
            sd.show_time,
            b.seats_booked,
            b.total_amount,
            b.status,
            b.booking_date
        FROM BOOKING b
        JOIN CUSTOMER    c  ON b.customer_id = c.customer_id
        JOIN SHOW_DETAILS sd ON b.show_id    = sd.show_id
        JOIN MOVIE       m  ON sd.movie_id   = m.movie_id
        JOIN THEATRE     t  ON sd.theatre_id = t.theatre_id
        ORDER BY b.booking_date DESC
    """
    return execute_query(sql, fetch=True) or []


def create_booking(show_id, customer_id, seats_booked, total_amount):
    """Insert a booking; DB trigger reduces available_seats automatically."""
    sql = """
        INSERT INTO BOOKING (show_id, customer_id, seats_booked, total_amount)
        VALUES (%s, %s, %s, %s)
    """
    return execute_query(sql, (show_id, customer_id, seats_booked, total_amount))


def get_booking_stats():
    """
    Aggregate query: total bookings, total revenue, avg seats per booking.
    Used on the dashboard.
    """
    sql = """
        SELECT
            COUNT(*)             AS total_bookings,
            SUM(total_amount)    AS total_revenue,
            AVG(seats_booked)    AS avg_seats,
            MAX(seats_booked)    AS max_seats
        FROM BOOKING
        WHERE status = 'confirmed'
    """
    return execute_query(sql, fetchone=True)