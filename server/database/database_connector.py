import logging
from typing import Any, Optional

import mysql.connector as connector
from mysql.connector.types import RowType


class DatabaseConnector:

    @classmethod
    def init_cursor(cls, settings: dict[str, Any], cursor_commit: bool = False) -> None:
        cls.__cursor_commit = cursor_commit
        try:
            cls.__connection = connector.connect(**settings)
            if cls.__connection.is_connected():
                cls.__cursor = cls.__connection.cursor()
                cls.__debug(f"connected to {settings['database']}")

        except connector.Error as err:
            cls.__debug(err)  


    @classmethod
    def query(cls, query: str, params: list = []) -> None:
        if not cls.__connection.is_connected(): return
        try:
            cls.__cursor.execute(query, params, multi=False)
            if cls.__cursor_commit:
                cls.__connection.commit()
        except connector.Error as err:
            cls.__debug(err.msg)


    @classmethod
    def select_all(cls, query: str, params: list=[]) -> Optional[list[RowType]]:
        if not cls.__connection.is_connected(): return []
        cls.query(query, params)
        if cls.__cursor.rowcount > 0: 
            return cls.__cursor.fetchall() 
        return []
    

    @classmethod
    def select_one(cls, query: str, params: list=[]) -> RowType:
        if not cls.__connection.is_connected(): return ()
        cls.query(query, params)
        result = cls.__cursor.fetchone()
        return result if result else ()


    @staticmethod
    def __debug(message) -> None:
        logging.debug(f'[database connector]: {message}')
    