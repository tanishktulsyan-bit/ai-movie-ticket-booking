# models/show_model.py — Data access layer for SHOW_DETAILS table

from database.db import execute_query


def get_all_shows():
    """
    Return shows joined with movie & theatre info for display.
    Uses JOIN + aggregate-friendly columns.
    """
    sql = """
        SELECT
            sd.show_id,
            m.title        AS movie_title,
            m.genre,
            t.name         AS theatre_name,
            t.location,
            sd.show_date,
            sd.show_time,
            sd.ticket_price,
            t.total_seats,
            sd.available_seats,
            (t.total_seats - sd.available_seats) AS booked_seats
        FROM SHOW_DETAILS sd
        JOIN MOVIE   m ON sd.movie_id   = m.movie_id
        JOIN THEATRE t ON sd.theatre_id = t.theatre_id
        ORDER BY sd.show_date, sd.show_time
    """
    return execute_query(sql, fetch=True) or []


def get_show_by_id(show_id):
    """Return full show detail (with movie & theatre) by show_id."""
    sql = """
        SELECT
            sd.*,
            m.title        AS movie_title,
            m.duration,
            t.name         AS theatre_name,
            t.location,
            t.total_seats
        FROM SHOW_DETAILS sd
        JOIN MOVIE   m ON sd.movie_id   = m.movie_id
        JOIN THEATRE t ON sd.theatre_id = t.theatre_id
        WHERE sd.show_id = %s
    """
    return execute_query(sql, (show_id,), fetchone=True)


def create_show(movie_id, theatre_id, show_date, show_time, ticket_price, available_seats):
    """Insert a new show; return the new show_id."""
    sql = """
        INSERT INTO SHOW_DETAILS
            (movie_id, theatre_id, show_date, show_time, ticket_price, available_seats)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    return execute_query(
        sql,
        (movie_id, theatre_id, show_date, show_time, ticket_price, available_seats)
    )


def update_available_seats(show_id, seats_to_reduce):
    """Manually reduce available_seats (backup for trigger)."""
    sql = """
        UPDATE SHOW_DETAILS
        SET available_seats = available_seats - %s
        WHERE show_id = %s
    """
    return execute_query(sql, (seats_to_reduce, show_id))