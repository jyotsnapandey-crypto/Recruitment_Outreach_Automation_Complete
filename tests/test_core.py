from modules.matcher import match_score, matching_keywords
from modules.drafts import generate_email_draft

def test_match_score_basic():
    assert match_score("Python SQL REST API", "Python SQL REST API") == 100

def test_match_score_empty_job():
    assert match_score("Python SQL", "") == 0

def test_match_score_normalizes_framework_aliases():
    assert match_score("React.js Node.js REST APIs", "React Node REST API") == 100

def test_keyword_match():
    result = matching_keywords("Python Flask", "Python Flask React")
    assert "python" in result["matched"]
    assert "react" in result["potential_gaps"]

def test_missing_description_is_explicit():
    from modules.resume import tailor_resume_text
    result = tailor_resume_text("Python developer", "", "Python Developer")
    assert "NO MATCH REPORT GENERATED" in result

def test_email_draft():
    subject, body = generate_email_draft("Alex", {
        "company": "ExampleCo", "role": "Python Developer", "recruiter_name": "Sam"
    }, "Python, Flask")
    assert "Python Developer" in subject
    assert "ExampleCo" in body
    assert "Alex" in body
