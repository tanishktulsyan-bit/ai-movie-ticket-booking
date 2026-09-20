# models/prediction_model.py — Data access layer for CROWD_PREDICTION table

from database.db import execute_query


def save_prediction(show_id, predicted_crowd, confidence_score, crowd_level):
    """Persist a prediction result."""
    sql = """
        INSERT INTO CROWD_PREDICTION
            (show_id, predicted_crowd, confidence_score, crowd_level)
        VALUES (%s, %s, %s, %s)
    """
    return execute_query(sql, (show_id, predicted_crowd, confidence_score, crowd_level))


def get_all_predictions():
    """Return all predictions joined with show, movie, theatre info."""
    sql = """
        SELECT
            cp.prediction_id,
            m.title             AS movie_title,
            t.name              AS theatre_name,
            sd.show_date,
            sd.show_time,
            t.total_seats,
            cp.predicted_crowd,
            cp.confidence_score,
            cp.crowd_level,
            cp.prediction_date
        FROM CROWD_PREDICTION cp
        JOIN SHOW_DETAILS sd ON cp.show_id    = sd.show_id
        JOIN MOVIE        m  ON sd.movie_id   = m.movie_id
        JOIN THEATRE      t  ON sd.theatre_id = t.theatre_id
        ORDER BY cp.prediction_date DESC
    """
    return execute_query(sql, fetch=True) or []


def get_historical_bookings_for_show(show_id):
    """
    Aggregate historical booking data for a specific show.
    Used by the AI prediction engine.
    """
    sql = """
        SELECT
            sd.show_id,
            t.total_seats,
            sd.available_seats,
            (t.total_seats - sd.available_seats)     AS seats_sold,
            COUNT(b.booking_id)                       AS booking_count,
            COALESCE(SUM(b.seats_booked), 0)          AS total_booked,
            COALESCE(AVG(b.seats_booked), 0)          AS avg_per_booking
        FROM SHOW_DETAILS sd
        JOIN THEATRE t ON sd.theatre_id = t.theatre_id
        LEFT JOIN BOOKING b ON sd.show_id = b.show_id AND b.status = 'confirmed'
        WHERE sd.show_id = %s
        GROUP BY sd.show_id, t.total_seats, sd.available_seats
    """
    return execute_query(sql, (show_id,), fetchone=True)


def get_avg_booking_for_similar_shows(movie_id, theatre_id):
    """
    Return average seats sold for the same movie in the same theatre.
    Core data used by the ML-lite prediction algorithm.
    """
    sql = """
        SELECT
            COALESCE(AVG(t.total_seats - sd.available_seats), 0) AS avg_seats_sold,
            COUNT(sd.show_id)                                      AS sample_size
        FROM SHOW_DETAILS sd
        JOIN THEATRE t ON sd.theatre_id = t.theatre_id
        WHERE sd.movie_id = %s AND sd.theatre_id = %s
    """
    return execute_query(sql, (movie_id, theatre_id), fetchone=True)