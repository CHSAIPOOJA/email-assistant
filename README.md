# README.md
# AI-Powered Smart Email Assistant with Daily Summaries

This project is a comprehensive email assistant that connects to Gmail accounts, categorizes emails, generates summaries, and provides a web dashboard.

## Features

- Secure Gmail API integration with OAuth 2.0
- Fetch and parse unread emails
- AI-powered email categorization and summarization
- Daily summary reports
- Flask web dashboard with analytics
- Automated daily summaries via scheduler
- Email notifications

## Setup Instructions

### 1. Google Cloud Console Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API" and enable it
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Desktop application"
   - Download the `credentials.json` file
   - Place it in the project root directory

### 2. Install Dependencies
```bash
pip install -r requirements.txt
# Note: spaCy model download may fail on Python 3.14+, but keyword-based categorization will still work
```

### 3. Initialize Database
```bash
python -c "from email_assistant.database import init_db; init_db()"
```

### 4. Run the Application
```bash
python email_assistant/app.py
```

Visit `http://localhost:5000` in your browser.

### 5. Process Emails (First Time)
```bash
python email_assistant/processor.py
```

This will fetch unread emails, process them, and populate the dashboard.

## Usage

- **Login**: Use username `admin` and password `password`
- **Dashboard**: View categorized emails, search, and analytics
- **Daily Summaries**: Automatically generated at 6 PM daily
- **Notifications**: Daily summaries sent via email (configure recipient in notifier.py)

## Module Details

### 1. Authentication (`auth.py`)
- Handles OAuth 2.0 flow with Gmail
- Supports multiple accounts via account_id
- Stores tokens securely in JSON files

### 2. Email Fetching (`email_fetcher.py`)
- Retrieves unread emails using Gmail API
- Extracts plain text from HTML emails
- Handles pagination for large inboxes

### 3. Email Parsing (`email_parser.py`)
- Parses Gmail API message format
- Extracts sender, subject, timestamp, body
- Creates structured email objects

### 4. Categorization (`categorizer.py`)
- Uses keyword matching for email categorization
- Detects priority emails
- Fallback to spaCy NLP if available

### 5. Summarization (`summarizer.py`)
- AI-powered email summarization using transformers
- Generates daily summary reports
- Handles long emails intelligently

### 6. Database (`database.py`)
- SQLite database for data persistence
- Stores emails, summaries, and analytics
- Provides query functions for the dashboard

### 7. Dashboard (`dashboard.py`)
- Flask web application
- User authentication with Flask-Login
- Email viewing, searching, and analytics

### 8. Scheduler (`scheduler.py`)
- Automated daily summary generation
- Background job scheduling with APScheduler

### 9. Notifier (`notifier.py`)
- Sends daily summary emails
- Uses Gmail API for sending notifications

### 10. Processor (`processor.py`)
- Orchestrates the entire email processing pipeline
- Run this to fetch and process new emails

## Configuration

Edit `email_assistant/config.py` to customize:
- Database path
- Email categories and keywords
- Scheduler timing
- AI model settings

## Security Notes

- Change the default login credentials in production
- Store `credentials.json` securely
- Use environment variables for sensitive data
- The app runs on `http://localhost:5000` by default

## Troubleshooting

- **OAuth Error**: Ensure `credentials.json` is in the project root
- **No Emails**: Check Gmail API permissions and token validity
- **spaCy Issues**: The app works with keyword-only categorization
- **Database Errors**: Run `init_db()` to create tables

## Project Structure

- `email_assistant/`: Main application modules
  - `auth.py`: Gmail authentication
  - `email_fetcher.py`: Fetch emails from Gmail
  - `email_parser.py`: Parse email content
  - `categorizer.py`: Categorize emails using NLP
  - `summarizer.py`: Generate AI summaries
  - `database.py`: Database operations
  - `dashboard.py`: Flask web application
  - `scheduler.py`: Automated tasks
  - `notifier.py`: Email notifications
  - `config.py`: Configuration settings

- `static/`: CSS, JavaScript files
- `templates/`: HTML templates
- `requirements.txt`: Python dependencies

## Modules Overview

1. **Authentication (auth.py)**: Handles OAuth 2.0 flow for Gmail API access
2. **Email Fetching (email_fetcher.py)**: Retrieves unread emails from Gmail
3. **Email Parsing (email_parser.py)**: Extracts sender, subject, timestamp, body
4. **Categorization (categorizer.py)**: Classifies emails into categories using keywords and NLP
5. **Summarization (summarizer.py)**: Uses AI to create concise email summaries
6. **Database (database.py)**: Stores email metadata and summaries in SQLite
7. **Dashboard (dashboard.py)**: Flask web interface for viewing emails and analytics
8. **Scheduler (scheduler.py)**: Automates daily summary generation
9. **Notifier (notifier.py)**: Sends daily summary emails to users

## Learning Path

The code is organized module by module with detailed comments. Start with `auth.py` to understand Gmail API authentication, then proceed through each module in order.