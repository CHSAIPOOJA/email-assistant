# email_assistant/dashboard.py
"""
Flask web dashboard for the Email Assistant.

This module provides a web interface for viewing categorized emails,
searching, displaying analytics, and accessing daily summaries.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from email_assistant.database import get_emails_by_category, get_email_analytics, get_daily_summary, get_db_connection
from email_assistant.config import SECRET_KEY, TEST_MODE
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Flask-Login setup
login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    """Load user from database by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(user_data['id'], user_data['username'], user_data['email'])
    return None

def create_app():
    """
    Application factory for Flask app.

    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SECRET_KEY'] = SECRET_KEY

    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Register routes
    @app.route('/')
    @login_required
    def dashboard():
        """Main dashboard showing emails and analytics."""
        category = request.args.get('category', 'all')
        search = request.args.get('search', '')

        # Get emails
        if category == 'all':
            emails = get_emails_by_category()
        else:
            emails = get_emails_by_category(category)

        # Filter by search
        if search:
            emails = [e for e in emails if search.lower() in e['subject'].lower() or search.lower() in e['sender'].lower()]

        # Get analytics
        analytics = get_email_analytics()

        # Get today's summary
        today = datetime.now().strftime('%Y-%m-%d')
        summary = get_daily_summary(today)

        return render_template('dashboard.html',
                             emails=emails,
                             analytics=analytics,
                             summary=summary,
                             current_category=category,
                             search=search,
                             is_test_mode=TEST_MODE)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login page."""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if not username or not password:
                flash('Username and password are required')
                return render_template('login.html')

            # Check credentials against database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, email, password_hash FROM users WHERE username = ?', (username,))
            user_data = cursor.fetchone()
            conn.close()

            if user_data and check_password_hash(user_data['password_hash'], password):
                user = User(user_data['id'], user_data['username'], user_data['email'])
                login_user(user)
                flash(f'Welcome back, {username}!')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password')

        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """User registration page."""
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            # Validation
            if not username or not email or not password or not confirm_password:
                flash('All fields are required')
                return render_template('register.html')

            if password != confirm_password:
                flash('Passwords do not match')
                return render_template('register.html')

            if len(password) < 6:
                flash('Password must be at least 6 characters long')
                return render_template('register.html')

            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if username already exists
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                conn.close()
                flash('Username already exists')
                return render_template('register.html')

            # Check if email already exists
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                conn.close()
                flash('Email already registered')
                return render_template('register.html')

            # Create new user with hashed password
            password_hash = generate_password_hash(password)
            try:
                cursor.execute(
                    'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                    (username, email, password_hash)
                )
                conn.commit()
                conn.close()
                flash('Account created successfully! Please login.')
                return redirect(url_for('login'))
            except Exception as e:
                conn.close()
                flash(f'Error creating account: {e}')
                return render_template('register.html')

        return render_template('register.html')

    @app.route('/logout')
    @login_required
    def logout():
        """User logout."""
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('login'))

    @app.route('/process_emails', methods=['POST'])
    @login_required
    def process_emails():
        """Process unread emails."""
        from email_assistant.processor import process_emails
        try:
            count = process_emails()
            if count == 0:
                flash('⚠️ No unread emails found. Check your Gmail inbox or verify authentication.', 'warning')
            else:
                flash(f'✅ Successfully processed {count} emails from Gmail!')
        except FileNotFoundError as e:
            flash(f'❌ Missing File: {str(e)}', 'error')
            print(f"FileNotFoundError: {e}")
        except Exception as e:
            error_msg = str(e)
            if 'WinError 10060' in error_msg or 'timeout' in error_msg.lower():
                flash('❌ Network Error: Cannot connect to Gmail. Check internet & firewall.', 'error')
            elif 'Gmail API Error' in error_msg or 'Gmail' in error_msg:
                flash(f'❌ Gmail Error: {error_msg[:100]}...', 'error')
            else:
                flash(f'❌ Error: {error_msg[:100]}...', 'error')
            print(f"ERROR: {error_msg}")
        return redirect(url_for('dashboard'))

    return app