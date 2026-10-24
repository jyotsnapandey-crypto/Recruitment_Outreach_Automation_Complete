import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "outreach.db"

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL, role TEXT NOT NULL, location TEXT DEFAULT '',
            recruiter_name TEXT DEFAULT '', recruiter_email TEXT DEFAULT '',
            job_url TEXT DEFAULT '', job_description TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'New', created_at TEXT NOT NULL
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS outreach (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL, candidate_name TEXT DEFAULT '',
            candidate_email TEXT DEFAULT '', subject TEXT NOT NULL, email_body TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Draft', created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE
        )""")

def add_job(company, role, location="", recruiter_name="", recruiter_email="", job_url="", job_description=""):
    now = datetime.now().isoformat(timespec="seconds")
    with connect() as conn:
        cur = conn.execute("""INSERT INTO jobs
            (company, role, location, recruiter_name, recruiter_email, job_url, job_description, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'New', ?)""",
            (company.strip(), role.strip(), location.strip(), recruiter_name.strip(),
             recruiter_email.strip(), job_url.strip(), job_description.strip(), now))
        return cur.lastrowid

def list_jobs():
    with connect() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM jobs ORDER BY id DESC").fetchall()]

def update_job_status(job_id, status):
    with connect() as conn:
        conn.execute("UPDATE jobs SET status=? WHERE id=?", (status, job_id))

def add_outreach(job_id, candidate_name, candidate_email, subject, email_body):
    now = datetime.now().isoformat(timespec="seconds")
    with connect() as conn:
        cur = conn.execute("""INSERT INTO outreach
            (job_id, candidate_name, candidate_email, subject, email_body, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'Draft', ?, ?)""",
            (job_id, candidate_name, candidate_email, subject, email_body, now, now))
        return cur.lastrowid

def list_outreach():
    with connect() as conn:
        rows = conn.execute("""SELECT o.*, j.company, j.role, j.recruiter_name, j.recruiter_email
            FROM outreach o JOIN jobs j ON j.id=o.job_id ORDER BY o.id DESC""").fetchall()
        return [dict(row) for row in rows]

def update_outreach_status(outreach_id, status):
    now = datetime.now().isoformat(timespec="seconds")
    with connect() as conn:
        conn.execute("UPDATE outreach SET status=?, updated_at=? WHERE id=?", (status, now, outreach_id))

def dashboard_stats():
    jobs = list_jobs()
    out = list_outreach()
    return {
        "Total leads": len(jobs),
        "Shortlisted": sum(j["status"] == "Shortlisted" for j in jobs),
        "Outreach drafts": sum(o["status"] == "Draft" for o in out),
        "Sent": sum(o["status"] == "Sent" for o in out),
        "Replies": sum(o["status"] == "Replied" for o in out),
    }
