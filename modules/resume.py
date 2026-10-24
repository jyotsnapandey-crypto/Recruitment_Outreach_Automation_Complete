from pathlib import Path
from .matcher import matching_keywords, match_score

def extract_resume_text(path):
    path = Path(path)
    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8", errors="replace")
    raise ValueError("This starter version supports .txt resumes. DOCX/PDF parsing is listed as future scope.")

def tailor_resume_text(resume_text, job_description, role):
    if not (job_description or "").strip():
        return f"""RESUME TAILORING REVIEW — {role}

NO MATCH REPORT GENERATED
A job description is required to calculate keyword overlap. Add the complete job description and run this review again.

ORIGINAL RESUME TEXT:
{resume_text}
"""
    result = matching_keywords(resume_text, job_description)
    score = match_score(resume_text, job_description)
    matched = ", ".join(result["matched"]) or "No clear overlapping keywords found"
    gaps = ", ".join(result["potential_gaps"]) or "No major keyword gaps detected"
    return f"""RESUME TAILORING REVIEW — {role}

KEYWORD OVERLAP ESTIMATE: {score}%

KEYWORDS ALREADY PRESENT:
{matched}

POTENTIAL KEYWORDS TO REVIEW:
{gaps}

SUGGESTED ACTIONS:
1. Keep the original facts, dates, education, skills, and achievements accurate.
2. If a potential keyword genuinely reflects your experience, consider mentioning it in the most relevant section.
3. Prioritize the projects and experience most relevant to this role.
4. Do not add a technology or qualification you do not have.

ORIGINAL RESUME TEXT:
{resume_text}
"""
