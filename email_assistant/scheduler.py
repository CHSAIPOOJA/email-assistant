# email_assistant/scheduler.py
"""
Scheduler module for automated tasks.

This module handles scheduling of daily summary generation
and other automated email assistant tasks.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from email_assistant.summarizer import generate_daily_summary
from email_assistant.notifier import send_daily_summary_notification
from email_assistant.config import DAILY_SUMMARY_HOUR
from datetime import datetime

def init_scheduler(app):
    """
    Initializes the background scheduler for automated tasks.

    Args:
        app: Flask application instance

    Returns:
        BackgroundScheduler: Configured scheduler instance
    """
    scheduler = BackgroundScheduler()

    # Schedule daily summary generation
    scheduler.add_job(
        func=generate_daily_summary_job,
        trigger=CronTrigger(hour=DAILY_SUMMARY_HOUR, minute=0),
        id='daily_summary',
        name='Generate Daily Email Summary',
        replace_existing=True
    )

    # Schedule daily notification (1 hour after summary)
    scheduler.add_job(
        func=send_daily_notification_job,
        trigger=CronTrigger(hour=DAILY_SUMMARY_HOUR + 1, minute=0),
        id='daily_notification',
        name='Send Daily Summary Notification',
        replace_existing=True
    )

    return scheduler

def generate_daily_summary_job():
    """
    Job function to generate daily summary.
    """
    try:
        print("Generating daily summary...")
        summary = generate_daily_summary()
        print("Daily summary generated successfully.")
        print(summary)
    except Exception as e:
        print(f"Error generating daily summary: {e}")

def send_daily_notification_job():
    """
    Job function to send daily summary notification.
    """
    try:
        print("Sending daily summary notification...")
        # Get yesterday's date
        yesterday = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)).strftime('%Y-%m-%d')
        send_daily_summary_notification(yesterday)
        print("Daily notification sent.")
    except Exception as e:
        print(f"Error sending daily notification: {e}")

def run_manual_summary(account_id='default'):
    """
    Manually trigger daily summary generation.

    Args:
        account_id (str): Account identifier
    """
    try:
        summary = generate_daily_summary(account_id=account_id)
        print("Manual summary generated:")
        print(summary)
        return summary
    except Exception as e:
        print(f"Error in manual summary: {e}")
        return None

def run_manual_notification(date=None):
    """
    Manually trigger daily summary notification.

    Args:
        date (str): Date for notification (default: yesterday)
    """
    if date is None:
        yesterday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)
        date = yesterday.strftime('%Y-%m-%d')

    try:
        send_daily_summary_notification(date)
        print(f"Manual notification sent for {date}")
    except Exception as e:
        print(f"Error in manual notification: {e}")