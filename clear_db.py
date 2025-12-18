#!/usr/bin/env python3
"""Script to clear all data from the database"""

import sqlite3
import os

DATABASE_PATH = os.path.join('chalicelib', 'database', 'app.db')

def clear_database():
    """Clear all data from all tables in the database"""
    if not os.path.exists(DATABASE_PATH):
        print(f"Database not found at: {DATABASE_PATH}")
        print("Nothing to clear.")
        return

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        # Delete all data from tables (order matters due to foreign keys)
        print("Clearing database...")
        
        cursor.execute('DELETE FROM auth_tokens')
        tokens_deleted = cursor.rowcount
        print(f"✓ Deleted {tokens_deleted} auth token(s)")
        
        cursor.execute('DELETE FROM books')
        books_deleted = cursor.rowcount
        print(f"✓ Deleted {books_deleted} book(s)")
        
        cursor.execute('DELETE FROM users')
        users_deleted = cursor.rowcount
        print(f"✓ Deleted {users_deleted} user(s)")
        
        # Reset auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='auth_tokens'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='books'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")
        
        conn.commit()
        print("\n✓ Database cleared successfully!")
        print("All tables are now empty and auto-increment counters have been reset.")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error clearing database: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    confirm = input("Are you sure you want to clear ALL data from the database? (yes/no): ")
    if confirm.lower() in ['yes', 'y']:
        clear_database()
    else:
        print("Operation cancelled.")
