# models/theatre_model.py — Data access layer for THEATRE table

from database.db import execute_query


def get_all_theatres():
    """Return all theatres."""
    sql = "SELECT * FROM THEATRE ORDER BY name"
    return execute_query(sql, fetch=True) or []


def get_theatre_by_id(theatre_id):
    """Return a single theatre by primary key."""
    sql = "SELECT * FROM THEATRE WHERE theatre_id = %s"
    return execute_query(sql, (theatre_id,), fetchone=True)


def add_theatre(name, location, total_seats):
    """Insert a new theatre; return the new theatre_id."""
    sql = """
        INSERT INTO THEATRE (name, location, total_seats)
        VALUES (%s, %s, %s)
    """
    return execute_query(sql, (name, location, total_seats))