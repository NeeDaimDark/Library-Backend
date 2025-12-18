#!/usr/bin/env python3
"""Script to populate the database with sample books"""

import sqlite3
import os

DATABASE_PATH = os.path.join('chalicelib', 'database', 'app.db')

SAMPLE_BOOKS = [
    ("The Great Gatsby", "F. Scott Fitzgerald", 1925, "978-0-7432-7356-5"),
    ("To Kill a Mockingbird", "Harper Lee", 1960, "978-0-06-112008-4"),
    ("1984", "George Orwell", 1949, "978-0-451-52494-2"),
    ("Pride and Prejudice", "Jane Austen", 1813, "978-0-14-143951-8"),
    ("The Catcher in the Rye", "J.D. Salinger", 1951, "978-0-316-76948-0"),
    ("Wuthering Heights", "Emily Brontë", 1847, "978-0-14-143957-0"),
    ("Jane Eyre", "Charlotte Brontë", 1847, "978-0-14-143951-8"),
    ("The Hobbit", "J.R.R. Tolkien", 1937, "978-0-547-92822-8"),
    ("The Lord of the Rings", "J.R.R. Tolkien", 1954, "978-0-544-00381-0"),
    ("Harry Potter and the Philosopher's Stone", "J.K. Rowling", 1997, "978-0-439-13959-5"),
    ("Harry Potter and the Chamber of Secrets", "J.K. Rowling", 1998, "978-0-439-13960-1"),
    ("Harry Potter and the Prisoner of Azkaban", "J.K. Rowling", 1999, "978-0-439-13961-8"),
    ("Harry Potter and the Goblet of Fire", "J.K. Rowling", 2000, "978-0-439-13959-5"),
    ("The Chronicles of Narnia", "C.S. Lewis", 1950, "978-0-06-085363-1"),
    ("The Silmarillion", "J.R.R. Tolkien", 1977, "978-0-544-00381-0"),
    ("Dune", "Frank Herbert", 1965, "978-0-441-17266-5"),
    ("Foundation", "Isaac Asimov", 1951, "978-0-553-29438-0"),
    ("Neuromancer", "William Gibson", 1984, "978-0-441-56956-0"),
    ("The Handmaid's Tale", "Margaret Atwood", 1985, "978-0-385-49081-8"),
    ("Beloved", "Toni Morrison", 1987, "978-0-452-26241-4"),
    ("Moby Dick", "Herman Melville", 1851, "978-0-14-143957-0"),
    ("War and Peace", "Leo Tolstoy", 1869, "978-0-199-23160-3"),
    ("Crime and Punishment", "Fyodor Dostoevsky", 1866, "978-0-14-044913-5"),
    ("The Brothers Karamazov", "Fyodor Dostoevsky", 1879, "978-0-14-044924-1"),
    ("Anna Karenina", "Leo Tolstoy", 1877, "978-0-14-143950-1"),
    ("The Odyssey", "Homer", -800, "978-0-14-027885-2"),
    ("The Iliad", "Homer", -800, "978-0-14-027885-2"),
    ("Oedipus Rex", "Sophocles", -429, "978-0-14-039066-5"),
    ("Hamlet", "William Shakespeare", 1603, "978-0-14-118155-0"),
    ("Macbeth", "William Shakespeare", 1606, "978-0-14-118155-0"),
    ("Romeo and Juliet", "William Shakespeare", 1595, "978-0-14-118156-7"),
    ("A Tale of Two Cities", "Charles Dickens", 1859, "978-0-14-143951-8"),
    ("Great Expectations", "Charles Dickens", 1861, "978-0-14-043722-3"),
    ("Oliver Twist", "Charles Dickens", 1838, "978-0-14-043420-8"),
    ("The Picture of Dorian Gray", "Oscar Wilde", 1890, "978-0-14-018533-9"),
    ("Frankenstein", "Mary Shelley", 1818, "978-0-14-143957-0"),
    ("Dracula", "Bram Stoker", 1897, "978-0-14-143950-1"),
    ("The Strange Case of Dr Jekyll and Mr Hyde", "Robert Louis Stevenson", 1886, "978-0-14-143951-8"),
    ("Treasure Island", "Robert Louis Stevenson", 1882, "978-0-14-143950-1"),
    ("The Adventures of Sherlock Holmes", "Arthur Conan Doyle", 1892, "978-0-14-144929-1"),
    ("A Christmas Carol", "Charles Dickens", 1843, "978-0-14-143951-8"),
    ("The Scarlet Letter", "Nathaniel Hawthorne", 1850, "978-0-14-143950-1"),
    ("The Crucible", "Arthur Miller", 1953, "978-0-14-118077-5"),
    ("The Old Man and the Sea", "Ernest Hemingway", 1952, "978-0-14-018526-1"),
    ("For Whom the Bell Tolls", "Ernest Hemingway", 1940, "978-0-684-80362-7"),
    ("The Sun Also Rises", "Ernest Hemingway", 1926, "978-0-7432-7356-5"),
    ("Slaughterhouse-Five", "Kurt Vonnegut", 1969, "978-0-385-33312-0"),
    ("Catch-22", "Joseph Heller", 1961, "978-0-684-83165-1"),
    ("The Jungle", "Upton Sinclair", 1906, "978-0-14-143950-1"),
    ("The Grapes of Wrath", "John Steinbeck", 1939, "978-0-14-118034-8"),
    ("East of Eden", "John Steinbeck", 1952, "978-0-14-118206-9"),
]

def populate_database():
    """Add sample books to the database"""
    if not os.path.exists(DATABASE_PATH):
        print(f"Database not found at: {DATABASE_PATH}")
        return

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        print(f"Adding {len(SAMPLE_BOOKS)} books to the database...")
        
        for title, author, year, isbn in SAMPLE_BOOKS:
            cursor.execute(
                'INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)',
                (title, author, year, isbn)
            )
        
        conn.commit()
        print(f"\n✓ Successfully added {len(SAMPLE_BOOKS)} books!")
        print("✓ Database is ready for testing!")
        
        # Show a sample
        cursor.execute('SELECT COUNT(*) FROM books')
        total = cursor.fetchone()[0]
        print(f"\nTotal books in database: {total}")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error adding books: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    populate_database()
