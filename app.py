from pathlib import Path
import streamlit as st
import pandas as pd
from modules.db import init_db, list_jobs, list_outreach, add_job, update_job_status, add_outreach, update_outreach_status, dashboard_stats
from modules.matcher import match_score
from modules.drafts import generate_email_draft
from modules.resume import extract_resume_text, tailor_resume_text
from modules.reporting import build_csv_bytes

st.set_page_config(page_title="Recruitment & Outreach Automation", page_icon="📨", layout="wide", initial_sidebar_state="expanded")
init_db()

# Clean, responsive visual theme. Streamlit components remain accessible and functional.
st.markdown("""
<style>
:root { --ink:#172033; --muted:#65718a; --brand:#4f46e5; --brand2:#7c3aed; --line:#e5e9f2; }
.stApp { background: linear-gradient(180deg, #f7f8ff 0%, #f8fafc 42%, #ffffff 100%); color:var(--ink); }
[data-testid="stHeader"] { background:rgba(248,250,252,.82); }
.block-container { max-width: 1440px; padding-top: 1.8rem; padding-bottom: 3rem; }
[data-testid="stSidebar"] { background: linear-gradient(180deg,#171b34 0%,#252a4a 100%); }
[data-testid="stSidebar"] * { color:#f7f8ff !important; }
[data-testid="stSidebar"] [data-testid="stAlert"] { background:rgba(255,255,255,.10); border:1px solid rgba(255,255,255,.15); }
.hero { padding: 1.65rem 1.8rem; border-radius: 22px; background:linear-gradient(120deg,#312e81 0%,#4f46e5 48%,#7c3aed 100%); color:white; margin-bottom:1.15rem; box-shadow:0 16px 38px rgba(79,70,229,.18); }
.hero-kicker { font-size:.76rem; font-weight:800; text-transform:uppercase; letter-spacing:.14em; opacity:.8; margin-bottom:.45rem; }
.hero h1 { color:white !important; font-size:clamp(1.7rem,3vw,2.45rem) !important; line-height:1.15; margin:0 0 .55rem 0; letter-spacing:-.035em; }
.hero p { color:#e8eaff !important; margin:0; max-width:850px; font-size:1rem; }
.hero-chip { display:inline-block; margin-top:1rem; border:1px solid rgba(255,255,255,.28); background:rgba(255,255,255,.13); border-radius:999px; padding:.35rem .7rem; font-size:.8rem; }
h2, h3 { letter-spacing:-.025em; color:#202744; }
[data-testid="stTabs"] [role="tablist"] { gap:.45rem; border-bottom:1px solid var(--line); }
[data-testid="stTabs"] button[role="tab"] { border-radius:10px 10px 0 0; padding:.7rem 1rem; font-weight:650; }
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] { background:#eef2ff; color:#4338ca; }
[data-testid="stMetric"] { background:white; border:1px solid var(--line); border-radius:16px; padding:1rem 1.05rem; box-shadow:0 4px 14px rgba(25,35,75,.035); }
[data-testid="stMetricLabel"] { color:#65718a; font-weight:650; }
[data-testid="stMetricValue"] { color:#28265f; }
[data-testid="stForm"], [data-testid="stExpander"], [data-testid="stDataFrame"] { border-radius:14px; }
[data-testid="stForm"] { border:1px solid var(--line); padding:1rem; background:rgba(255,255,255,.78); }
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stSelectbox"] [data-baseweb="select"] > div { border-radius:10px; }
.stButton button, .stDownloadButton button, [data-testid="stFormSubmitButton"] button { border-radius:10px; font-weight:650; padding:.55rem 1rem; transition:transform .15s ease, box-shadow .15s ease; }
.stButton button[kind="primary"], [data-testid="stFormSubmitButton"] button[kind="primary"] { background:linear-gradient(100deg,#4f46e5,#6d28d9); border:0; }
.stButton button:hover, .stDownloadButton button:hover { transform:translateY(-1px); box-shadow:0 6px 15px rgba(79,70,229,.15); }
[data-testid="stAlert"] { border-radius:12px; }
[data-testid="stDataFrame"] { border:1px solid var(--line); overflow:hidden; }
.small-note { color:#69758e; font-size:.88rem; }
@media (max-width: 700px) { .block-container { padding:1rem .8rem 2rem; } .hero { padding:1.25rem; border-radius:16px; } [data-testid="stTabs"] [role="tablist"] { gap:0; } [data-testid="stTabs"] button[role="tab"] { padding:.55rem .55rem; font-size:.82rem; } }
</style>
<div class="hero">
  <div class="hero-kicker">Career workflow workspace</div>
  <h1>Recruitment &amp; Outreach Automation</h1>
  <p>Organize job leads, align your resume to each role, prepare thoughtful recruiter outreach, and keep your follow-ups in one calm, focused workspace.</p>
  <span class="hero-chip">✦ Prototype · Human-reviewed outreach · No automatic emails</span>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ✦ Your career workspace")
    st.caption("Recruitment workflow toolkit")
    st.write("Manage opportunities, prepare outreach, and track your progress.")
    st.info("Review all generated content. This prototype never sends messages automatically.")
    st.markdown("---")
    st.caption("Built with Python · Streamlit · SQLite")

tab_dashboard, tab_jobs, tab_resume, tab_outreach, tab_followups, tab_reports = st.tabs([
    "Dashboard", "Job Leads", "Resume Assistant", "Outreach", "Follow-ups", "Reports"
])

with tab_dashboard:
    st.markdown("<p class='small-note'>Your job-search activity at a glance. Counts update as you add leads and manage outreach.</p>", unsafe_allow_html=True)
    stats = dashboard_stats()
    cols = st.columns(5)
    for col, (label, value) in zip(cols, stats.items()):
        col.metric(label, value)
    st.subheader("Recent job leads")
    jobs = list_jobs()
    if jobs:
        st.dataframe(pd.DataFrame(jobs), use_container_width=True, hide_index=True)
    else:
        st.info("No leads yet. Open Job Leads and add the included sample opportunity or your own authorized lead.")
    st.subheader("Recent outreach activity")
    out = list_outreach()
    if out:
        st.dataframe(pd.DataFrame(out), use_container_width=True, hide_index=True)
    else:
        st.caption("Outreach drafts will appear here after you create them.")

with tab_jobs:
    st.subheader("Add a job lead")
    if not list_jobs():
        st.info("New here? Load a clearly labelled demo lead to test the workflow, or enter your own opportunity below.")
        if st.button("Load demo job lead"):
            add_job(
                "Example Tech", "Python Developer", "Remote", "Sample Recruiter", "recruiter@example.com",
                "https://example.com/jobs/python-developer",
                "We are seeking a Python Developer with Python, SQL, REST APIs, Git, Flask, and problem-solving skills. "
                "The role involves building backend services, writing tests, working with databases, and collaborating with a team."
            )
            st.success("Demo lead added. Replace the sample details with a real opportunity before using it.")
            st.rerun()
    with st.form("add_job_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        company = c1.text_input("Company", placeholder="Example: Example Tech")
        role = c2.text_input("Target role", placeholder="Python Developer")
        location = c1.text_input("Location", value="United States")
        recruiter_name = c2.text_input("Recruiter name (optional)")
        recruiter_email = c1.text_input("Recruiter email (optional)")
        job_url = c2.text_input("Job post URL (optional)")
        description = st.text_area("Job description", height=140)
        submitted = st.form_submit_button("Save job lead", type="primary")
    if submitted:
        if not company.strip() or not role.strip():
            st.error("Company and target role are required.")
        else:
            add_job(company, role, location, recruiter_name, recruiter_email, job_url, description)
            st.success("Job lead saved.")
            st.rerun()

    st.divider()
    st.subheader("Job leads")
    jobs = list_jobs()
    if jobs:
        st.dataframe(pd.DataFrame(jobs), use_container_width=True, hide_index=True)
        ids = {f"#{j['id']} · {j['role']} at {j['company']}": j["id"] for j in jobs}
        selected_label = st.selectbox("Update lead status", list(ids.keys()))
        new_status = st.selectbox("Status", ["New", "Shortlisted", "Applied", "Closed", "Not relevant"])
        if st.button("Update selected lead"):
            update_job_status(ids[selected_label], new_status)
            st.success("Lead status updated.")
            st.rerun()
    else:
        st.caption("Your saved leads will appear here.")

with tab_resume:
    st.subheader("Resume Assistant")
    st.write("Extract text from a TXT resume or paste resume text. The assistant uses the job description to suggest truthful, role-aligned wording. It does not invent experience.")
    uploaded = st.file_uploader("Optional: upload a .txt resume", type=["txt"])
    resume_text = ""
    if uploaded is not None:
        resume_text = uploaded.getvalue().decode("utf-8", errors="replace")
    resume_text = st.text_area("Resume text", value=resume_text, height=220, placeholder="Paste your current summary, skills and project experience here.")
    jobs = list_jobs()
    if jobs:
        options = {f"#{j['id']} · {j['role']} at {j['company']}": j for j in jobs}
        chosen = st.selectbox("Choose target job", list(options.keys()), key="resume_job")
        job = options[chosen]
        st.text_area("Target job description", value=job["job_description"] or "", height=130, disabled=True)
        if not (job["job_description"] or "").strip():
            st.warning("This job lead has no job description yet. Open Job Leads, edit/add a description, then return here. A meaningful match score cannot be calculated without it.")
        if st.button("Generate tailoring suggestions"):
            if not resume_text.strip():
                st.warning("Paste or upload resume text first.")
            elif not (job["job_description"] or "").strip():
                st.error("Please add the target job description before generating a match report.")
            else:
                tailored = tailor_resume_text(resume_text, job["job_description"], job["role"])
                st.session_state["tailored_resume"] = tailored
                st.session_state["resume_match"] = match_score(resume_text, job["job_description"])
        if "tailored_resume" in st.session_state:
            st.metric("Keyword overlap estimate", f"{st.session_state.get('resume_match', 0)}%")
            st.text_area("Suggested tailored resume text (review before use)", value=st.session_state["tailored_resume"], height=260)
            st.download_button("Download tailored text", st.session_state["tailored_resume"], "tailored_resume.txt", "text/plain")
    else:
        st.info("Add a job lead first to use resume tailoring suggestions.")
    st.caption("This offline version uses transparent keyword matching and editing prompts, not an external generative AI model. An API integration can be added if credentials and time are available.")

with tab_outreach:
    st.subheader("Create and manage outreach drafts")
    jobs = list_jobs()
    if not jobs:
        st.info("Add a job lead first.")
    else:
        job_map = {f"#{j['id']} · {j['role']} at {j['company']}": j for j in jobs}
        selected = st.selectbox("Job lead", list(job_map.keys()), key="outreach_job")
        job = job_map[selected]
        candidate_name = st.text_input("Candidate name", key="candidate_name")
        candidate_email = st.text_input("Candidate email (optional)", key="candidate_email")
        skills = st.text_input("Relevant skills you genuinely have", placeholder="Python, REST APIs, SQL")
        if st.button("Generate email draft", type="primary"):
            subject, body = generate_email_draft(candidate_name, job, skills)
            st.session_state["draft_subject"] = subject
            st.session_state["draft_body"] = body
            st.session_state["draft_job_id"] = job["id"]
            st.session_state["draft_candidate"] = candidate_name
        if "draft_body" in st.session_state:
            subject = st.text_input("Email subject", value=st.session_state["draft_subject"])
            body = st.text_area("Email body — review and edit", value=st.session_state["draft_body"], height=240)
            if st.button("Save outreach draft"):
                add_outreach(st.session_state["draft_job_id"], st.session_state.get("draft_candidate", ""), candidate_email, subject, body)
                st.success("Draft saved. Copy it into your email client after review.")
                st.rerun()
    st.divider()
    st.subheader("Saved outreach")
    out = list_outreach()
    if out:
        st.dataframe(pd.DataFrame(out), use_container_width=True, hide_index=True)
        out_map = {f"#{o['id']} · {o['subject']} [{o['status']}]": o for o in out}
        selected_out = st.selectbox("Select draft to update", list(out_map.keys()))
        status = st.selectbox("Outreach status", ["Draft", "Approved", "Sent", "Replied", "No response", "Follow-up sent"], key="out_status")
        if st.button("Update outreach status"):
            update_outreach_status(out_map[selected_out]["id"], status)
            st.success("Outreach status updated.")
            st.rerun()
    else:
        st.caption("No saved drafts yet.")

with tab_followups:
    st.subheader("Follow-up tracker")
    st.write("Review outreach that has not received a reply. Follow-ups are drafted for human review; this prototype does not send emails.")
    out = list_outreach()
    pending = [o for o in out if o["status"] in ("Sent", "No response", "Follow-up sent")]
    if pending:
        st.dataframe(pd.DataFrame(pending), use_container_width=True, hide_index=True)
        st.info("Suggested practice: follow up after approximately 5–7 business days, unless the recruiter specified otherwise.")
    else:
        st.info("No sent or pending outreach records yet. Mark a draft as Sent to include it here.")
    st.text_area("Follow-up message template", value="Hi, I wanted to follow up on my previous message regarding the role. I remain interested and would be happy to share any additional information. Thank you for your time.", height=120)

with tab_reports:
    st.subheader("Reports and exports")
    jobs = list_jobs()
    out = list_outreach()
    st.write("Download data for review or include it in your project demonstration.")
    st.download_button("Download job leads CSV", build_csv_bytes(jobs), "job_leads.csv", "text/csv")
    st.download_button("Download outreach CSV", build_csv_bytes(out), "outreach.csv", "text/csv")
    st.subheader("Implementation notes")
    st.markdown("""
    - Persistent local SQLite database.
    - Role/job keyword overlap score for transparent matching.
    - Editable outreach drafts and status tracking.
    - Manual review; no automated scraping or bulk email dispatch.
    - CSV reporting for easy evaluation.
    """)
