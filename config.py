import os

class Config:
    # MySQL Database Configuration
    # Update these values with your actual MySQL credentials
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = 'movie_crowd_db'
    MYSQL_PORT = 3306

    # Flask secret key for session management
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-environment')

    # Debug mode (set to False in production)
    DEBUG = True