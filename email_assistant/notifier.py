# email_assistant/notifier.py
"""
Email notification module for sending daily summaries.

This module handles sending email notifications with daily summaries
using the Gmail API.
"""

from email_assistant.auth import authenticate_gmail
from email_assistant.database import get_daily_summary
from email.mime.text import MIMEText
import base64
from datetime import datetime

def send_daily_summary_notification(date, recipient_email=None, account_id='default'):
    """
    Sends daily summary notification via email.

    Args:
        date (str): Date in YYYY-MM-DD format
        recipient_email (str): Email address to send to (default: account email)
        account_id (str): Account identifier
    """
    # Get the daily summary
    summary = get_daily_summary(date, account_id)
    if not summary:
        print(f"No summary found for {date}")
        return

    # Authenticate and get Gmail service
    service = authenticate_gmail(account_id)

    # Prepare email content
    subject = f"Daily Email Summary - {date}"
    body = f"""
Your daily email summary for {date}:

{summary['summary_text']}

---
This is an automated message from your Email Assistant.
"""

    # Create message
    message = create_message(recipient_email or get_account_email(service), subject, body)

    try:
        # Send the message
        sent_message = service.users().messages().send(
            userId='me',
            body=message
        ).execute()

        print(f"Daily summary notification sent. Message ID: {sent_message['id']}")
    except Exception as e:
        print(f"Error sending notification: {e}")

def create_message(recipient, subject, body):
    """
    Creates a Gmail API message object.

    Args:
        recipient (str): Recipient email address
        subject (str): Email subject
        body (str): Email body

    Returns:
        dict: Gmail API message format
    """
    message = MIMEText(body)
    message['to'] = recipient
    message['subject'] = subject

    # Encode the message
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    return {
        'raw': raw_message
    }

def get_account_email(service):
    """
    Gets the account email address from Gmail profile.

    Args:
        service: Gmail API service object

    Returns:
        str: Account email address
    """
    try:
        profile = service.users().getProfile(userId='me').execute()
        return profile['emailAddress']
    except Exception as e:
        print(f"Error getting account email: {e}")
        return 'your-email@example.com'  # Fallback

def send_test_notification(recipient_email, account_id='default'):
    """
    Sends a test notification email.

    Args:
        recipient_email (str): Email address to send test to
        account_id (str): Account identifier
    """
    service = authenticate_gmail(account_id)

    subject = "Email Assistant Test Notification"
    body = """
This is a test notification from your Email Assistant.

If you received this email, the notification system is working correctly!

---
Email Assistant
"""

    message = create_message(recipient_email, subject, body)

    try:
        sent_message = service.users().messages().send(
            userId='me',
            body=message
        ).execute()

        print(f"Test notification sent to {recipient_email}. Message ID: {sent_message['id']}")
    except Exception as e:
        print(f"Error sending test notification: {e}")