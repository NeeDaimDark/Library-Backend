class SchemaQueries:
    CREATE_USERS_TABLE = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''

    CREATE_BOOKS_TABLE = '''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            isbn TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''

    CREATE_AUTH_TOKENS_TABLE = '''
        CREATE TABLE IF NOT EXISTS auth_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    '''


class UserQueries:
    INSERT_USER = 'INSERT INTO users (username, email, password) VALUES (?, ?, ?)'
    SELECT_USER_BY_USERNAME = 'SELECT * FROM users WHERE username = ?'
    SELECT_USER_BY_EMAIL = 'SELECT * FROM users WHERE email = ?'
    SELECT_USER_BY_ID = 'SELECT * FROM users WHERE id = ?'


class BookQueries:
    INSERT_BOOK = 'INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)'
    SELECT_ALL_BOOKS = 'SELECT * FROM books ORDER BY created_at DESC'
    SELECT_BOOK_BY_ID = 'SELECT * FROM books WHERE id = ?'
    UPDATE_BOOK = 'UPDATE books SET title = ?, author = ?, year = ?, isbn = ? WHERE id = ?'
    DELETE_BOOK = 'DELETE FROM books WHERE id = ?'

    SELECT_BOOKS_BASE = 'SELECT * FROM books WHERE 1=1'
    COUNT_BOOKS_BASE = 'SELECT COUNT(*) as count FROM books WHERE 1=1'

    FILTER_BY_AUTHOR = ' AND LOWER(author) LIKE LOWER(?)'
    FILTER_BY_YEAR = ' AND year = ?'
    FILTER_BY_TITLE = ' AND LOWER(title) LIKE LOWER(?)'

    PAGINATION_SUFFIX = ' ORDER BY created_at DESC LIMIT ? OFFSET ?'
