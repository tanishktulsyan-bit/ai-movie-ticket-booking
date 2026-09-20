# services/prediction_service.py — AI Crowd Prediction Engine
#
# ALGORITHM (ML-lite / Average-based):
# ─────────────────────────────────────────────────────────────────
# Step 1  Pull current booking data for the show (seats sold so far).
# Step 2  Pull historical average seats sold for similar shows
#         (same movie × same theatre).
# Step 3  Weighted blend:
#           predicted = 0.6 × current_sold + 0.4 × historical_avg
# Step 4  Confidence score derived from sample size — more past shows
#         → higher confidence (max 95 %).
# Step 5  Classify crowd level: Low / Medium / High / Housefull.
#
# HOW TO UPGRADE TO LINEAR REGRESSION (explained):
# ─────────────────────────────────────────────────────────────────
# Replace the weighted average with:
#   from sklearn.linear_model import LinearRegression
#   Features: [day_of_week, hour_of_show, genre_encoded, price, movie_rating]
#   Target  : seats_sold
# Train on historical BOOKING rows, then call model.predict([features]).
# ─────────────────────────────────────────────────────────────────

from models.prediction_model import (
    save_prediction,
    get_all_predictions,
    get_historical_bookings_for_show,
    get_avg_booking_for_similar_shows,
)
from models.show_model import get_show_by_id, get_all_shows


def fetch_all_predictions():
    return get_all_predictions()


def _classify_crowd(fill_pct: float) -> str:
    """
    Convert fill percentage into a human-readable crowd level.
    fill_pct is in range [0, 100].
    """
    if fill_pct >= 95:
        return 'Housefull'
    elif fill_pct >= 70:
        return 'High'
    elif fill_pct >= 40:
        return 'Medium'
    else:
        return 'Low'


def _compute_confidence(sample_size: int) -> float:
    """
    Confidence grows with more historical samples; cap at 95 %.
    Formula: confidence = min(95, 50 + sample_size * 5)
    """
    return min(95.0, 50.0 + sample_size * 5.0)


def predict_crowd(show_id: int):
    """
    Main prediction entry-point.
    Returns: (success, message, result_dict|None)
    """
    # ── 1. Load show details ───────────────────────
    show = get_show_by_id(show_id)
    if not show:
        return False, "Show not found.", None

    total_seats = show['total_seats']

    # ── 2. Current bookings for this show ──────────
    current_data = get_historical_bookings_for_show(show_id)
    if not current_data:
        return False, "Could not retrieve booking data.", None

    current_sold = int(current_data['seats_sold'] or 0)

    # ── 3. Historical average (same movie + theatre) ─
    hist = get_avg_booking_for_similar_shows(show['movie_id'], show['theatre_id'])
    hist_avg     = float(hist['avg_seats_sold'] or 0) if hist else 0.0
    sample_size  = int(hist['sample_size'] or 0) if hist else 0

    # ── 4. Weighted blend ──────────────────────────
    if sample_size > 1:
        # Enough history — blend current + historical
        predicted = int(0.6 * current_sold + 0.4 * hist_avg)
    else:
        # No history — fall back to current sold
        predicted = current_sold

    # Never predict beyond total capacity
    predicted = min(predicted, total_seats)

    # ── 5. Confidence & crowd level ───────────────
    confidence  = _compute_confidence(sample_size)
    fill_pct    = (predicted / total_seats * 100) if total_seats > 0 else 0
    crowd_level = _classify_crowd(fill_pct)

    # ── 6. Persist prediction ─────────────────────
    pred_id = save_prediction(show_id, predicted, confidence, crowd_level)

    result = {
        'show_id'          : show_id,
        'movie_title'      : show['movie_title'],
        'theatre_name'     : show['theatre_name'],
        'show_date'        : str(show['show_date']),
        'show_time'        : str(show['show_time']),
        'total_seats'      : total_seats,
        'current_sold'     : current_sold,
        'historical_avg'   : round(hist_avg, 1),
        'predicted_crowd'  : predicted,
        'fill_percentage'  : round(fill_pct, 1),
        'confidence_score' : confidence,
        'crowd_level'      : crowd_level,
        'sample_size'      : sample_size,
        'prediction_id'    : pred_id,
    }

    return True, "Prediction generated successfully!", result


def get_shows_for_prediction():
    """Return all shows for the prediction form dropdown."""
    return get_all_shows()