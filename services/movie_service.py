# services/movie_service.py — Business logic for Movie module

from models.movie_model import get_all_movies, get_movie_by_id, add_movie


def fetch_all_movies():
    return get_all_movies()


def fetch_movie(movie_id):
    return get_movie_by_id(movie_id)


def create_movie(data):
    """
    Validate and create a new movie.
    data: dict with keys title, genre, language, duration, rating, release_date
    Returns: (success: bool, message: str, movie_id: int|None)
    """
    title        = data.get('title', '').strip()
    genre        = data.get('genre', '').strip()
    language     = data.get('language', '').strip()
    duration     = data.get('duration', 0)
    rating       = data.get('rating', 0.0)
    release_date = data.get('release_date', '')

    # Basic validation
    if not all([title, genre, language, duration, release_date]):
        return False, "All fields are required.", None

    try:
        duration = int(duration)
        rating   = float(rating)
    except ValueError:
        return False, "Duration must be an integer; Rating must be a number.", None

    if duration <= 0:
        return False, "Duration must be positive.", None

    if not (0.0 <= rating <= 10.0):
        return False, "Rating must be between 0 and 10.", None

    movie_id = add_movie(title, genre, language, duration, rating, release_date)
    if movie_id:
        return True, f"Movie '{title}' added successfully!", movie_id
    return False, "Database error — could not add movie.", None