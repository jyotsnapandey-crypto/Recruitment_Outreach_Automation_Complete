# Recruitment and Outreach Automation System


## Interface design
The app uses a responsive light theme with a gradient hero banner, clearer navigation, styled metric cards, rounded forms, and mobile-friendly spacing. The UI is built with Streamlit and CSS; no separate frontend build step is required.

## Overview
A runnable Python + Streamlit prototype inspired by the supplied 11-page technical specification. It supports job lead management, keyword-based resume review, outreach email drafting, follow-up tracking, SQLite persistence, and CSV exports.

## Features implemented
1. Dashboard with counts for leads, shortlisted leads, drafts, sent outreach, and replies.
2. Add job leads with company, role, location, recruiter contact, URL, and job description.
3. Update job lead status.
4. Resume assistant using keyword overlap and transparent tailoring suggestions.
5. Generate and save editable outreach email drafts.
6. Update outreach status, including sent/replied/follow-up states.
7. Follow-up tracker and editable follow-up template.
8. Export job and outreach records to CSV.
9. SQLite persistence.
10. Unit tests for matching and email drafting.

## Requirements
- Python 3.10+
- Windows, macOS, or Linux
- Internet connection to install dependencies

## Deploy on Streamlit Community Cloud
1. Upload this project folder to a GitHub repository (include `app.py`, `modules/`, `requirements.txt`, `README.md`, and `sample_data/`).
2. Open https://share.streamlit.io/ and sign in with GitHub.
3. Choose **Create app**, select the repository and branch, and set the main file path to `app.py`.
4. Deploy and share the generated `https://...streamlit.app` URL.
5. Test the link in a private/incognito window. Do not commit `.env` files, passwords, API keys, or private recruiter data.

**Hosting note:** Streamlit Community Cloud's local filesystem is not a production database; SQLite data may be lost when the app is restarted or redeployed. This prototype is suitable for demonstration. For durable multi-user deployment, connect a managed database and add authentication.

## Run locally
Open this folder in VS Code and run in the terminal:

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
streamlit run app.py
```

Run tests:
```bash
pytest -q
```

## Demo flow
1. Add a sample job lead such as “Python Developer” and enter a short sample job description.
2. Open Resume Assistant and paste sample resume text.
3. Generate tailoring suggestions and download the text file.
4. Open Outreach, generate an email draft, review it, and save it.
5. Update the status to Sent or Replied to demonstrate tracking.
6. Open Reports and download both CSV exports.

## Project structure
- `app.py`: Streamlit interface and navigation
- `modules/db.py`: SQLite storage and status updates
- `modules/matcher.py`: keyword matching and overlap score
- `modules/resume.py`: resume review suggestions
- `modules/drafts.py`: outreach email draft generation
- `modules/reporting.py`: CSV export helper
- `tests/test_core.py`: unit tests
- `PROJECT_REPORT.md`: report for submission
- `data/`: local SQLite database is created here at runtime
- `sample_data/`: sample input data

## Scope and transparency
This is a runnable academic/demo prototype, not a full production implementation of every integration described in the original blueprint. The following are not implemented in this two-hour starter: automated LinkedIn scraping, Gemini/Groq/OpenRouter API calls, DOCX/PDF layout-preserving resume rewriting, live Gmail SMTP sending, IMAP reply syncing, and actual threaded follow-ups. The UI provides manual workflows and tracking placeholders for those features.

Do not claim integrations are live unless you implement and test them. Automated scraping and unsolicited bulk outreach can violate platform or email-provider rules. Use authorized data sources, review every message, respect opt-outs, and protect credentials and personal data.
