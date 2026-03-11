# email_assistant/summarizer.py
"""
Email summarization module using AI/NLP models.

This module provides AI-powered summarization for individual emails
and generates daily summary reports.
"""

from transformers import pipeline
from email_assistant.config import SUMMARIZATION_MODEL
from email_assistant.database import get_emails_by_category, save_daily_summary
from datetime import datetime, timedelta
import re

# Initialize summarization pipeline
try:
    summarizer = pipeline("summarization", model=SUMMARIZATION_MODEL)
    SUMMARIZER_AVAILABLE = True
except Exception as e:
    print(f"Error loading summarization model: {e}")
    try:
        # Fallback to text2text-generation for BART models
        summarizer = pipeline("text2text-generation", model=SUMMARIZATION_MODEL)
        SUMMARIZER_AVAILABLE = True
    except Exception as e2:
        print(f"Error loading text2text-generation model: {e2}")
        SUMMARIZER_AVAILABLE = False

def summarize_email(email_body, max_length=100, min_length=30):
    """
    Summarizes an individual email using AI.

    Args:
        email_body (str): Full email body text
        max_length (int): Maximum summary length
        min_length (int): Minimum summary length

    Returns:
        str: AI-generated summary or original text if short
    """
    if not SUMMARIZER_AVAILABLE:
        # Fallback: return first few sentences
        return fallback_summarize(email_body)

    try:
        # Clean the text
        clean_text = clean_email_text(email_body)

        # If text is short, return as is
        if len(clean_text.split()) < 50:
            return clean_text

        # Generate summary
        summary = summarizer(
            clean_text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )[0]['summary_text']

        return summary

    except Exception as e:
        print(f"Error summarizing email: {e}")
        return fallback_summarize(email_body)

def fallback_summarize(text, max_sentences=3):
    """
    Fallback summarization using sentence extraction.

    Args:
        text (str): Text to summarize
        max_sentences (int): Maximum sentences to include

    Returns:
        str: Extracted summary
    """
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # Take first few sentences
    summary_sentences = sentences[:max_sentences]
    return '. '.join(summary_sentences) + '.'

def clean_email_text(text):
    """
    Cleans email text for summarization.

    Args:
        text (str): Raw email text

    Returns:
        str: Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove email signatures (basic)
    text = re.sub(r'Best regards.*', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'Regards.*', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'--.*', '', text, flags=re.IGNORECASE | re.DOTALL)

    return text.strip()

def generate_daily_summary(account_id='default', date=None):
    """
    Generates a daily summary report for all emails.

    Args:
        account_id (str): Account identifier
        date (str): Date in YYYY-MM-DD format (default: yesterday)

    Returns:
        str: Daily summary text
    """
    if date is None:
        # Default to yesterday
        yesterday = datetime.now() - timedelta(days=1)
        date = yesterday.strftime('%Y-%m-%d')

    # Get all emails for the date
    # Note: This is a simplified version. In practice, you'd filter by date
    all_emails = get_emails_by_category(account_id=account_id)

    if not all_emails:
        return f"No emails found for {date}."

    # Group emails by category
    category_groups = {}
    total_emails = len(all_emails)
    priority_count = 0

    for email in all_emails:
        category = email['category']
        if category not in category_groups:
            category_groups[category] = []
        category_groups[category].append(email)

        if email['priority']:
            priority_count += 1

    # Generate summary text
    summary_parts = [f"Daily Email Summary for {date}\n"]
    summary_parts.append(f"Total emails: {total_emails}")
    summary_parts.append(f"Priority emails: {priority_count}\n")

    for category, emails in category_groups.items():
        summary_parts.append(f"{category.upper()} ({len(emails)} emails):")

        # Summarize top emails in category
        top_emails = emails[:5]  # Limit to 5 per category
        for email in top_emails:
            sender = email['sender']
            subject = email['subject'][:50]  # Truncate long subjects
            summary_parts.append(f"  - {sender}: {subject}")

        if len(emails) > 5:
            summary_parts.append(f"  ... and {len(emails) - 5} more")
        summary_parts.append("")

    full_summary = "\n".join(summary_parts)

    # Save to database
    save_daily_summary(date, full_summary, total_emails, account_id)

    return full_summary

def summarize_email_batch(emails):
    """
    Adds summaries to a batch of emails.

    Args:
        emails (list): List of email dictionaries

    Returns:
        list: Emails with summaries added
    """
    for email in emails:
        if 'full_body' in email:
            email['summary'] = summarize_email(email['full_body'])

    return emails