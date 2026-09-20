# routes/theatre_routes.py — Theatre Blueprint

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.theatre_service import fetch_all_theatres, create_theatre

theatre_bp = Blueprint('theatres', __name__, url_prefix='/theatres')


@theatre_bp.route('/')
def list_theatres():
    theatres = fetch_all_theatres()
    return render_template('add_theatre.html', theatres=theatres)


@theatre_bp.route('/add', methods=['POST'])
def add_theatre():
    success, message, _ = create_theatre(request.form)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('theatres.list_theatres'))