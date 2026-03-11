# Email Assistant - How It Works & Gmail Setup Guide

## 🎯 What's Happening Right Now

### Current Status: DEMO MODE
The screenshots show **demo emails**, not real Gmail data. The system is using:
- Demo email from professor
- Demo interview invitation
- Demo personal email
- Demo promotional email

This is **no real Gmail connection** yet.

---

## 📧 How Gmail Integration Works

### The Complete Workflow

```
1. CONNECT TO GMAIL
   ↓ (OAuth 2.0 - You authorize the app)
   
2. FETCH EMAILS
   ↓ (App reads your unread emails)
   
3. PARSE & CATEGORIZE
   ↓ (Extract sender, subject, body)
   ↓ (Categorize: college, placement, job, etc.)
   
4. STORE IN DATABASE
   ↓ (Save to SQLite database on your computer)
   
5. DISPLAY ON DASHBOARD
   ↓ (Show in web interface)
   
6. DAILY SUMMARIES (Every 24 hours)
   ↓ (Generate report at 6 PM)
   ↓ (Send email notification)
```

---

## 🔑 How OAuth 2.0 Works

### What does the app actually access?

When you click "Process New Emails" with real Gmail:

1. **Browser opens Google login**
2. **You sign in with your Gmail email**
3. **Google asks for permission**:
   - ✅ Read unread emails (read-only - can't delete/modify)
   - ❌ Write access (NOT granted)
   - ❌ Access contacts (NOT granted)
   - ❌ Access calendar (NOT granted)

4. **You allow permission**
5. **App gets access token** (temporary key)
6. **App fetches YOUR unread emails** from YOUR account
7. **Everything stays on your computer** (database stored locally)

### What the app CANNOT do:
- Delete your emails
- Send emails from your account
- Modify emails
- Access other Google services
- Share your data with anyone

---

## 🚀 Setup Real Gmail Integration (Step by Step)

### Step 1: Prepare Google Cloud Console

1. **Go to**: https://console.cloud.google.com/
2. **Select your project** (or create new)
3. **Enable Gmail API**:
   - Click "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

4. **Create OAuth Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client ID"
   - Choose "Desktop application"
   - Download and save as `credentials.json` in project root

5. **Add Test Users** (to avoid 403 error):
   - Go to "APIs & Services" > "OAuth consent screen"
   - Click "Add Users"
   - Add your Gmail email: `poojaaaa9390@gmail.com`
   - Click "Add"

### Step 2: Configure Your Email Assistant

1. **Edit `config.py`**:
   ```python
   # Change this line:
   TEST_MODE = False  # Disable demo mode
   ```

2. **Delete old tokens**:
   - Delete any `token_*.json` files from project root (if exists) to force re‑authentication

   - This forces re-authentication

3. **Place credentials**:
   - Make sure `credentials.json` is in project root
   - Check file exists: `d:\btech projects\Email Assistant\credentials.json`

### Step 3: First Run - Connect Gmail

1. **Open dashboard**: `http://localhost:5000`
2. **Login** with your account
3. **Click "Process New Emails"**
4. **Browser opens Google login**:
   - Sign in with the email you added as test user
   - Select "Allow" for permissions
   - Complete OAuth flow

5. **App fetches your emails**:
   - All unread emails load
   - Dashboard updates with real data
   - Database stores everything locally

---

## ⏰ Daily Summary & Notifications Setup

### How Daily Summaries Work

The app automatically:
1. **Every 24 hours at 6 PM**:
   - Reads all stored emails from today
   - Groups by category
   - Generates summary text
   - Stores in database

2. **Optionally sends email**:
   - Email gets sent to your Gmail inbox
   - Contains summary of all today's emails
   - Shows categories and counts

### To Enable Email Notifications

**Edit `email_assistant/notifier.py`**:

```python
def send_daily_summary_notification(date, recipient_email=None, account_id='default'):
    # Change this line:
    recipient_email = 'poojaaaa9390@gmail.com'  # Your email
    
    # Rest of function sends notification
```

### Example Daily Summary Email

```
Subject: Daily Email Summary - 2026-03-09

Your daily email summary for 2026-03-09:

Total emails: 15
Priority emails: 3

COLLEGE (4 emails):
  - professor@university.edu: Assignment deadline extended
  - dean@university.edu: Important notice
  ... and 2 more

PLACEMENT (5 emails):
  - hr@company.com: Interview scheduled
  - recruiter@tech.com: Job offer
  ... and 3 more

PERSONAL (3 emails):
  - friend@email.com: Weekend plans
  ... and 2 more

PROMOTIONS (3 emails):
  - newsletter@shop.com: 50% off sale
  ... and 2 more
```

---

## 📊 Data Storage Explained

### Where Your Data Stays

Everything is stored **on your computer only**:

| File/Folder | Purpose |
|-------------|---------|
| `email_assistant.db` | SQLite database with all emails |
| `token_<account>.json` | Gmail API access token (encrypted, one per user) |
| `credentials.json` | Your OAuth credentials |
| Dashboard cache | Temporary browser cache |

### Database Structure

The SQLite database stores:
```
emails table:
- message_id (unique Gmail ID)
- sender (email address)
- subject (email subject)
- timestamp (when received)
- body_preview (first 200 chars)
- category (college, placement, etc.)
- priority (0 or 1)
- summary (AI-generated)

daily_summaries table:
- date (YYYY-MM-DD)
- summary_text (full summary)
- email_count (how many emails)
```

---

## 🔄 Example: Complete Flow

### Day 1 - Setup
1. Install credentials.json
2. Set TEST_MODE = False
3. First "Process New Emails" click
4. OAuth flow completes
5. 50 unread emails fetched

### Day 1 - Processing
1. Each email parsed (sender, subject, etc.)
2. Categorized: college (10), placement (15), personal (20), promotions (5)
3. Priority detected: 3 urgent emails
4. All stored in database
5. Dashboard shows: 50 emails, organized by category

### Day 2 - Daily Summary (6 PM)
1. Scheduler runs automatically
2. Reads all emails from Day 1
3. Groups by category
4. Generates summary
5. Email sent to you with summary
6. You receive: "Your daily email summary: 50 emails processed, 3 urgent"

### Day 3 - Continue
1. New emails arrive
2. Click "Process New Emails" anytime
3. App fetches new unread emails
4. Adds to existing database
5. Dashboard updates

---

## 🎮 Test It Now

### Option A: Keep Using Demo (No Setup)
- Already working ✅
- See how categorization works
- Understand the interface
- No Gmail needed

### Option B: Switch to Real Gmail (Recommended)
1. Follow steps above (Google Cloud Console)
2. Set TEST_MODE = False
3. Click "Process New Emails"
4. Authorize Gmail
5. See your real emails categorized!

---

## ❓ Common Questions

**Q: Is my email safe?**
A: Yes! Only read-only access. All data stored locally on your computer.

**Q: What if I revoke access?**
A: Go to Google Account Settings > Connected Apps > Disconnect "Email Assistant"

**Q: Can the app send emails for me?**
A: No, only read emails. Notifications are sent FROM your account but you control both.

**Q: What happens to old emails?**
A: Stays in database until you manually delete or clear database.

**Q: Multiple Gmail accounts?**
A: Yes! Use different `account_id` parameters in code.

**Q: How often to process emails?**
A: Anytime! Click button, or wait for daily summary at 6 PM.

---

## 📝 Current Setup Status

| Feature | Status | What's Needed |
|---------|--------|--------------|
| Web Dashboard | ✅ Working | None |
| User Login/Register | ✅ Working | None |
| Email Categorization | ✅ Working | Gmail API credentials |
| Demo Emails | ✅ Working | None |
| Priority Detection | ✅ Working | Real emails |
| AI Summarization | ✅ Working | Real emails |
| Daily Summaries | ✅ Working | Gmail setup |
| Email Notifications | ✅ Working | Gmail setup |
| Database Storage | ✅ Working | None |

---

## 🎯 Next Steps

**Choose your path:**

### Path 1: Learn with Demo Data ✅ (5 minutes)
- Already set up
- Click "Process New Emails"
- See all features work
- Understand before Gmail setup

### Path 2: Connect Real Gmail 🔑 (30 minutes)
- Follow Google Cloud Console steps
- Save credentials.json
- Set TEST_MODE = False
- Click "Process New Emails"
- Authorize Gmail
- Enjoy real email management!

Pick whichever you prefer! Both work perfectly.
