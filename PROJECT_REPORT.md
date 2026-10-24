# Recruitment and Outreach Automation System
## Project Report

### 1. Abstract
This project is a local web application prototype that organizes job leads and recruitment outreach in one interface. It helps a user save role and recruiter details, review resume/job keyword overlap, create personalized email drafts, track communication statuses, and export records for reporting.

### 2. Problem Statement
Job search and recruiter outreach can involve repetitive manual work: recording opportunities, comparing requirements with resume content, drafting messages, and tracking whether a response has arrived. A centralized workflow can make these tasks easier to organize.

### 3. Objectives
- Store job leads and recruiter details.
- Compare resume text with a job description using transparent keyword overlap.
- Suggest areas to review when tailoring resume content.
- Create editable outreach email drafts.
- Track outreach statuses and follow-up candidates.
- Export records as CSV for analysis.

### 4. Technology Stack
- Python: core logic
- Streamlit: web user interface
- SQLite: local relational database
- Pandas: table display and CSV exports
- Pytest: unit testing

### 5. System Architecture
The Streamlit interface collects input and calls modules for database operations, matching, resume suggestions, email drafting, and CSV reporting. SQLite stores job leads and outreach records. The user reviews resume suggestions and email drafts before using them.

### 6. Database Design
**Jobs table:** id, company, role, location, recruiter name/email, job URL, job description, status, created timestamp.

**Outreach table:** id, job ID, candidate name/email, subject, email body, status, created timestamp, updated timestamp. Each outreach record references a job lead.

### 7. Main Modules
- Dashboard: summarizes records and activity.
- Job Leads: add leads and update lead status.
- Resume Assistant: computes keyword overlap and generates review suggestions.
- Outreach: generates, edits, saves and tracks email drafts.
- Follow-ups: lists outreach marked sent or awaiting a reply and provides a template.
- Reports: downloads job and outreach CSV files.

### 8. Algorithm: Keyword Overlap
The matching module normalizes common technology aliases, removes common stopwords, and compares relevant technical terms where recognized. If no technical terms are detected, it falls back to remaining content words. The interface blocks analysis when the job description is empty. The overlap estimate is:

Overlap (%) = 100 × (number of distinct job-description terms found in resume / number of distinct job-description terms)

This is a simple heuristic, not a machine-learning model or a hiring recommendation. Alias normalization is limited and results depend on wording; the score may not reflect semantic similarity or actual qualification.

### 9. Privacy and Responsible Use
The prototype does not scrape LinkedIn or send emails automatically. Messages require human review and manual sending. Use only authorized job data, avoid unsolicited bulk messaging, honor opt-outs, and do not commit credentials, cookies, API keys, or personal recruiter data to a public repository.

### 10. Limitations
- No automatic LinkedIn integration.
- No external generative AI API integration.
- Resume upload currently supports plain-text files rather than DOCX/PDF layout-preserving editing.
- No live Gmail SMTP/IMAP integration.
- Follow-up status is manually tracked.
- Keyword overlap is a basic heuristic and can miss synonyms or context.

### 11. Future Scope
- Add approved job-source connectors.
- Add optional LLM integration with output validation.
- Parse DOCX/PDF resumes while preserving formatting.
- Add consent-based email integration and rate limits.
- Synchronize replies through an authorized mail API.
- Add stronger authentication, logging, integration tests, and deployment.

### 12. Conclusion
The prototype demonstrates the core workflow of lead organization, resume keyword review, outreach drafting, status tracking, and reporting. It provides a practical foundation for implementing the wider system described in the technical specification.
