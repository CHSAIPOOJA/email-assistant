# OAUTH Setup Guide - Fix 403 Error

## Problem
You're getting a **"Access blocked:...has not completed the Google verification process"** error when trying to use Gmail OAuth.

## Root Cause
Google blocks unverified applications from accessing certain sensitive scopes. Your app is in "Testing" mode, which means only approved test users can access it.

## Solutions

### Option 1: Add Your Email as a Test User (RECOMMENDED - Fastest)

1. **Go to Google Cloud Console**:
   - Visit: https://console.cloud.google.com/
   - Select your project

2. **Configure OAuth Consent Screen**:
   - Go to "APIs & Services" > "OAuth consent screen"
   - Click "Add Users" button under "Test users"
   - Add your Gmail email address (poojaaaa9390@gmail.com)
   - Click "Add"

3. **Re-authenticate**:
   - Delete the file `token_default.json` in your project root (if it exists)
   - Click "Process New Emails" on the dashboard
   - Follow the OAuth flow again

### Option 2: Use Demo/Test Mode (NO OAUTH NEEDED)

For testing and development, the app now includes **TEST_MODE**:

1. **Edit `email_assistant/config.py`**:
   ```python
   TEST_MODE = True  # Set to True to use demo emails
   ```

2. **Demo emails include**:
   - College email from professor
   - Job interview invitation (urgent)
   - Personal email from friend
   - Promotional offer email

3. **Click "Process New Emails"**:
   - The system will use demo emails instead of Gmail
   - All categorization and summarization will work normally

### Option 3: Complete Google Verification (For Production)

1. Fill out the OAuth consent screen completely:
   - App name: "AI-Powered Email Assistant"
   - Add all required information
   - Upload logo if available

2. Submit app for verification:
   - Google will review your app
   - Takes 1-3 hours usually
   - Once approved, any Google user can access

## Current Status

✅ **TEST_MODE is enabled by default**
- The app will use demo emails automatically
- No Google authentication errors
- Perfect for learning and testing

## To Switch to Real Gmail

When you're ready to use real Gmail:

1. Set `TEST_MODE = False` in `config.py`
2. Follow "Option 1" above (add as test user)
3. Delete `token_default.json` if it exists
4. Click "Process New Emails"

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Still getting 403 error | Delete `token_default.json` and retry |
| OAuth won't open browser | Open http://localhost:8080 manually |
| Can't find test users option | Make sure you're on OAuth consent screen, not Credentials |
| Demo emails not loading | Check that `TEST_MODE = True` in config.py |

## File Locations

- **Config File**: `email_assistant/config.py`
- **Token File**: `token_default.json` (in project root)
- **Credentials**: `credentials.json` (in project root)
