from typing import Optional, Dict, Any
from chalicelib.database.db import db_connection
from chalicelib.constants import db_queries


class UserRepository:

    @staticmethod
    def create(username: str, email: str, password_hash: bytes) -> int:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                db_queries.UserQueries.INSERT_USER,
                (username, email, password_hash)
            )
            user_id: int = cursor.lastrowid
            return user_id

    @staticmethod
    def find_by_username(username: str) -> Optional[Dict[str, Any]]:
        with db_connection() as conn:
            cursor = conn.cursor()
            user = cursor.execute(
                db_queries.UserQueries.SELECT_USER_BY_USERNAME,
                (username,)
            ).fetchone()
            return dict(user) if user else None

    @staticmethod
    def find_by_email(email: str) -> Optional[Dict[str, Any]]:
        with db_connection() as conn:
            cursor = conn.cursor()
            user = cursor.execute(
                db_queries.UserQueries.SELECT_USER_BY_EMAIL,
                (email,)
            ).fetchone()
            return dict(user) if user else None

    @staticmethod
    def find_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        with db_connection() as conn:
            cursor = conn.cursor()
            user = cursor.execute(
                db_queries.UserQueries.SELECT_USER_BY_ID,
                (user_id,)
            ).fetchone()
            return dict(user) if user else None
