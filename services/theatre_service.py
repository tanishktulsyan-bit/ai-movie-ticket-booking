# services/theatre_service.py — Business logic for Theatre module

from models.theatre_model import get_all_theatres, get_theatre_by_id, add_theatre


def fetch_all_theatres():
    return get_all_theatres()


def fetch_theatre(theatre_id):
    return get_theatre_by_id(theatre_id)


def create_theatre(data):
    """
    Validate and create a new theatre.
    Returns: (success, message, theatre_id|None)
    """
    name        = data.get('name', '').strip()
    location    = data.get('location', '').strip()
    total_seats = data.get('total_seats', 0)

    if not all([name, location, total_seats]):
        return False, "All fields are required.", None

    try:
        total_seats = int(total_seats)
    except ValueError:
        return False, "Total seats must be a number.", None

    if total_seats <= 0:
        return False, "Total seats must be a positive number.", None

    theatre_id = add_theatre(name, location, total_seats)
    if theatre_id:
        return True, f"Theatre '{name}' added successfully!", theatre_id
    return False, "Database error — could not add theatre.", None