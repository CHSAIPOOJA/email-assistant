# email_assistant/processor.py
"""
Email processing pipeline.

This module orchestrates the entire email processing workflow:
fetch -> parse -> categorize -> summarize -> store
"""

from email_assistant.email_fetcher import fetch_unread_emails
from email_assistant.email_parser import parse_multiple_emails
from email_assistant.categorizer import batch_categorize
from email_assistant.summarizer import summarize_email_batch
from email_assistant.database import save_email, clear_emails
from email_assistant.auth import authenticate_gmail

def process_emails(account_id='default', max_emails=50):
    # account_id should uniquely identify a user (email is fine)
    """
    Processes emails through the entire pipeline.

    Args:
        account_id (str): Account identifier
        max_emails (int): Maximum emails to process

    Returns:
        int: Number of emails processed
    """
    print(f"\n{'='*60}")
    print(f"🔄 STARTING EMAIL PROCESSING")
    print(f"{'='*60}")
    print(f"Account: {account_id}")
    print(f"Max emails: {max_emails}")

    try:
        # Clear existing emails to ensure fresh data
        print("\n[STEP 1] Clearing old emails...")
        clear_emails(account_id)
        print("✅ Old emails cleared")

        # Step 1: Fetch unread emails
        print("\n[STEP 2] Fetching unread emails from Gmail...")
        raw_emails = fetch_unread_emails(account_id, max_emails)
        print(f"✅ Fetched {len(raw_emails)} emails")

        if not raw_emails:
            print("\n⚠️  No unread emails to process.")
            print(f"{'='*60}\n")
            return 0

        # Step 2: Parse emails
        print("\n[STEP 3] Parsing emails...")
        parsed_emails = parse_multiple_emails(raw_emails, account_id)
        print(f"✅ Parsed {len(parsed_emails)} emails")

        # Step 3: Categorize emails
        print("\n[STEP 4] Categorizing emails...")
        categorized_emails = batch_categorize(parsed_emails)
        print(f"✅ Categorized {len(categorized_emails)} emails")

        # Step 4: Summarize emails
        print("\n[STEP 5] Summarizing emails...")
        summarized_emails = summarize_email_batch(categorized_emails)
        print(f"✅ Summarized {len(summarized_emails)} emails")

        # Step 5: Save to database
        print("\n[STEP 6] Saving to database...")
        for i, email in enumerate(summarized_emails, 1):
            save_email(email)
            print(f"   - Saved email {i}/{len(summarized_emails)}")
        print(f"✅ All emails saved")

        print(f"\n{'='*60}")
        print(f"✅ SUCCESS: Processed {len(summarized_emails)} emails")
        print(f"{'='*60}\n")
        return len(summarized_emails)

    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ ERROR IN EMAIL PROCESSING")
        print(f"{'='*60}")
        print(f"Error: {e}")
        print(f"Type: {type(e).__name__}")
        print(f"{'='*60}\n")
        raise

def run_full_pipeline(account_id='default'):
    """
    Runs the complete email assistant pipeline.

    Args:
        account_id (str): Account identifier
    """
    # Process emails
    processed_count = process_emails(account_id)

    if processed_count > 0:
        # Generate daily summary
        from email_assistant.summarizer import generate_daily_summary
        print("Generating daily summary...")
        summary = generate_daily_summary(account_id)
        print("Daily summary generated.")

    print("Email processing pipeline completed.")

if __name__ == '__main__':
    # Run the pipeline
    run_full_pipeline()