from typing import Any, Union

from database.database_connector import DatabaseConnector as Cursor
from static.shared_types import UserDetails


def create_new_chat(user_one: int, user_two: int, question_id: int):
    query_one = "INSERT INTO chats (created_at, question_id) VALUES(current_date(), %s);"
    query_two = "INSERT INTO chat_users (chat_id, user_id) VALUES (LAST_INSERT_ID(), %s), (LAST_INSERT_ID(), %s);"
    query_three = "SELECT LAST_INSERT_ID() as chat_id"
    Cursor.query(query_one, [question_id])
    Cursor.query(query_two, [user_one, user_two])
    rows = Cursor.select_one(query_three, [])
    return rows[0] if rows else None


def load_user_chats(user_id: int) -> list[tuple]:
    query = """
    SELECT DISTINCT users.user_id, users.first_name, users.last_name, chat_users.chat_id
    FROM users JOIN chat_users ON users.user_id = chat_users.user_id
    WHERE chat_users.chat_id IN (SELECT chat_id FROM chat_users WHERE user_id = %s)
    AND users.user_id != %s;
    """
    rows = Cursor.select_all(query, [user_id, user_id])
    return rows if rows else []


def get_chat_question(chat_id) -> tuple:
    query = """
    SELECT q.question_id, q.title, q.subject, q.description, q.expires_date, q.second_year_content
    FROM questions q WHERE q.question_id = ( SELECT question_id FROM chats WHERE chats.chat_id = %s)
    """
    row = Cursor.select_one(query, [chat_id])
    return row if row else ()


def get_users_chat_ids(user_id: int) -> list[tuple]:
    query = "SELECT chat_id FROM chat_users WHERE user_id = %s"
    rows = Cursor.select_all(query, [user_id])
    return rows if rows else []


def get_chat_replies(chat_id: int) -> list[tuple]:
    query = """
    SELECT users.first_name, users.last_name, chat_replies.created_at, chat_replies.message
    FROM chat_replies JOIN users ON chat_replies.author_id = users.user_id
    WHERE chat_replies.chat_id = %s ORDER BY chat_replies.created_at ASC;
    """
    rows = Cursor.select_all(query, [chat_id])
    return rows if rows else []


def check_user_in_chat(chat_id: int, user_id: int) -> bool:
    query = "SELECT * FROM chat_users WHERE chat_id = %s AND user_id = %s"
    row = Cursor.select_one(query, [chat_id, user_id])
    return True if row else False


def add_reply_to_chat(chat_id: int, user_id: int, message: str):
    query = """
    INSERT INTO chat_replies (chat_id, author_id, message)
    SELECT %s, %s, %s FROM dual WHERE EXISTS (SELECT 1 FROM chat_users WHERE chat_id = %s AND user_id = %s);
    """
    Cursor.query(query, [chat_id, user_id, message, chat_id, user_id])


def add_file_to_chat(chat_id: int, user_id: int, name: str, contents: str, file_size: int, created_at: str):
    query = """
    INSERT INTO chat_files (chat_id, publisher_id, file_name, file_contents, file_size, created_at)
    SELECT %s, %s, %s, %s, %s, %s FROM dual WHERE EXISTS (SELECT 1 FROM chat_users WHERE chat_id = %s AND user_id = %s);
    """
    Cursor.query(query, [chat_id, user_id, name, contents, file_size, created_at, chat_id, user_id])


def get_users_in_chat(chat_id: int) -> list[tuple]:
    query = "SELECT user_id FROM chat_users WHERE chat_id = %s"
    rows = Cursor.select_all(query, [chat_id])
    return rows if rows else []


def get_users_from_question(question_id: int) -> list:
    query = """
    SELECT DISTINCT chat_users.user_id, chats.chat_id FROM chat_users
    JOIN chats ON chat_users.chat_id = chats.chat_id WHERE chats.question_id = %s;
    """
    rows = Cursor.select_all(query, [question_id])
    return rows if rows else []


def delete_question_chats(question_id: int) -> None:
    query_one = "DELETE chat_replies FROM chat_replies JOIN chats ON chat_replies.chat_id = chats.chat_id WHERE chats.question_id = %s;"
    query_two = "DELETE chat_users FROM chat_users JOIN chats ON chat_users.chat_id = chats.chat_id WHERE chats.question_id = %s;"
    query_three = "DELETE FROM chats WHERE question_id = %s;"
    Cursor.query(query_one, [question_id])
    Cursor.query(query_two, [question_id])
    Cursor.query(query_three, [question_id])


def delete_chat(chat_id: int) -> None:
    query_one = "DELETE FROM chat_replies WHERE chat_replies.chat_id = %s;"
    query_two = "DELETE FROM chat_users WHERE chat_users.chat_id = %s;"
    query_three = "DELETE FROM chats WHERE chats.chat_id = %s;"
    Cursor.query(query_one, [chat_id])
    Cursor.query(query_two, [chat_id])
    Cursor.query(query_three, [chat_id])


def check_user_published_question(chat_id: int, user_id: int) -> bool:
    query = """
    SELECT COUNT(*) AS is_question_publisher FROM questions
    WHERE questions.publisher_id = %s AND questions.question_id = (
        SELECT chats.question_id FROM chats WHERE chats.chat_id = %s
    );
    """
    row = Cursor.select_one(query, [user_id, chat_id])
    return True if row and row[0] == 1 else False

