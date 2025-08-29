# Inbox Zero Agent


This project contains a simple email‑management **agent** written in Python that
helps you apply the *Inbox Zero* philosophy to your day‑to‑day messages.  The
Inbox Zero concept was popularized by Merlin Mann in 2006 and encourages you
to keep your inbox as close to empty as possible【318550582690369†L58-L64】.  By
processing each message immediately—choosing whether to **do**, **defer**,
**delegate** or **delete**—you reduce the mental clutter associated with
email【318550582690369†L68-L73】.  While many commercial tools implement this
approach, this repository demonstrates how you can build your own lightweight
agent to prioritize, summarize and declutter emails.

## Features

- **Email prioritization:** Assigns `High`, `Medium` or `Low` priority based on
  simple keyword heuristics (e.g. “urgent”, “invoice”).  Important messages
  surface to the top of your queue.
- **Summarization:** Extracts a short summary from the body of each email
  using sentence splitting.  This gives you a quick overview without reading
  the entire message.
- **Draft reply generation:** Produces a basic reply tailored to common
  scenarios such as meeting requests, invoices or general enquiries.  The
  replies are template‑based placeholders that you can edit before sending.
- **Decluttering:** Categorizes messages into `General`, `Newsletter`,
  `Promotions` or `Social` based on the sender’s address, helping you
  archive or filter newsletters and marketing emails automatically.

## Installation

This agent is implemented in pure Python and does not require any external
dependencies beyond the standard library.  To use it, clone this repository
and ensure you have Python 3.8 or later installed.  You can run the script
directly:

```bash
python inbox_zero_agent.py --email-dir path/to/emails --output processed_emails.json
```

The `--email-dir` argument points to a directory containing your sample
emails (see below for the expected format), and `--output` controls the name
of the JSON file where results will be written.

## Sample email format

For demonstration purposes, the agent reads plain‑text files rather than
connecting to an actual mail server.  Each file should end with a `.txt`
extension and may include optional header lines:

```
Subject: Lunch meeting next Wednesday
From: alice@example.com

Hi Bob,

Can we schedule a lunch meeting next Wednesday at noon? I’d like to discuss
project updates and upcoming deadlines.

Cheers,
Alice
```

Lines starting with `Subject:` and `From:` are parsed as metadata; all
subsequent lines form the email body.  Place as many sample files as you
like in the directory you provide via `--email-dir`.

## How it works

1. **Load emails:** The script reads each `.txt` file in the given directory
   and constructs an `Email` object containing the filename, subject,
   sender and body.
2. **Prioritize:** Using a set of hard‑coded keywords, it determines
   whether the message is high, medium or low priority.  For example,
   messages mentioning “urgent” or “deadline” are marked as high.
3. **Summarize:** The body of each email is split into sentences using a
   regular expression.  The first two sentences are joined to produce a
   concise summary.  If fewer sentences are available, the full body is
   returned.
4. **Draft replies:** A few simple conditional checks look for words like
   “meeting” or “invoice” and return an appropriate template.  Generic
   replies are used when no specific context is detected.
5. **Categorize:** The sender’s address is analysed for patterns such
   as “newsletter” or “promo” to assign the message to one of four
   high‑level categories, illustrating how automatic filing could work.
6. **Save results:** Finally, all processed data (priority, summary, draft
   reply and category) is written to a JSON file for further use.

## Future improvements

This project intentionally keeps the logic simple to illustrate the core
concepts behind an Inbox Zero agent.  In a real‑world application you could:

- Connect to a mail server via IMAP or the Gmail API to process live
  messages.
- Replace keyword heuristics with machine‑learning models or large language
  models for more nuanced prioritization and summarization.
- Integrate a vector database to search past email history when drafting
  replies【512207302045658†L212-L219】.
- Provide a user interface (web or CLI) that allows you to review drafts and
  confirm or edit actions before they are taken.

## License

This example is provided for educational purposes.  Refer to the `LICENSE`
file for details.
