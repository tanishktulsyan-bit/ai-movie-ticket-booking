# models/movie_model.py — Data access layer for MOVIE table

from database.db import execute_query


def get_all_movies():
    """Return all movies ordered by release date (newest first)."""
    sql = "SELECT * FROM MOVIE ORDER BY release_date DESC"
    return execute_query(sql, fetch=True) or []


def get_movie_by_id(movie_id):
    """Return a single movie by primary key."""
    sql = "SELECT * FROM MOVIE WHERE movie_id = %s"
    return execute_query(sql, (movie_id,), fetchone=True)


def add_movie(title, genre, language, duration, rating, release_date):
    """Insert a new movie; return the new movie_id."""
    sql = """
        INSERT INTO MOVIE (title, genre, language, duration, rating, release_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    return execute_query(sql, (title, genre, language, duration, rating, release_date))