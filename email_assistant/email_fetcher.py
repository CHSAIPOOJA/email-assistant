# email_assistant/email_fetcher.py
"""
Email fetching module for retrieving emails from Gmail.

This module connects to Gmail API and fetches unread emails from specified accounts.
It handles pagination and returns raw email data for further processing.
"""

from email_assistant.auth import authenticate_gmail
from email_assistant.config import EMAIL_CATEGORIES, TEST_MODE
import base64
import email
from bs4 import BeautifulSoup

def fetch_unread_emails(account_id='default', max_results=50):
    """
    Fetches unread emails from Gmail account.

    Args:
        account_id (str): Account identifier for authentication
        max_results (int): Maximum number of emails to fetch

    Returns:
        list: List of raw email dictionaries with message data
    """
    
    # Authenticate and get Gmail service
    print(f"[DEBUG] Authenticating Gmail for account: {account_id}")
    service = authenticate_gmail(account_id)
    print(f"[DEBUG] Authentication successful")

    # Query for unread emails
    query = 'is:unread'
    print(f"[DEBUG] Querying Gmail with: {query}")

    try:
        # Get list of messages
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get('messages', [])
        print(f"[DEBUG] Found {len(messages)} unread messages")

        if not messages:
            print("⚠️  No unread emails found in Gmail. Check:")
            print("   • Your Gmail has unread emails")
            print("   • You're querying the right account")
            print("   • Gmail API has proper permissions")
            return []

        # Fetch full message details for each email
        emails = []
        for message in messages:
            try:
                msg_data = service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()
                emails.append(msg_data)
            except Exception as e:
                print(f"Error fetching message {message['id']}: {e}")
                continue

        print(f"Successfully fetched {len(emails)} unread emails from Gmail.")
        return emails

    except Exception as e:
        print(f"ERROR accessing Gmail API: {e}")
        print(f"Error type: {type(e).__name__}")
        print("\nThis is a REAL ERROR - not using demo data.")
        print("Possible causes:")
        print("  • Network connection issue")
        print("  • Firewall blocking Google API")
        print("  • Gmail API rate limit exceeded")
        print("  • Invalid/expired authentication token")
        print("\nFixes to try:")
        print("  1. Check internet connection")
        print("  2. Disable VPN/Proxy")
        print("  3. Allow Python in Windows Firewall")
        print("  4. Delete token_default.json and re-authenticate")
        raise Exception(f"Gmail API Error: {e}")

def get_unread_count(account_id='default'):
    """
    Gets the current unread email count from Gmail.

    Args:
        account_id (str): Account identifier

    Returns:
        int: Number of unread emails
    """
    try:
        service = authenticate_gmail(account_id)
        results = service.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=1
        ).execute()
        return results.get('resultSizeEstimate', 0)
    except Exception as e:
        print(f"Error getting unread count: {e}")
        return 0

def get_email_body(payload):
    """
    Extracts the plain text body from email payload.

    Args:
        payload (dict): Email payload from Gmail API

    Returns:
        str: Plain text body of the email
    """
    body = ""

    if 'parts' in payload:
        # Multipart email
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                body += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            elif part['mimeType'] == 'text/html':
                html_content = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                # Convert HTML to plain text
                soup = BeautifulSoup(html_content, 'html.parser')
                body += soup.get_text()
    else:
        # Single part email
        if payload['mimeType'] == 'text/plain':
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        elif payload['mimeType'] == 'text/html':
            html_content = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
            soup = BeautifulSoup(html_content, 'html.parser')
            body = soup.get_text()

    return body.strip()

def get_email_headers(payload):
    """
    Extracts email headers from payload.

    Args:
        payload (dict): Email payload from Gmail API

    Returns:
        dict: Dictionary of email headers
    """
    headers = {}
    for header in payload['headers']:
        headers[header['name'].lower()] = header['value']
    return headers