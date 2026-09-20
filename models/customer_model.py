# models/customer_model.py — Data access layer for CUSTOMER table

from database.db import execute_query


def get_all_customers():
    sql = "SELECT * FROM CUSTOMER ORDER BY name"
    return execute_query(sql, fetch=True) or []


def get_customer_by_id(customer_id):
    sql = "SELECT * FROM CUSTOMER WHERE customer_id = %s"
    return execute_query(sql, (customer_id,), fetchone=True)


def get_or_create_customer(name, email, phone):
    """
    Fetch existing customer by email, or insert a new one.
    Returns customer_id.
    """
    existing = execute_query(
        "SELECT customer_id FROM CUSTOMER WHERE email = %s",
        (email,),
        fetchone=True
    )
    if existing:
        return existing['customer_id']

    return execute_query(
        "INSERT INTO CUSTOMER (name, email, phone) VALUES (%s, %s, %s)",
        (name, email, phone)
    )