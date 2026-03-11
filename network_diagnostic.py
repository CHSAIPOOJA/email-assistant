# network_diagnostic.py
"""
Complete network diagnostic to troubleshoot Gmail connection issues.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 70)
print("NETWORK & GMAIL DIAGNOSTIC")
print("=" * 70)

# Test 1: Check if credentials.json is valid
print("\n1. Checking credentials.json validity...")
try:
    import json
    with open('credentials.json', 'r') as f:
        creds = json.load(f)
    
    if 'installed' in creds:
        creds = creds['installed']
    
    required_fields = ['client_id', 'client_secret', 'auth_uri', 'token_uri']
    missing = [f for f in required_fields if f not in creds]
    
    if missing:
        print(f"   ❌ Missing fields: {missing}")
        print("   Your credentials.json might be corrupted!")
    else:
        print("   ✅ credentials.json is valid")
except Exception as e:
    print(f"   ❌ Error reading credentials: {e}")

# Test 2: Check Google.com accessibility
print("\n2. Testing basic internet connectivity...")
try:
    import requests
    response = requests.get('https://www.google.com', timeout=5)
    print(f"   ✅ Google.com is accessible (Status: {response.status_code})")
except Exception as e:
    print(f"   ❌ Cannot reach Google.com: {e}")
    print("   Your internet or DNS might have issues")

# Test 3: Check if token needs refresh
print("\n3. Checking authentication token...")
# look for any token file pattern
existing_tokens = [f for f in os.listdir('.') if f.startswith('token_') and f.endswith('.json')]
if existing_tokens:
    print(f"   ✅ Found token files: {existing_tokens}")
    # for diagnostics we can check any one file
    token_path = existing_tokens[0]
    print(f"   Using token file for diagnostics: {token_path}")
    try:
        import json
        with open(token_path, 'r') as f:
            tok = json.load(f)
        print(f"   Token expiry: {tok.get('expiry', 'unknown')}")
        print("   ⚠️  Token might be expired - may need refresh")
    except Exception as e:
        print(f"   ❌ Error reading token: {e}")
else:
    print("   ⚠️  No token files found - Gmail not authenticated yet")
    # nothing else to check

# Test 4: Check for proxy settings
print("\n4. Checking Windows proxy settings...")
try:
    import subprocess
    result = subprocess.run(['netsh', 'winhttp', 'show', 'proxy'], 
                          capture_output=True, text=True)
    proxy_info = result.stdout
    if 'Direct access (no proxy server)' in proxy_info:
        print("   ✅ No proxy configured")
    else:
        print("   ⚠️  Proxy detected - might interfere with API")
        print(f"   {proxy_info}")
except:
    print("   (Could not check proxy)")

# Test 5: Try direct Gmail API call
print("\n5. Testing Gmail API connection (this might take 15 seconds)...")
try:
    from email_assistant.auth import authenticate_gmail
    service = authenticate_gmail('default')
    
    # Try to get profile
    profile = service.users().getProfile(userId='me').execute()
    email = profile.get('emailAddress')
    print(f"   ✅ Gmail API Connected!")
    print(f"   Logged in as: {email}")
    
    # Try to list messages
    print("\n6. Fetching email list...")
    results = service.users().messages().list(
        userId='me',
        q='is:unread',
        maxResults=1,
        timeout=10
    ).execute()
    
    unread = results.get('resultSizeEstimate', 0)
    print(f"   ✅ Unread emails found: {unread}")
    
    if unread == 0:
        print("   💡 Your Gmail has no unread emails")
        print("   Send yourself a test email to verify the system works!")
    
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    print(f"\n   Error Type: {type(e).__name__}")
    
    if 'WinError 10060' in str(e) or 'timeout' in str(e).lower():
        print("\n   TIMEOUT ERROR - Possible causes:")
        print("   1. ISP blocking Google APIs")
        print("   2. Corporate network restrictions")
        print("   3. Network gateway issue")
        print("   4. DNS issue")
        print("\n   Try:")
        print("   • Restart your router/modem")
        print("   • Try on mobile hotspot (if available)")
        print("   • Contact your ISP")
    elif 'invalid_grant' in str(e).lower():
        print("\n   INVALID GRANT - Token expired or revoked")
        print("   Fix: Delete token_default.json and re-authenticate")
    else:
        print(f"\n   Unexpected error: {e}")

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70 + "\n")
