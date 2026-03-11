# email_assistant/app.py
"""
Main application entry point for the Email Assistant.

This file initializes the Flask application, sets up the database,
and starts the scheduler for automated tasks.
"""

from flask import Flask
from email_assistant.dashboard import create_app
from email_assistant.scheduler import init_scheduler
from email_assistant.database import init_db

def main():
    """
    Main function to run the Email Assistant application.
    """
    # Create Flask app
    app = create_app()

    # Initialize database
    init_db()

    # Initialize and start scheduler
    scheduler = init_scheduler(app)
    scheduler.start()

    try:
        # Run the Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        scheduler.shutdown()

if __name__ == '__main__':
    main()