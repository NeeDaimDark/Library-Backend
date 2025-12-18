from typing import Optional, Dict, List, Any
from chalicelib.database.db import db_connection
from chalicelib.constants import db_queries


class BookRepository:

    @staticmethod
    def create(title: str, author: str, year: Optional[int] = None, isbn: Optional[str] = None) -> int:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                db_queries.BookQueries.INSERT_BOOK,
                (title, author, year, isbn)
            )
            book_id: int = cursor.lastrowid
            return book_id

    @staticmethod
    def find_all() -> List[Dict[str, Any]]:
        with db_connection() as conn:
            cursor = conn.cursor()
            books = cursor.execute(db_queries.BookQueries.SELECT_ALL_BOOKS).fetchall()
            return [dict(book) for book in books]

    @staticmethod
    def find_by_id(book_id: int) -> Optional[Dict[str, Any]]:
        with db_connection() as conn:
            cursor = conn.cursor()
            book = cursor.execute(
                db_queries.BookQueries.SELECT_BOOK_BY_ID,
                (book_id,)
            ).fetchone()
            return dict(book) if book else None

    @staticmethod
    def update(
        book_id: int,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None,
        isbn: Optional[str] = None
    ) -> bool:
        with db_connection() as conn:
            cursor = conn.cursor()

            book = cursor.execute(db_queries.BookQueries.SELECT_BOOK_BY_ID, (book_id,)).fetchone()
            if not book:
                return False

            update_title: str = title if title is not None else book['title']
            update_author: str = author if author is not None else book['author']
            update_year: Optional[int] = year if year is not None else book['year']
            update_isbn: Optional[str] = isbn if isbn is not None else book['isbn']

            cursor.execute(
                db_queries.BookQueries.UPDATE_BOOK,
                (update_title, update_author, update_year, update_isbn, book_id)
            )
            return True

    @staticmethod
    def delete(book_id: int) -> bool:
        with db_connection() as conn:
            cursor = conn.cursor()

            book = cursor.execute(db_queries.BookQueries.SELECT_BOOK_BY_ID, (book_id,)).fetchone()
            if not book:
                return False

            cursor.execute(db_queries.BookQueries.DELETE_BOOK, (book_id,))
            return True
