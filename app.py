# app.py — Application Entry Point

from flask import Flask, render_template
from config import Config

# ── Import Blueprints ──────────────────────────────────────────────
from routes.movie_routes      import movie_bp
from routes.theatre_routes    import theatre_bp
from routes.show_routes       import show_bp
from routes.booking_routes    import booking_bp
from routes.prediction_routes import prediction_bp

# ── Import models for dashboard aggregates ────────────────────────
from models.movie_model   import get_all_movies
from models.theatre_model import get_all_theatres
from models.booking_model import get_booking_stats
from models.show_model    import get_all_shows


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    # ── Register Blueprints ────────────────────────────────────────
    app.register_blueprint(movie_bp)
    app.register_blueprint(theatre_bp)
    app.register_blueprint(show_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(prediction_bp)

    # ── Dashboard (root route) ─────────────────────────────────────
    @app.route('/')
    def dashboard():
        movies   = get_all_movies()
        theatres = get_all_theatres()
        shows    = get_all_shows()
        stats    = get_booking_stats() or {}
        return render_template('dashboard.html',
                               movies=movies,
                               theatres=theatres,
                               shows=shows,
                               stats=stats)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=Config.DEBUG, port=5000)