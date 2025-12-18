import sqlite3
import os
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from chalicelib.constants.db_queries import SchemaQueries

DATABASE_PATH: str = os.path.join(os.path.dirname(__file__), 'app.db')
DATABASE_URL: str = f'sqlite:///{DATABASE_PATH}'

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        pass


def get_db_connection() -> sqlite3.Connection:
    conn: sqlite3.Connection = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def db_connection() -> Generator[sqlite3.Connection, None, None]:
    conn: sqlite3.Connection = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(SchemaQueries.CREATE_USERS_TABLE)
        cursor.execute(SchemaQueries.CREATE_BOOKS_TABLE)
        cursor.execute(SchemaQueries.CREATE_AUTH_TOKENS_TABLE)
