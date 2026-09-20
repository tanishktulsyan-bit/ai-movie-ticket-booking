# routes/show_routes.py — Show Blueprint

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.show_service import fetch_all_shows, fetch_movies_and_theatres, create_new_show

show_bp = Blueprint('shows', __name__, url_prefix='/shows')


@show_bp.route('/')
def list_shows():
    shows   = fetch_all_shows()
    movies, theatres = fetch_movies_and_theatres()
    return render_template('create_show.html', shows=shows,
                           movies=movies, theatres=theatres)


@show_bp.route('/create', methods=['POST'])
def create_show():
    success, message, _ = create_new_show(request.form)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('shows.list_shows'))