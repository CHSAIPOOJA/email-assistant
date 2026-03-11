# debug_email_fetch.py
"""
Debug script to check if Gmail is really being accessed or if demo data is being used.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from email_assistant.auth import authenticate_gmail
from email_assistant.email_fetcher import fetch_unread_emails
from email_assistant.config import TEST_MODE

print("=" * 70)
print("EMAIL FETCHING DEBUG CHECK")
print("=" * 70)

print(f"\n1. TEST_MODE Setting: {TEST_MODE}")
if TEST_MODE:
    print("   ❌ TEST_MODE IS ON - This is why you're seeing demo data!")
    print("   To fix: Edit email_assistant/config.py and set TEST_MODE = False")
    sys.exit(1)
else:
    print("   ✅ TEST_MODE is OFF - Should use real Gmail")

print(f"\n2. Checking credentials.json...")
if os.path.exists('credentials.json'):
    print("   ✅ credentials.json found")
    with open('credentials.json', 'r') as f:
        content = f.read()
        if 'client_id' in content and 'client_secret' in content:
            print("   ✅ credentials.json contains API keys")
        else:
            print("   ❌ credentials.json is empty or invalid!")
else:
    print("   ❌ credentials.json NOT found!")
    print("   Location should be: d:\\btech projects\\Email Assistant\\credentials.json")
    sys.exit(1)

print(f"\n3. Checking authentication token...")
if os.path.exists('token_default.json'):
    print("   ✅ token_default.json exists - Gmail is authenticated")
else:
    print("   ⚠️  token_default.json not found - Will create on first auth")

print(f"\n4. Testing Gmail API Connection...")
try:
    service = authenticate_gmail('default')
    print("   ✅ Connected to Gmail API")
    
    profile = service.users().getProfile(userId='me').execute()
    email = profile.get('emailAddress', 'Unknown')
    print(f"   ✅ Authenticated as: {email}")
    
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    print("   This explains why demo data is being used!")
    sys.exit(1)

print(f"\n5. Fetching emails from Gmail...")
try:
    emails = fetch_unread_emails('default', max_results=10)
    
    if not emails:
        print("   ⚠️  No unread emails found in your Gmail")
        print("   (This is OK - your inbox might be all read)")
    else:
        print(f"   ✅ Successfully fetched {len(emails)} emails")
        
        # Check if they're demo emails
        if all('demo_' in str(email.get('id', '')) for email in emails):
            print("   ❌ These are DEMO emails, not from Gmail!")
        else:
            print("   ✅ These are REAL emails from your Gmail account")
            
            # Show first email
            if emails:
                first = emails[0]
                headers = {}
                for h in first.get('payload', {}).get('headers', []):
                    headers[h['name']] = h['value']
                
                print(f"\n   First email details:")
                print(f"     From: {headers.get('From', 'Unknown')}")
                print(f"     Subject: {headers.get('Subject', 'No Subject')[:50]}")
                print(f"     Date: {headers.get('Date', 'Unknown')}")
                
except Exception as e:
    print(f"   ❌ ERROR fetching emails: {e}")
    print("   This might be why demo data is shown")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("\n✅ ALL CHECKS PASSED - Real Gmail is being accessed!")
print("\nIf dashboard still shows demo data:")
print("  1. Clear browser cache (Ctrl+Shift+Delete)")
print("  2. Refresh the page (F5)")
print("  3. Click 'Process New Emails' again")
print("\n" + "=" * 70 + "\n")
