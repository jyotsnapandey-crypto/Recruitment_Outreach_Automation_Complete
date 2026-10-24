def generate_email_draft(candidate_name, job, skills):
    name = candidate_name.strip() or "[Your name]"
    recruiter = (job.get("recruiter_name") or "").strip() or "there"
    company = job.get("company") or "your company"
    role = job.get("role") or "the role"
    skills_text = skills.strip() or "[Add relevant skills you genuinely have]"
    subject = f"Interest in {role} opportunity"
    body = f"""Hi {recruiter},

I came across the {role} opportunity at {company} and wanted to express my interest.

My relevant skills include {skills_text}. I would welcome the opportunity to discuss how my actual experience aligns with the role. I have attached my resume for your consideration.

Thank you for your time.

Best regards,
{name}"""
    return subject, body
