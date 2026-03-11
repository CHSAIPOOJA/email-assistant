# email_assistant/database.py
"""
Database module for storing email data and summaries.

This module handles all database operations using SQLite.
It creates tables for emails, summaries, and user sessions.
"""

import sqlite3
from email_assistant.config import DATABASE_PATH
import os

def get_db_connection():
    """
    Creates and returns a database connection.

    Returns:
        sqlite3.Connection: Database connection object
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

def init_db():
    """
    Initializes the database by creating necessary tables.
    """
    if not os.path.exists(DATABASE_PATH):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create emails table
        cursor.execute('''
            CREATE TABLE emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT UNIQUE,
                sender TEXT,
                subject TEXT,
                timestamp TEXT,
                body_preview TEXT,
                category TEXT,
                priority INTEGER DEFAULT 0,
                summary TEXT,
                account_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create daily_summaries table
        cursor.execute('''
            CREATE TABLE daily_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                summary_text TEXT,
                email_count INTEGER,
                account_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create users table for login (basic implementation)
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()
        print("Database initialized successfully.")

def save_email(email_data):
    """
    Saves email data to the database.

    Args:
        email_data (dict): Dictionary containing email information
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO emails
        (message_id, sender, subject, timestamp, body_preview, category, priority, summary, account_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        email_data['message_id'],
        email_data['sender'],
        email_data['subject'],
        email_data['timestamp'],
        email_data['body_preview'],
        email_data['category'],
        email_data['priority'],
        email_data.get('summary', ''),
        email_data['account_id']
    ))

    conn.commit()
    conn.close()

def clear_emails(account_id='default'):
    """
    Clears all emails from the database for the specified account.

    Args:
        account_id (str): Account identifier
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM emails WHERE account_id = ?', (account_id,))
    conn.commit()
    conn.close()
    print(f"Cleared all emails for account: {account_id}")

def get_emails_by_category(category=None, account_id='default'):
    """
    Retrieves emails from database, optionally filtered by category.

    Args:
        category (str): Email category to filter by
        account_id (str): Account identifier

    Returns:
        list: List of email dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if category:
        cursor.execute('''
            SELECT * FROM emails
            WHERE category = ? AND account_id = ?
            ORDER BY timestamp DESC
        ''', (category, account_id))
    else:
        cursor.execute('''
            SELECT * FROM emails
            WHERE account_id = ?
            ORDER BY timestamp DESC
        ''', (account_id,))

    emails = cursor.fetchall()
    conn.close()

    return [dict(row) for row in emails]

def get_daily_summary(date, account_id='default'):
    """
    Retrieves daily summary for a specific date.

    Args:
        date (str): Date in YYYY-MM-DD format
        account_id (str): Account identifier

    Returns:
        dict: Daily summary data or None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM daily_summaries
        WHERE date = ? AND account_id = ?
    ''', (date, account_id))

    summary = cursor.fetchone()
    conn.close()

    return dict(summary) if summary else None

def save_daily_summary(date, summary_text, email_count, account_id='default'):
    """
    Saves daily summary to database.

    Args:
        date (str): Date in YYYY-MM-DD format
        summary_text (str): Generated summary text
        email_count (int): Number of emails summarized
        account_id (str): Account identifier
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO daily_summaries (date, summary_text, email_count, account_id)
        VALUES (?, ?, ?, ?)
    ''', (date, summary_text, email_count, account_id))

    conn.commit()
    conn.close()

def get_email_analytics(account_id='default'):
    """
    Retrieves basic analytics data.

    Args:
        account_id (str): Account identifier

    Returns:
        dict: Analytics data
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Count emails by category
    cursor.execute('''
        SELECT category, COUNT(*) as count
        FROM emails
        WHERE account_id = ?
        GROUP BY category
    ''', (account_id,))

    category_counts = dict(cursor.fetchall())

    # Count priority emails
    cursor.execute('''
        SELECT COUNT(*) as priority_count
        FROM emails
        WHERE priority = 1 AND account_id = ?
    ''', (account_id,))

    priority_count = cursor.fetchone()['priority_count']

    # Total emails
    cursor.execute('''
        SELECT COUNT(*) as total
        FROM emails
        WHERE account_id = ?
    ''', (account_id,))

    total_emails = cursor.fetchone()['total']

    conn.close()

    return {
        'category_counts': category_counts,
        'priority_count': priority_count,
        'total_emails': total_emails
    }