# services/show_service.py — Business logic for Show module

from models.show_model import get_all_shows, get_show_by_id, create_show
from models.movie_model import get_all_movies
from models.theatre_model import get_all_theatres


def fetch_all_shows():
    return get_all_shows()


def fetch_show(show_id):
    return get_show_by_id(show_id)


def fetch_movies_and_theatres():
    """Helper to populate form dropdowns."""
    return get_all_movies(), get_all_theatres()


def create_new_show(data):
    """
    Validate and create a show.
    available_seats defaults to the theatre's total_seats.
    Returns: (success, message, show_id|None)
    """
    movie_id   = data.get('movie_id')
    theatre_id = data.get('theatre_id')
    show_date  = data.get('show_date', '').strip()
    show_time  = data.get('show_time', '').strip()
    ticket_price = data.get('ticket_price', 0)

    if not all([movie_id, theatre_id, show_date, show_time, ticket_price]):
        return False, "All fields are required.", None

    try:
        movie_id     = int(movie_id)
        theatre_id   = int(theatre_id)
        ticket_price = float(ticket_price)
    except ValueError:
        return False, "Invalid numeric values.", None

    # available_seats = theatre's total capacity
    from models.theatre_model import get_theatre_by_id
    theatre = get_theatre_by_id(theatre_id)
    if not theatre:
        return False, "Theatre not found.", None

    available_seats = theatre['total_seats']

    show_id = create_show(movie_id, theatre_id, show_date, show_time,
                          ticket_price, available_seats)
    if show_id:
        return True, "Show created successfully!", show_id
    return False, "Database error — could not create show.", None