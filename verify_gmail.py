# verify_gmail.py
"""
Verification script to check if Gmail is actually connected and authenticated.
Run this to confirm your Gmail account is properly linked.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from email_assistant.auth import authenticate_gmail
from email_assistant.config import TEST_MODE

def verify_gmail_connection(account_id='default'):
    """Verify that Gmail is properly authenticated for a given account ID.

    Args:
        account_id (str): Identifier used when processing emails (usually user email)
    """
    
    print("=" * 60)
    print("GMAIL CONNECTION VERIFICATION")
    print("=" * 60)
    
    # Check TEST_MODE setting
    print(f"\n1. TEST_MODE Setting: {TEST_MODE}")
    if TEST_MODE:
        print("   ❌ TEST_MODE is ON - Using demo emails")
        print("   ✅ To use real Gmail, set TEST_MODE = False in config.py")
        return False
    else:
        print("   ✅ TEST_MODE is OFF - Ready for real Gmail")
    
    # Determine token filename for this account
    safe_id = ''.join(c if c.isalnum() else '_' for c in account_id)
    token_file = f'token_{safe_id}.json'
    if os.path.exists(token_file):
        print(f"\n2. Authentication Token ({token_file}): ✅ FOUND")
        print(f"   Location: {os.path.abspath(token_file)}")
        print("   Status: Gmail is authenticated!")
    else:
        print(f"\n2. Authentication Token: ❌ NOT FOUND")
        print(f"   You need to click 'Process New Emails' first")
        print(f"   This will open Google login to create the token")
        return False
    
    # Test Gmail API connection
    print("\n3. Testing Gmail API Connection...")
    try:
        service = authenticate_gmail('default')
        
        # Get user profile
        profile = service.users().getProfile(userId='me').execute()
        email_address = profile.get('emailAddress', 'Unknown')
        
        print(f"   ✅ CONNECTED TO: {email_address}")
        
        # Get unread email count
        results = service.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=1
        ).execute()
        
        unread_count = results.get('resultSizeEstimate', 0)
        print(f"   ✅ Unread Emails in Gmail: {unread_count}")
        
        # Fetch first email to verify real data
        messages = results.get('messages', [])
        if messages:
            print("\n4. Sample Email from YOUR Gmail:")
            msg_id = messages[0]['id']
            msg_data = service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            
            headers = {}
            for header in msg_data['payload']['headers']:
                headers[header['name']] = header['value']
            
            print(f"   From: {headers.get('From', 'Unknown')}")
            print(f"   Subject: {headers.get('Subject', 'No Subject')}")
            print(f"   Date: {headers.get('Date', 'Unknown')}")
            
            print("\n   ✅ This is a REAL email from YOUR Gmail account!")
        else:
            print("\n4. No unread emails found.")
            print("   Your Gmail inbox has no unread emails yet.")
            print("   Send yourself a test email to verify!")
        
        return True
        
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        print(f"   Connection failed. Try clicking 'Process New Emails' again")
        return False

def show_summary():
    """Show verification summary."""
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if verify_gmail_connection():
        print("\n✅ YOUR GMAIL IS PROPERLY CONNECTED!")
        print("\nWhat this means:")
        print("  • The app is authenticated with your Gmail account")
        print("  • Click 'Process New Emails' to fetch your emails")
        print("  • Your emails will be organized and displayed")
        print("  • Daily summaries will track your actual emails")
    else:
        print("\n❌ Gmail not properly connected yet.")
        print("\nNext steps:")
        print("  1. Go to http://localhost:5000")
        print("  2. Click 'Process New Emails' button")
        print("  3. Sign in with your Gmail account")
        print("  4. Allow permissions")
        print("  5. Run this script again to verify")
    
    print("\n" + "=" * 60 + "\n")

if __name__ == '__main__':
    show_summary()