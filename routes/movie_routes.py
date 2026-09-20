# routes/movie_routes.py — Movie Blueprint

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.movie_service import fetch_all_movies, create_movie

movie_bp = Blueprint('movies', __name__, url_prefix='/movies')


@movie_bp.route('/')
def list_movies():
    movies = fetch_all_movies()
    return render_template('add_movie.html', movies=movies)


@movie_bp.route('/add', methods=['POST'])
def add_movie():
    success, message, _ = create_movie(request.form)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('movies.list_movies'))