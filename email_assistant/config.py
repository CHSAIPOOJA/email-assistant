# email_assistant/config.py
"""
Configuration file for the Email Assistant project.

This file contains configuration settings for the application,
such as database paths, API keys, and other constants.
"""

import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database configuration
DATABASE_PATH = os.path.join(BASE_DIR, '..', 'email_assistant.db')

# Gmail API credentials file
CREDENTIALS_FILE = os.path.join(BASE_DIR, '..', 'credentials.json')

# Flask configuration
SECRET_KEY = 'your-secret-key-here-change-in-production'  # Change this in production
DEBUG = True

# TEST MODE - Set to True to use demo data instead of Gmail
TEST_MODE = False

# Scheduler configuration
DAILY_SUMMARY_HOUR = 18  # 6 PM daily summary

# Email categories
EMAIL_CATEGORIES = ['college', 'placement', 'personal', 'important', 'promotions']

# Priority keywords
PRIORITY_KEYWORDS = ['urgent', 'deadline', 'interview', 'offer', 'important', 'asap', 'immediate', 'critical']

# Category keywords
CATEGORY_KEYWORDS = {
    'college': ['university', 'college', 'student', 'academic', 'course', 'assignment', 'exam', 'professor', 'lecture', 'campus'],
    'placement': ['job', 'internship', 'recruitment', 'hiring', 'application', 'resume', 'interview', 'career', 'position', 'vacancy'],
    'personal': ['friend', 'family', 'personal', 'hi', 'hello', 'how are you', 'meeting', 'dinner', 'party'],
    'important': ['important', 'urgent', 'critical', 'attention', 'required', 'mandatory', 'official'],
    'promotions': ['sale', 'discount', 'offer', 'promotion', 'newsletter', 'marketing', 'advertisement', 'deal', 'special']
}

# NLP model for summarization (using transformers)
SUMMARIZATION_MODEL = 'facebook/bart-large-cnn'

# Spacy model for NLP tasks
SPACY_MODEL = 'en_core_web_sm'