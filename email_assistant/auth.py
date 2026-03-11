# email_assistant/auth.py
"""
Authentication module for Gmail API using OAuth 2.0.

This module handles the authentication process to securely connect to Gmail accounts.
It uses Google's OAuth 2.0 flow to obtain access tokens and refresh them as needed.

Requirements:
- credentials.json file from Google Cloud Console (Gmail API enabled)
- SCOPES define the permissions requested (readonly for Gmail)

Functions:
- authenticate_gmail(account_id): Authenticates and returns a Gmail API service object
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os

# Define the scopes for Gmail API access
# 'https://www.googleapis.com/auth/gmail.readonly' allows reading emails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail(account_id='default'):
    """
    Authenticates with Gmail API using OAuth 2.0 and returns a service object.

    Args:
        account_id (str): Identifier for the account (for multiple accounts, use different IDs)

    Returns:
        googleapiclient.discovery.Resource: Gmail API service object

    Process:
    1. Check if a token file exists for the account
    2. Load credentials from token if available
    3. Refresh token if expired, or start new OAuth flow
    4. Save new/updated token to file
    5. Build and return Gmail API service
    """
    creds = None
    token_file = f'token_{account_id}.json'

    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        raise FileNotFoundError("❌ credentials.json not found! Download it from Google Cloud Console → APIs & Services → Credentials")

    print(f"[DEBUG] Checking for token file: {token_file}")

    # Load existing credentials from token file if it exists
    if os.path.exists(token_file):
        print(f"[DEBUG] Found existing token file")
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        print(f"[DEBUG] Loaded credentials from {token_file}")

    # If credentials are invalid or don't exist, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh the expired token
            print(f"[DEBUG] Token expired, refreshing...")
            creds.refresh(Request())
            print(f"[DEBUG] Token refreshed successfully")
        else:
            # Start a new OAuth flow
            # This will open a browser for user authentication
            print(f"[DEBUG] Starting new OAuth flow - browser should open for authentication")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            print(f"[DEBUG] OAuth flow completed successfully")

        # Save the credentials to token file for future use
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
        print(f"[DEBUG] Saved new token to {token_file}")

    # Build the Gmail API service
    print(f"[DEBUG] Building Gmail API service...")
    service = build('gmail', 'v1', credentials=creds)
    print(f"[DEBUG] Gmail service built successfully")
    return service