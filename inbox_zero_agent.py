#!/usr/bin/env python3
"""
Inbox Zero Agent
=================

This script provides a simple email‑management agent to help users implement the
“Inbox Zero” methodology.  Productivity experts describe Inbox Zero as a way
to reduce mental clutter by keeping your inbox as empty as possible; it was
popularized by Merlin Mann in 2006【318550582690369†L58-L64】.  The method
revolves around four basic actions: *do*, *defer*, *delegate* or
*delete*【318550582690369†L68-L73】.  By quickly deciding which of these
actions to take for each message, you can stop email overwhelm and free up
attention for more meaningful tasks【318550582690369†L58-L64】.

The agent in this script demonstrates core features inspired by that
philosophy:

* **Email prioritization:** classify messages as high, medium or low priority
  based on simple keyword heuristics (e.g. “urgent”, “invoice”).
* **Summarization:** extract a brief summary from each email body using
  sentence splitting.  This offers a quick overview without reading the
  entire message.
* **Draft reply generation:** produce a basic draft reply tailored to
  common scenarios such as scheduling meetings or acknowledging invoices.
* **Decluttering:** categorize each message as *General*, *Newsletter*,
  *Promotions* or *Social* so you can quickly archive or filter them.

This prototype does not connect to real email servers; instead it reads
plain‑text files from a directory to represent emails.  For a production
system you could integrate with the Gmail API or other mail services and
replace the heuristics with machine‑learning models or large language
models.  Nonetheless, this example illustrates how an agent can automate
routine triage while aligning with the Inbox Zero philosophy.

Usage
-----

Create a directory containing sample emails stored as ``.txt`` files.  Each
file should include optional ``Subject:`` and ``From:`` lines followed by
the body of the email.  Then run:

```
python inbox_zero_agent.py --email-dir path/to/emails --output processed_emails.json
```

The script will print how many emails were processed and save a JSON file
containing the prioritization, summary, draft reply and category for each
email.
"""

from dataclasses import dataclass
import os
import re
import json
import argparse
from typing import List, Dict


@dataclass
class Email:
    """Simple representation of an email with minimal metadata."""
    filename: str
    subject: str
    sender: str
    body: str


def load_emails(email_dir: str) -> List[Email]:
    """
    Load plain‑text emails from a directory.

    Each ``.txt`` file may start with optional ``Subject:`` and ``From:``
    headers.  The remainder of the file is treated as the email body.  Lines
    not starting with these headers are concatenated into a single body.

    Args:
        email_dir: Path to the directory containing ``.txt`` files.

    Returns:
        A list of ``Email`` objects.
    """
    emails: List[Email] = []
    for filename in sorted(os.listdir(email_dir)):
        if not filename.lower().endswith(".txt"):
            continue
        path = os.path.join(email_dir, filename)
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            # Skip unreadable files
            continue
        subject = ""
        sender = ""
        body_lines: List[str] = []
        for line in lines:
            # Normalize header names to lower case for matching
            lower = line.strip().lower()
            if lower.startswith("subject:"):
                subject = line.split(":", 1)[1].strip()
            elif lower.startswith("from:"):
                sender = line.split(":", 1)[1].strip()
            else:
                body_lines.append(line.rstrip())
        body = " ".join(body_lines).strip()
        emails.append(Email(filename=filename, subject=subject, sender=sender, body=body))
    return emails


def classify_priority(email: Email) -> str:
    """
    Determine the priority of an email based on simple keyword heuristics.

    High priority keywords include “urgent”, “asap”, “meeting”, “invoice”,
    “payment”, “deadline”.  Medium priority keywords include “reply”,
    “question”, “help” and “request”.  Everything else is considered low.

    Args:
        email: The email to classify.

    Returns:
        One of ``"High"``, ``"Medium"`` or ``"Low"``.
    """
    high_keywords = {"urgent", "asap", "meeting", "invoice", "payment", "deadline"}
    medium_keywords = {"reply", "question", "help", "request"}
    text = f"{email.subject} {email.body}".lower()
    if any(word in text for word in high_keywords):
        return "High"
    if any(word in text for word in medium_keywords):
        return "Medium"
    return "Low"


