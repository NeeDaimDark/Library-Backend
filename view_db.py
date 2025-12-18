#!/usr/bin/env python3
"""Simple script to view the contents of the database"""

import sqlite3
import os
import sys

DATABASE_PATH = os.path.join('chalicelib', 'database', 'app.db')

def view_users():
    """Display all users in the database"""
    if not os.path.exists(DATABASE_PATH):
        print(f"Database not found at: {DATABASE_PATH}")
        return

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get all users
    users = cursor.execute('SELECT id, username, email, created_at FROM users').fetchall()

    if not users:
        print("\nNo users found in the database.")
    else:
        print(f"\n{'='*80}")
        print(f"USERS - Found {len(users)} user(s):")
        print(f"{'='*80}\n")

        for user in users:
            print(f"ID: {user['id']}")
            print(f"Username: {user['username']}")
            print(f"Email: {user['email']}")
            print(f"Created: {user['created_at']}")
            print("-" * 80)

    conn.close()

def view_books():
    """Display all books in the database"""
    if not os.path.exists(DATABASE_PATH):
        print(f"Database not found at: {DATABASE_PATH}")
        return

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get all books
    books = cursor.execute('SELECT * FROM books').fetchall()

    if not books:
        print("\nNo books found in the database.")
    else:
        print(f"\n{'='*80}")
        print(f"BOOKS - Found {len(books)} book(s):")
        print(f"{'='*80}\n")

        for book in books:
            print(f"ID: {book['id']}")
            print(f"Title: {book['title']}")
            print(f"Author: {book['author']}")
            print(f"Year: {book['year']}")
            print(f"ISBN: {book['isbn']}")
            print(f"Created: {book['created_at']}")
            print("-" * 80)

    conn.close()

def view_all():
    """Display all data from the database"""
    if not os.path.exists(DATABASE_PATH):
        print(f"Database not found at: {DATABASE_PATH}")
        return

    print("\n" + "="*80)
    print("DATABASE VIEWER - Library API")
    print("="*80)

    view_users()
    view_books()

    print()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == 'users':
            view_users()
        elif command == 'books':
            view_books()
        else:
            print("Usage: python view_db.py [users|books]")
            print("  users - Show only users")
            print("  books - Show only books")
            print("  (no argument) - Show all data")
    else:
        view_all()
