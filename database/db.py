# database/db.py - Database Connection Handler

import mysql.connector
from mysql.connector import Error
from config import Config


def get_connection():
    """
    Creates and returns a MySQL database connection.
    Uses configuration from config.py.
    """
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"[DB ERROR] Could not connect to MySQL: {e}")
        return None


def execute_query(query, params=None, fetch=False, fetchone=False):
    """
    Generic helper to run any SQL query.

    Args:
        query   : SQL string
        params  : Tuple of bind values (optional)
        fetch   : True → fetchall(), returns list of dicts
        fetchone: True → fetchone(), returns single dict

    Returns:
        list | dict | lastrowid | None
    """
    connection = get_connection()
    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())

        if fetch:
            result = cursor.fetchall()
            return result

        if fetchone:
            result = cursor.fetchone()
            return result

        # INSERT / UPDATE / DELETE
        connection.commit()
        return cursor.lastrowid

    except Error as e:
        print(f"[QUERY ERROR] {e}")
        connection.rollback()
        return None

    finally:
        cursor.close()
        connection.close()