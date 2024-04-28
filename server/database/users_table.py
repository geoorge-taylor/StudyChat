from typing import Any, Union

from database.database_connector import DatabaseConnector as Cursor
from static.shared_types import UserDetails


def register_user(user_details: UserDetails) -> None:
    query = """
    INSERT INTO users(
        email, first_name, last_name, password, 
        tutor_group, option_one, option_two, option_three, 
        option_four, user_status) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    Cursor.query(
        query, [
            user_details["email"],
            user_details["first_name"],
            user_details["last_name"],
            user_details["password"],
            user_details['tutor_group'],
            user_details["option_one"],
            user_details["option_two"],
            user_details["option_three"],
            user_details["option_four"],
            'Online'
        ],
    )

def get_user(user_id) -> list:
    query = "SELECT * FROM users WHERE user_id = %s;"
    row = Cursor.select_one(query, [user_id])
    if not row: return []
    else: return [{
        "email": row[1],
        "first_name": row[2],
        "last_name": row[3],
        "password": None,
        "tutor_group": row[5],
        "option_one": row[6],
        "option_two": row[7],
        "option_three": row[8],
        "option_four": row[9],
        "points": row[11]
    }, row[10]]


def login_user(email: str, password: str) -> bool:
    query = "SELECT password FROM users WHERE email = %s;"
    row = Cursor.select_one(query, [email])
    if not row: return False
    return True if row[0] == password else False


def get_user_full_name(user_id: int) -> tuple:
    query = "SELECT first_name, last_name FROM users WHERE user_id = %s;"
    row = Cursor.select_one(query, [user_id])
    if not row: return ()
    else: return row


def get_user_id(email: str) -> tuple:
    query = "SELECT user_id FROM users WHERE email = %s;"
    row = Cursor.select_one(query, [email])
    return () if row is None else row


def check_email_exists(email: str) -> bool:
    query = "SELECT email FROM users WHERE email = %s;"
    row = Cursor.select_one(query, [email])
    return True if row else False


def update_user_status(user_id: int, status: str) -> None:
    query = "UPDATE users SET user_status = %s WHERE user_id = %s"
    Cursor.query(query, [status, user_id])


def increment_users_points(user_id: int, ammount: int) -> None:
    query = "UPDATE users SET points = points + %s WHERE user_id = %s;"
    Cursor.query(query, [ammount, user_id])


