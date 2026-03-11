# email_assistant/email_parser.py
"""
Email parsing module for extracting structured data from Gmail messages.

This module takes raw Gmail API message data and parses it into
structured email objects with sender, subject, timestamp, and body preview.
"""

from email_assistant.email_fetcher import get_email_body, get_email_headers
from datetime import datetime
import email.utils

def parse_email(raw_email, account_id='default'):
    """
    Parses raw Gmail API email data into structured format.

    Args:
        raw_email (dict): Raw email data from Gmail API
        account_id (str): Account identifier

    Returns:
        dict: Parsed email data
    """
    try:
        headers = get_email_headers(raw_email['payload'])
        body = get_email_body(raw_email['payload'])

        # Extract basic information
        message_id = raw_email['id']
        sender = headers.get('from', 'Unknown')
        subject = headers.get('subject', 'No Subject')
        timestamp = parse_timestamp(headers.get('date', ''))

        # Create body preview (first 200 characters)
        body_preview = body[:200] + '...' if len(body) > 200 else body

        # Clean up sender (remove email address if present)
        sender_name = extract_sender_name(sender)

        return {
            'message_id': message_id,
            'sender': sender_name,
            'sender_email': sender,
            'subject': subject,
            'timestamp': timestamp,
            'body_preview': body_preview,
            'full_body': body,
            'account_id': account_id,
            'category': '',  # Will be set by categorizer
            'priority': 0,   # Will be set by categorizer
            'summary': ''    # Will be set by summarizer
        }

    except Exception as e:
        print(f"Error parsing email {raw_email.get('id', 'unknown')}: {e}")
        return None

def parse_timestamp(date_string):
    """
    Parses email timestamp into readable format.

    Args:
        date_string (str): Raw date string from email headers

    Returns:
        str: Formatted timestamp (YYYY-MM-DD HH:MM:SS)
    """
    try:
        # Parse the date string
        parsed_date = email.utils.parsedate_to_datetime(date_string)
        # Format to readable string
        return parsed_date.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"Error parsing timestamp '{date_string}': {e}")
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def extract_sender_name(sender_string):
    """
    Extracts the sender name from the From header.

    Args:
        sender_string (str): Raw sender string (e.g., "John Doe <john@example.com>")

    Returns:
        str: Clean sender name
    """
    try:
        # Split on '<' to separate name from email
        if '<' in sender_string:
            name_part = sender_string.split('<')[0].strip()
            # Remove quotes if present
            if name_part.startswith('"') and name_part.endswith('"'):
                name_part = name_part[1:-1]
            return name_part
        else:
            # No email address, return as is
            return sender_string.strip()
    except Exception as e:
        print(f"Error extracting sender name from '{sender_string}': {e}")
        return sender_string

def parse_multiple_emails(raw_emails, account_id='default'):
    """
    Parses multiple raw emails into structured format.

    Args:
        raw_emails (list): List of raw email dictionaries
        account_id (str): Account identifier

    Returns:
        list: List of parsed email dictionaries
    """
    parsed_emails = []
    for raw_email in raw_emails:
        parsed = parse_email(raw_email, account_id)
        if parsed:
            parsed_emails.append(parsed)

    return parsed_emails