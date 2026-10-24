import re
from collections import Counter

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "you", "your", "are", "our", "will",
    "have", "has", "was", "were", "into", "their", "they", "role", "job", "work", "team", "years",
    "experience", "ability", "strong", "using", "use", "not", "all", "any", "can", "who", "what",
    "about", "required", "preferred", "skills", "skill", "responsibilities", "requirements", "theirs",
    "which", "when", "where", "while", "such", "including", "include", "across", "within", "must",
    "should", "would", "could", "will", "etc", "per", "one", "two", "new", "good", "best", "workings",
    "developer", "development", "working", "building", "build", "support", "help", "looking", "candidate",
}

# Normalize common technology spellings so equivalent resume/job wording can match.
ALIASES = {
    "reactjs": "react", "react.js": "react", "nodejs": "node", "node.js": "node",
    "expressjs": "express", "express.js": "express", "nextjs": "next", "next.js": "next",
    "scikitlearn": "scikit-learn", "sklearn": "scikit-learn", "restful": "rest-api",
    "rest-apis": "rest-api", "apis": "api", "apis": "api", "javascript": "javascript",
    "typescript": "typescript", "c++": "cpp", "cplusplus": "cpp", "postgres": "postgresql",
    "mongo": "mongodb", "machine-learning": "machine-learning", "ml": "machine-learning",
    "artificial-intelligence": "artificial-intelligence", "ai": "artificial-intelligence",
}

TECH_TERMS = {
    "python", "java", "javascript", "typescript", "cpp", "c", "sql", "mysql", "postgresql", "mongodb",
    "tidb", "react", "node", "express", "flask", "django", "fastapi", "streamlit", "html", "css",
    "tailwind", "rest-api", "api", "jwt", "git", "github", "docker", "kubernetes", "aws", "azure",
    "gcp", "linux", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "machine-learning",
    "artificial-intelligence", "nlp", "llm", "prompt-engineering", "data-analysis", "data-structures",
    "algorithms", "oop", "dbms", "testing", "pytest", "postman", "vercel", "render", "railway",
    "communication", "leadership", "agile", "scrum", "rest", "api-design", "authentication", "authorization",
}

def tokenize(text):
    text = (text or "").lower()
    # Capture known multiword concepts before splitting punctuation.
    text = text.replace("object-oriented programming", " oop ")
    text = text.replace("data structures and algorithms", " data-structures algorithms ")
    text = text.replace("machine learning", " machine-learning ")
    text = text.replace("artificial intelligence", " artificial-intelligence ")
    text = text.replace("rest apis", " rest-api ").replace("rest api", " rest-api ")
    raw = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{1,}", text)
    normalized = []
    for word in raw:
        word = word.strip(".-")
        word = ALIASES.get(word, word)
        if word not in STOPWORDS and len(word) > 2:
            normalized.append(word)
    return normalized

def _terms(text):
    tokens = tokenize(text)
    # Prefer meaningful technical/role skills; if none are detected, use remaining content words.
    technical = {token for token in tokens if token in TECH_TERMS}
    return technical if technical else set(tokens)

def match_score(resume_text, job_description):
    jd = _terms(job_description)
    resume = _terms(resume_text)
    if not jd:
        return 0
    return round(100 * len(jd & resume) / len(jd))

def matching_keywords(resume_text, job_description, limit=12):
    jd_tokens = tokenize(job_description)
    resume_tokens = set(tokenize(resume_text))
    # Preserve frequency/order from the job description but report only unique terms.
    jd_counts = Counter(word for word in jd_tokens if word in TECH_TERMS)
    if not jd_counts:
        jd_counts = Counter(word for word in jd_tokens if word not in STOPWORDS)
    common, missing = [], []
    for word, _ in jd_counts.most_common():
        if word in resume_tokens:
            common.append(word)
        else:
            missing.append(word)
    return {"matched": common[:limit], "potential_gaps": missing[:limit]}
