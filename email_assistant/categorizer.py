# email_assistant/categorizer.py
"""
Email categorization module using keyword matching and NLP.

This module categorizes emails into predefined categories and detects priority emails.
It uses keyword matching for categorization and priority detection.
"""

from email_assistant.config import CATEGORY_KEYWORDS, PRIORITY_KEYWORDS, EMAIL_CATEGORIES
import re

# Try to load spacy model, fallback to keyword-only if not available
try:
    import spacy
    nlp = spacy.load('en_core_web_sm')
    SPACY_AVAILABLE = True
except Exception as e:
    print(f"spaCy not available: {e}")
    SPACY_AVAILABLE = False

def categorize_email(parsed_email):
    """
    Categorizes an email and detects if it's priority.

    Args:
        parsed_email (dict): Parsed email data from email_parser

    Returns:
        dict: Updated email data with category and priority
    """
    subject = parsed_email['subject'].lower()
    body = parsed_email['full_body'].lower()
    sender = parsed_email['sender_email'].lower()

    # Combine subject and body for analysis
    text = subject + ' ' + body

    # Detect priority
    priority = detect_priority(text)

    # Categorize email
    category = categorize_by_keywords(text, sender)

    # Update email data
    parsed_email['category'] = category
    parsed_email['priority'] = priority

    return parsed_email

def detect_priority(text):
    """
    Detects if an email is priority based on keywords.

    Args:
        text (str): Combined subject and body text

    Returns:
        int: 1 if priority, 0 otherwise
    """
    for keyword in PRIORITY_KEYWORDS:
        if keyword.lower() in text:
            return 1
    return 0

def categorize_by_keywords(text, sender):
    """
    Categorizes email based on keyword matching.

    Args:
        text (str): Combined subject and body text
        sender (str): Sender email address

    Returns:
        str: Email category
    """
    # Count keyword matches for each category
    category_scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Count occurrences (case-insensitive)
            score += len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text))
        category_scores[category] = score

    # Check for promotional senders (common domains)
    if any(domain in sender for domain in ['newsletter', 'promotion', 'deal', 'offer']):
        category_scores['promotions'] += 10

    # Find category with highest score
    max_score = max(category_scores.values())
    if max_score == 0:
        return 'personal'  # Default category

    # Get categories with max score
    top_categories = [cat for cat, score in category_scores.items() if score == max_score]

    # If tie, prefer certain categories
    preference_order = ['important', 'placement', 'college', 'promotions', 'personal']
    for pref_cat in preference_order:
        if pref_cat in top_categories:
            return pref_cat

    return top_categories[0]

def categorize_with_nlp(text):
    """
    Advanced categorization using spaCy NLP (if available).

    Args:
        text (str): Text to analyze

    Returns:
        str: Suggested category based on NLP analysis
    """
    if not SPACY_AVAILABLE:
        return None

    try:
        doc = nlp(text)

        # Simple NLP-based categorization
        # Check for organizations (might indicate college/university)
        orgs = [ent.text.lower() for ent in doc.ents if ent.label_ == 'ORG']
        if any(word in ' '.join(orgs) for word in ['university', 'college', 'school']):
            return 'college'

        # Check for job-related terms
        job_terms = ['job', 'position', 'hiring', 'application', 'interview']
        if any(term in text for term in job_terms):
            return 'placement'

        # Check for monetary values (might indicate promotions)
        money_entities = [ent for ent in doc.ents if ent.label_ == 'MONEY']
        if money_entities:
            return 'promotions'

    except Exception as e:
        print(f"NLP categorization error: {e}")

    return None

def batch_categorize(emails):
    """
    Categorizes multiple emails.

    Args:
        emails (list): List of parsed email dictionaries

    Returns:
        list: List of categorized email dictionaries
    """
    categorized_emails = []
    for email in emails:
        categorized = categorize_email(email)
        categorized_emails.append(categorized)

    return categorized_emails