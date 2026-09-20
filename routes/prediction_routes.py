# routes/prediction_routes.py — Prediction Blueprint

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.prediction_service import (
    fetch_all_predictions,
    predict_crowd,
    get_shows_for_prediction,
)

prediction_bp = Blueprint('predictions', __name__, url_prefix='/predictions')


@prediction_bp.route('/')
def list_predictions():
    predictions = fetch_all_predictions()
    shows       = get_shows_for_prediction()
    return render_template('prediction.html',
                           predictions=predictions, shows=shows)


@prediction_bp.route('/predict', methods=['POST'])
def run_prediction():
    show_id = request.form.get('show_id')
    if not show_id:
        flash("Please select a show.", 'error')
        return redirect(url_for('predictions.list_predictions'))

    success, message, result = predict_crowd(int(show_id))
    if success:
        flash(message, 'success')
        # Pass result back via session-like query param
        return render_template('prediction.html',
                               predictions=fetch_all_predictions(),
                               shows=get_shows_for_prediction(),
                               latest=result)
    else:
        flash(message, 'error')
        return redirect(url_for('predictions.list_predictions'))


@prediction_bp.route('/api/predict/<int:show_id>')
def api_predict(show_id):
    """JSON endpoint — useful for AJAX calls."""
    success, message, result = predict_crowd(show_id)
    return jsonify({'success': success, 'message': message, 'data': result})