def summarize_email(email: Email, max_sentences: int = 2) -> str:
    """
    Create a short summary of an email body by extracting the first few sentences.

    Sentences are split using a simple regular expression that looks for
    punctuation followed by a space.  If the body has fewer than
    ``max_sentences`` sentences, the entire body is returned.

    Args:
        email: The email to summarize.
        max_sentences: Maximum number of sentences to include in the summary.

    Returns:
        A summary string.
    """
    # Use regex to split on period, exclamation or question mark followed by space
    sentences = re.split(r"(?<=[.!?]) +", email.body)
    # Filter out empty sentences and strip whitespace
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return ""
    summary = " ".join(sentences[:max_sentences])
    return summary


def generate_draft_reply(email: Email) -> str:
    """
    Generate a naive draft reply based on the content of an email.

    Simple keyword matching triggers different reply templates.  This is a
    placeholder for more sophisticated AI models in a production system.

    Args:
        email: The email for which to generate a draft.

    Returns:
        A string containing a draft reply.
    """
    lower_body = email.body.lower()
    lower_subject = email.subject.lower()
    # Meeting or scheduling
    if "meeting" in lower_body or "meeting" in lower_subject or "schedule" in lower_body:
        return (
            "Hi,\n\n"
            "Thank you for reaching out about scheduling a meeting. "
            "I'm reviewing my calendar and will propose some available times shortly.\n\n"
            "Best regards,"
        )
    # Invoice or payment
    if "invoice" in lower_body or "invoice" in lower_subject or "payment" in lower_body:
        return (
            "Hello,\n\n"
            "I have received your message regarding the invoice. "
            "I'll review the details and follow up with you soon.\n\n"
            "Kind regards,"
        )
    # Gratitude
    if "thank" in lower_body:
        return (
            "Hi,\n\n"
            "You're very welcome! Let me know if there's anything else you need.\n\n"
            "Best,"
        )
    # Generic default reply
    return (
        "Hello,\n\n"
        "Thank you for your email. I've received your message and will get back to you soon.\n\n"
        "Best regards,"
    )


def categorize_email(email: Email) -> str:
    """
    Assign a high‑level category to an email based on the sender's address.

    Categories include ``Newsletter``, ``Promotions``, ``Social`` and ``General``.
    The rules are simple and may not catch all cases, but they demonstrate how
    automatic filing could work.

    Args:
        email: The email to categorize.

    Returns:
        One of the category names as a string.
    """
    address = email.sender.lower()
    domain = address.split("@")[-1] if "@" in address else address
    # Newsletter addresses often include certain keywords
    if any(keyword in address for keyword in ["newsletter", "news", "update", "mailing"]):
        return "Newsletter"
    # Promotions or marketing domains
    if any(keyword in domain for keyword in ["promo", "marketing", "offers"]):
        return "Promotions"
    # Social network notifications
    if any(keyword in domain for keyword in ["social", "facebook", "linkedin", "twitter"]):
        return "Social"
    # Default category
    return "General"


def process_emails(emails: List[Email]) -> List[Dict[str, str]]:
    """
    Process a list of emails to assign priority, summary, draft reply and category.

    Args:
        emails: A list of ``Email`` objects.

    Returns:
        A list of dictionaries containing the processed results for each email.
    """
    results: List[Dict[str, str]] = []
    for email in emails:
        priority = classify_priority(email)
        summary = summarize_email(email)
        reply = generate_draft_reply(email)
        category = categorize_email(email)
        results.append(
            {
                "filename": email.filename,
                "subject": email.subject,
                "sender": email.sender,
                "priority": priority,
                "summary": summary,
                "draft_reply": reply,
                "category": category,
            }
        )
    return results


def save_results(results: List[Dict[str, str]], output_path: str) -> None:
    """
    Save processed email results to a JSON file.

    Args:
        results: A list of dictionaries returned by ``process_emails``.
        output_path: Path to the JSON file to write.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def main() -> None:
    """
    Command‑line entry point.

    Parses arguments for the email directory and output file, loads emails,
    processes them, and writes the results.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Inbox Zero Agent: prioritize, summarize and categorize emails to help you "
            "achieve inbox zero."
        )
    )
    parser.add_argument(
        "--email-dir",
        required=True,
        help="Directory containing plain text email files (.txt).",
    )
    parser.add_argument(
        "--output",
        default="results.json",
        help="Output JSON file to save processed emails (default: results.json).",
    )
    args = parser.parse_args()

    emails = load_emails(args.email_dir)
    if not emails:
        print(f"No .txt email files found in directory '{args.email_dir}'.")
        return
    results = process_emails(emails)
    save_results(results, args.output)
    print(f"Processed {len(results)} emails. Results saved to {args.output}.")


if __name__ == "__main__":
    main()