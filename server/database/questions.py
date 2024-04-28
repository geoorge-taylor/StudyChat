from datetime import date
from typing import Any, Union

from database.database_connector import DatabaseConnector as Cursor
from static.shared_types import QuestionDetails, UserDetails


def create_question_automatic(publisher_id: int, details: QuestionDetails) -> tuple[list, tuple]:
    # 1. Insert the question into the questions table
    # 2. Insert into the user_question table the question_id and user_ids of those elegible for the question
    #    and prevent the user who made the question to receive it
    # 3. Select the user_ids and the question_id of all the users that were affected by the question being created
    #    so we can then send a command for them to create the question client side 

    query_one = """
    INSERT INTO questions(publisher_id, title, subject, description, expires_date, second_year_content) 
    VALUES (%s,%s,%s,%s,%s,%s);
    """
    query_four = "SELECT last_insert_id();"
    query_two = """
    INSERT INTO user_questions (user_id, question_id)
    SELECT user_id, LAST_INSERT_ID() FROM users
    JOIN questions ON (
        users.option_one = questions.subject OR 
        users.option_two = questions.subject OR 
        users.option_three = questions.subject OR 
        users.option_four = questions.subject
    )
    WHERE questions.question_id = LAST_INSERT_ID()
    AND users.user_id != (
        SELECT publisher_id FROM questions 
        WHERE question_id = LAST_INSERT_ID()
    );
    """
    querey_three = """
    SELECT user_questions.user_id, user_questions.question_id
    FROM user_questions
    JOIN questions ON user_questions.question_id = questions.question_id
    JOIN users ON user_questions.user_id = users.user_id
    WHERE questions.question_id = last_insert_id();
    """

    Cursor.query(query_one,[
            publisher_id,
            details['title'],
            details['subject'],
            details['description'],
            details['expires_date'],
            details['second_year_content']]
    )
    question_id = Cursor.select_one(query_four, [])
    Cursor.query(query_two,[])
    users_affected = Cursor.select_all(querey_three, [])

    if not users_affected: return ([], question_id)
    else: return users_affected, question_id


def create_question_manual(user_ids: list[int], publisher_id: int, details: QuestionDetails) -> Any:
    query_one = """
    INSERT INTO questions(publisher_id, title, subject, description, expires_date, second_year_content) 
    VALUES (%s,%s,%s,%s,%s,%s)
    """
    Cursor.query(query_one,[
            publisher_id,
            details['title'],
            details['subject'],
            details['description'],
            details['expires_date'],
            details['second_year_content']]
    )

    for user_id in user_ids:
        query_two = """
        INSERT INTO user_questions(user_id, question_id) 
        VALUES (%s, last_insert_id())
        """
        Cursor.query(query_two, [user_id])

    querey_three = "SELECT last_insert_id()"
    row = Cursor.select_one(querey_three)
    return row[0] if row else None


def get_pending_questions(user_id: int) -> list[tuple]:
    query_one = "SELECT * FROM questions WHERE publisher_id = %s"
    rows = Cursor.select_all(query_one, [user_id])
    if not rows: return []
    else: return rows


def get_incoming_questions(user_id: int) -> list[tuple]:
    query_one = """
    SELECT * FROM questions WHERE question_id IN (
        SELECT question_id FROM user_questions WHERE user_id = %s
    );
    """
    rows = Cursor.select_all(query_one, [user_id])
    if not rows: return []
    else: return rows


def generate_questions(user_id: int) -> None:
    query = """
    INSERT INTO user_questions (user_id, question_id)
    SELECT %s, questions.question_id FROM questions
    JOIN users ON (
        users.option_one = questions.subject OR
        users.option_two = questions.subject OR
        users.option_three = questions.subject OR
        users.option_four = questions.subject
    )
    WHERE users.user_id = %s
    """
    Cursor.query(query, [user_id, user_id])


def get_suggested_users(user_id: int) -> list:
    query = """
    SELECT DISTINCT users_two.user_id, users_two.first_name, users_two.last_name, users_two.user_status
    FROM users AS users_one
    JOIN users AS users_two ON (
        users_one.option_one = users_two.option_one OR
        users_one.option_two = users_two.option_two OR
        users_one.option_three = users_two.option_three OR
        users_one.option_four = users_two.option_four)
    WHERE users_one.user_id = %s AND users_two.user_id != %s;
    """
    rows = Cursor.select_all(query, [user_id, user_id])
    return rows if rows else []


def get_users_from_input(input: str) -> list:
    query = """
    SELECT user_id, first_name, last_name, user_status FROM users
    WHERE first_name LIKE CONCAT('%', %s, '%') 
    OR last_name LIKE CONCAT('%', %s, '%');
    """
    rows = Cursor.select_all(query, [input, input])
    return rows if rows else []


def get_question_recipients(question_id: int) -> list:
    query = "SELECT user_id FROM user_questions WHERE question_id = %s"
    rows = Cursor.select_all(query, [question_id])
    return rows if rows else []


def get_question_awnsers(question_id: int) -> tuple:
    query = "SELECT COUNT(*) FROM chats WHERE question_id = %s"
    row = Cursor.select_one(query, [question_id])
    return row if row else ()


def delete_question(question_id: int) -> None:
    query_one = "DELETE FROM user_questions WHERE question_id = %s"
    query_two = "DELETE FROM questions WHERE question_id = %s"
    Cursor.query(query_one, [question_id])
    Cursor.query(query_two, [question_id])


def delete_question_from_inbox(question_id: int) -> None:
    query = "DELETE FROM user_questions WHERE question_id = %s"
    Cursor.query(query, [question_id])


def get_question(question_id: int) -> tuple:
    query_one = "SELECT * FROM questions WHERE question_id = %s"
    row = Cursor.select_one(query_one, [question_id])
    if not row: return ()
    else: return row


def check_user_has_question(question_id: int, user_id: int) -> bool:
    query = "SELECT * FROM user_questions WHERE question_id = %s AND user_id = %s"
    row = Cursor.select_one(query, [question_id, user_id])
    return True if row else False


def remove_incoming_question(question_id: int, user_id: int) -> None:
    query = "DELETE FROM user_questions WHERE question_id = %s AND user_id = %s"
    Cursor.query(query, [question_id, user_id])


def check_user_published_question(question_id: int, user_id: int) -> bool:
    query = "SELECT * FROM questions WHERE question_id = %s AND publisher_id = %s"
    row = Cursor.select_one(query, [question_id, user_id])
    return True if row else False


def get_question_publisher(question_id: int) -> tuple:
    query = "SELECT publisher_id FROM questions WHERE question_id = %s;"
    row = Cursor.select_one(query, [question_id])
    return row if row else ()