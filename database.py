"""
RYNZ Database – Supabase client initialization and data helpers
"""
import streamlit as st
from functools import lru_cache
import os

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False


def _get_secrets():
    """Get Supabase credentials from Streamlit secrets or env vars."""
    try:
        url = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", ""))
        anon = st.secrets.get("SUPABASE_ANON_KEY", os.getenv("SUPABASE_ANON_KEY", ""))
        service = st.secrets.get("SUPABASE_SERVICE_KEY", os.getenv("SUPABASE_SERVICE_KEY", ""))
        return url, anon, service
    except Exception:
        return (
            os.getenv("SUPABASE_URL", ""),
            os.getenv("SUPABASE_ANON_KEY", ""),
            os.getenv("SUPABASE_SERVICE_KEY", ""),
        )


def init_supabase():
    """Initialize Supabase connection check."""
    url, anon, _ = _get_secrets()
    if not url or not anon:
        st.warning("⚠️ Supabase not configured. Add SUPABASE_URL and SUPABASE_ANON_KEY to secrets.")


@st.cache_resource
def get_supabase_client():
    """Return cached Supabase anon client."""
    if not SUPABASE_AVAILABLE:
        raise RuntimeError("supabase package not installed.")
    url, anon, _ = _get_secrets()
    if not url or not anon:
        raise RuntimeError("Supabase URL/Key not configured.")
    return create_client(url, anon)


@st.cache_resource
def get_service_client():
    """Return cached Supabase service role client."""
    if not SUPABASE_AVAILABLE:
        raise RuntimeError("supabase package not installed.")
    url, _, service = _get_secrets()
    if not url or not service:
        # Fallback to anon
        return get_supabase_client()
    return create_client(url, service)


# ─── JOBS ─────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def fetch_jobs(search: str = "", job_type: str = "All", location: str = "", limit: int = 50):
    """Fetch jobs from DB with filters."""
    try:
        db = get_service_client()
        query = db.table("jobs").select("*").eq("is_active", True)
        if search:
            query = query.ilike("title", f"%{search}%")
        if job_type != "All":
            query = query.eq("job_type", job_type)
        if location:
            query = query.ilike("location", f"%{location}%")
        result = query.order("created_at", desc=True).limit(limit).execute()
        return result.data or []
    except Exception:
        return _mock_jobs(search, job_type)


def _mock_jobs(search="", job_type="All"):
    jobs = [
        {"id": 1, "title": "Senior Software Engineer", "company": "Google", "location": "Mountain View, CA", "job_type": "Full-time", "salary": "$180K - $250K", "skills": ["Python", "Go", "Kubernetes"], "description": "Build next-gen infrastructure at Google.", "apply_url": "https://careers.google.com", "created_at": "2025-06-01", "is_remote": True},
        {"id": 2, "title": "ML Engineer", "company": "OpenAI", "location": "San Francisco, CA", "job_type": "Full-time", "salary": "$200K - $300K", "skills": ["PyTorch", "Python", "CUDA"], "description": "Work on frontier AI models.", "apply_url": "https://openai.com/careers", "created_at": "2025-06-02", "is_remote": False},
        {"id": 3, "title": "Product Manager", "company": "Stripe", "location": "Remote", "job_type": "Full-time", "salary": "$160K - $220K", "skills": ["Product Strategy", "Analytics", "SQL"], "description": "Drive Stripe's payments products.", "apply_url": "https://stripe.com/jobs", "created_at": "2025-06-03", "is_remote": True},
        {"id": 4, "title": "Frontend Engineer", "company": "Vercel", "location": "Remote", "job_type": "Full-time", "salary": "$140K - $190K", "skills": ["React", "TypeScript", "Next.js"], "description": "Build the fastest web deployment platform.", "apply_url": "https://vercel.com/careers", "created_at": "2025-06-03", "is_remote": True},
        {"id": 5, "title": "Data Scientist", "company": "Netflix", "location": "Los Gatos, CA", "job_type": "Full-time", "salary": "$170K - $240K", "skills": ["Python", "R", "Spark", "ML"], "description": "Personalization & recommendation systems.", "apply_url": "https://jobs.netflix.com", "created_at": "2025-06-04", "is_remote": False},
        {"id": 6, "title": "DevOps Engineer", "company": "GitHub", "location": "Remote", "job_type": "Full-time", "salary": "$130K - $180K", "skills": ["Kubernetes", "Terraform", "AWS"], "description": "Scale developer infrastructure worldwide.", "apply_url": "https://github.com/about/careers", "created_at": "2025-06-04", "is_remote": True},
        {"id": 7, "title": "Backend Engineer", "company": "Notion", "location": "San Francisco, CA", "job_type": "Full-time", "salary": "$150K - $210K", "skills": ["Node.js", "PostgreSQL", "Redis"], "description": "Build the future of productivity software.", "apply_url": "https://notion.so/careers", "created_at": "2025-06-05", "is_remote": True},
        {"id": 8, "title": "Security Engineer", "company": "Cloudflare", "location": "Austin, TX", "job_type": "Full-time", "salary": "$155K - $220K", "skills": ["Rust", "Networking", "PKI"], "description": "Protect the internet at scale.", "apply_url": "https://cloudflare.com/careers", "created_at": "2025-06-05", "is_remote": False},
    ]
    if search:
        jobs = [j for j in jobs if search.lower() in j["title"].lower() or search.lower() in j["company"].lower()]
    if job_type != "All":
        jobs = [j for j in jobs if j["job_type"] == job_type]
    return jobs


# ─── INTERNSHIPS ──────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def fetch_internships(search: str = "", limit: int = 50):
    try:
        db = get_service_client()
        query = db.table("internships").select("*").eq("is_active", True)
        if search:
            query = query.ilike("title", f"%{search}%")
        result = query.order("created_at", desc=True).limit(limit).execute()
        return result.data or []
    except Exception:
        return _mock_internships(search)


def _mock_internships(search=""):
    internships = [
        {"id": 1, "title": "Software Engineering Intern", "company": "Google", "location": "Mountain View, CA", "duration": "12 weeks", "stipend": "$8,500/month", "skills": ["Python", "Java", "Algorithms"], "deadline": "2025-08-01", "apply_url": "https://careers.google.com", "is_remote": False, "is_paid": True},
        {"id": 2, "title": "Data Science Intern", "company": "Meta", "location": "Menlo Park, CA", "duration": "12 weeks", "stipend": "$9,000/month", "skills": ["Python", "SQL", "ML"], "deadline": "2025-07-15", "apply_url": "https://metacareers.com", "is_remote": False, "is_paid": True},
        {"id": 3, "title": "AI Research Intern", "company": "DeepMind", "location": "London, UK", "duration": "6 months", "stipend": "£6,000/month", "skills": ["PyTorch", "Research", "ML Theory"], "deadline": "2025-09-01", "apply_url": "https://deepmind.com/careers", "is_remote": False, "is_paid": True},
        {"id": 4, "title": "Product Design Intern", "company": "Figma", "location": "Remote", "duration": "16 weeks", "stipend": "$7,000/month", "skills": ["Figma", "UX Research", "Prototyping"], "deadline": "2025-07-20", "apply_url": "https://figma.com/careers", "is_remote": True, "is_paid": True},
        {"id": 5, "title": "Backend Engineering Intern", "company": "Stripe", "location": "San Francisco, CA", "duration": "12 weeks", "stipend": "$8,000/month", "skills": ["Ruby", "Go", "APIs"], "deadline": "2025-08-10", "apply_url": "https://stripe.com/jobs", "is_remote": False, "is_paid": True},
        {"id": 6, "title": "ML Infra Intern", "company": "Anthropic", "location": "San Francisco, CA", "duration": "12 weeks", "stipend": "$9,500/month", "skills": ["Python", "MLOps", "Cloud"], "deadline": "2025-07-30", "apply_url": "https://anthropic.com/careers", "is_remote": True, "is_paid": True},
    ]
    if search:
        internships = [i for i in internships if search.lower() in i["title"].lower() or search.lower() in i["company"].lower()]
    return internships


# ─── SCHOLARSHIPS ─────────────────────────────────────────────────────────────

@st.cache_data(ttl=600)
def fetch_scholarships(country: str = "All", degree: str = "All", search: str = ""):
    try:
        db = get_service_client()
        query = db.table("scholarships").select("*").eq("is_active", True)
        if country != "All":
            query = query.eq("country", country)
        if degree != "All":
            query = query.eq("degree_level", degree)
        if search:
            query = query.ilike("title", f"%{search}%")
        result = query.order("deadline").limit(50).execute()
        return result.data or []
    except Exception:
        return _mock_scholarships(country, degree, search)


def _mock_scholarships(country="All", degree="All", search=""):
    scholarships = [
        {"id": 1, "title": "Fulbright Foreign Student Program", "organization": "US State Department", "amount": "Full Funding", "country": "USA", "degree_level": "Masters/PhD", "deadline": "2025-10-01", "description": "Fully funded graduate studies in the USA.", "apply_url": "https://foreign.fulbrightonline.org", "field": "All Fields"},
        {"id": 2, "title": "Chevening Scholarship", "organization": "UK Government", "amount": "Full Funding", "country": "UK", "degree_level": "Masters", "deadline": "2025-11-05", "description": "UK government's global scholarship programme.", "apply_url": "https://chevening.org", "field": "All Fields"},
        {"id": 3, "title": "Google PhD Fellowship", "organization": "Google", "amount": "$50,000/year", "country": "USA", "degree_level": "PhD", "deadline": "2025-08-01", "description": "Support for outstanding PhD students in CS.", "apply_url": "https://research.google/outreach/phd-fellowship/", "field": "Computer Science"},
        {"id": 4, "title": "DAAD Scholarship", "organization": "German Academic Exchange", "amount": "€934/month", "country": "Germany", "degree_level": "Masters/PhD", "deadline": "2025-10-15", "description": "Study in Germany with living stipend.", "apply_url": "https://daad.de", "field": "All Fields"},
        {"id": 5, "title": "Gates Cambridge Scholarship", "organization": "Gates Foundation", "amount": "Full Funding", "country": "UK", "degree_level": "Masters/PhD", "deadline": "2025-12-03", "description": "Pursue a postgraduate degree at Cambridge.", "apply_url": "https://gatescambridge.org", "field": "All Fields"},
        {"id": 6, "title": "Schwarzman Scholars", "organization": "Schwarzman College", "amount": "Full Funding", "country": "China", "degree_level": "Masters", "deadline": "2025-09-12", "description": "1-year Master's at Tsinghua University.", "apply_url": "https://schwarzmanscholars.org", "field": "Leadership"},
        {"id": 7, "title": "AAUW Fellowships", "organization": "AAUW", "amount": "$20,000", "country": "USA", "degree_level": "PhD", "deadline": "2025-11-01", "description": "For women pursuing full-time PhD studies.", "apply_url": "https://aauw.org/resources/programs/fellowships-grants/", "field": "All Fields"},
        {"id": 8, "title": "Commonwealth Scholarship", "organization": "Commonwealth Foundation", "amount": "Full Funding", "country": "UK", "degree_level": "Masters/PhD", "deadline": "2025-12-01", "description": "For students from low-to-middle income Commonwealth countries.", "apply_url": "https://cscuk.fcdo.gov.uk", "field": "Development"},
    ]
    if country != "All":
        scholarships = [s for s in scholarships if s["country"] == country]
    if degree != "All":
        scholarships = [s for s in scholarships if degree in s["degree_level"]]
    if search:
        scholarships = [s for s in scholarships if search.lower() in s["title"].lower()]
    return scholarships


# ─── NEWS ─────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=180)
def fetch_news(category: str = "Tech"):
    """Fetch news – live via RSS or fallback mock data."""
    try:
        import requests
        feeds = {
            "Tech": "https://feeds.feedburner.com/TechCrunch",
            "AI": "https://www.artificialintelligence-news.com/feed/",
            "Business": "https://feeds.bloomberg.com/technology/news.rss",
            "Startups": "https://news.ycombinator.com/rss",
        }
        url = feeds.get(category, feeds["Tech"])
        resp = requests.get(url, timeout=5, headers={"User-Agent": "RYNZ/1.0"})
        if resp.status_code == 200:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(resp.content)
            items = []
            for item in root.findall(".//item")[:15]:
                title = item.findtext("title", "").strip()
                link = item.findtext("link", "").strip()
                pub_date = item.findtext("pubDate", "").strip()[:16]
                if title and link:
                    items.append({"title": title, "url": link, "source": category, "published": pub_date})
            if items:
                return items
    except Exception:
        pass
    return _mock_news(category)


def _mock_news(category="Tech"):
    mock = {
        "Tech": [
            {"title": "Apple Unveils M4 Ultra Chip with 512GB Unified Memory", "url": "#", "source": "TechCrunch", "published": "2025-06-05"},
            {"title": "GitHub Copilot Now Supports Full Codebase Reasoning", "url": "#", "source": "GitHub Blog", "published": "2025-06-05"},
            {"title": "Cloudflare Launches AI Gateway with Built-in Rate Limiting", "url": "#", "source": "Cloudflare Blog", "published": "2025-06-04"},
            {"title": "Rust Overtakes Python in Systems Programming Adoption Survey", "url": "#", "source": "The Register", "published": "2025-06-04"},
            {"title": "WebGPU Lands in All Major Browsers – What It Means for Developers", "url": "#", "source": "web.dev", "published": "2025-06-03"},
        ],
        "AI": [
            {"title": "GPT-5 Achieves PhD-Level Reasoning on MMLU Benchmark", "url": "#", "source": "OpenAI", "published": "2025-06-05"},
            {"title": "Google DeepMind AlphaFold 3 Predicts All Molecular Interactions", "url": "#", "source": "Nature", "published": "2025-06-05"},
            {"title": "Anthropic Claude 4 Sets New Record on Coding Benchmarks", "url": "#", "source": "Anthropic", "published": "2025-06-04"},
            {"title": "Mistral Releases 7B Model Beating GPT-4 on Reasoning Tasks", "url": "#", "source": "Mistral AI", "published": "2025-06-03"},
            {"title": "EU AI Act Full Compliance Deadline Approaches – Here's What Changes", "url": "#", "source": "VentureBeat", "published": "2025-06-03"},
        ],
        "Business": [
            {"title": "NVIDIA Market Cap Surpasses $4 Trillion in Historic Milestone", "url": "#", "source": "Bloomberg", "published": "2025-06-05"},
            {"title": "Stripe Processes $1 Trillion in Annual Payment Volume", "url": "#", "source": "Forbes", "published": "2025-06-04"},
            {"title": "Y Combinator W25 Batch: 40% Are AI-Native Startups", "url": "#", "source": "TechCrunch", "published": "2025-06-04"},
            {"title": "Andreessen Horowitz Raises $7.2B AI-Focused Fund", "url": "#", "source": "WSJ", "published": "2025-06-03"},
        ],
        "Startups": [
            {"title": "Perplexity AI Raises $500M at $9B Valuation", "url": "#", "source": "Reuters", "published": "2025-06-05"},
            {"title": "ElevenLabs Hits $1B ARR with Voice AI Platform", "url": "#", "source": "TechCrunch", "published": "2025-06-04"},
            {"title": "Cursor Editor Raises $105M Series B for AI Coding", "url": "#", "source": "Forbes", "published": "2025-06-03"},
            {"title": "Linear Reaches $100M ARR – The Anti-JIRA Movement Grows", "url": "#", "source": "The Information", "published": "2025-06-02"},
        ],
    }
    return mock.get(category, mock["Tech"])


# ─── USER DATA ────────────────────────────────────────────────────────────────

def save_job_for_user(user_id: str, job_data: dict) -> dict:
    try:
        db = get_service_client()
        db.table("saved_items").upsert({
            "user_id": user_id,
            "item_type": "job",
            "item_id": str(job_data.get("id", "")),
            "item_data": job_data,
        }).execute()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_saved_items(user_id: str, item_type: str = "job") -> list:
    try:
        db = get_service_client()
        result = db.table("saved_items").select("*").eq("user_id", user_id).eq("item_type", item_type).execute()
        return [row["item_data"] for row in (result.data or [])]
    except Exception:
        return []


def save_chat_message(user_id: str, role: str, content: str):
    try:
        db = get_service_client()
        db.table("chat_history").insert({"user_id": user_id, "role": role, "content": content}).execute()
    except Exception:
        pass


def get_dashboard_stats(user_id: str) -> dict:
    try:
        db = get_service_client()
        saved = db.table("saved_items").select("id", count="exact").eq("user_id", user_id).execute()
        chats = db.table("chat_history").select("id", count="exact").eq("user_id", user_id).execute()
        return {
            "saved_count": saved.count or 0,
            "chat_count": chats.count or 0,
        }
    except Exception:
        return {"saved_count": 0, "chat_count": 0}


# ─── ADMIN ────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=60)
def get_admin_stats() -> dict:
    try:
        db = get_service_client()
        users = db.table("profiles").select("id", count="exact").execute()
        jobs = db.table("jobs").select("id", count="exact").execute()
        chats = db.table("chat_history").select("id", count="exact").execute()
        saved = db.table("saved_items").select("id", count="exact").execute()
        return {
            "total_users": users.count or 0,
            "total_jobs": jobs.count or 0,
            "total_chats": chats.count or 0,
            "total_saved": saved.count or 0,
        }
    except Exception:
        return {"total_users": 1240, "total_jobs": 8420, "total_chats": 45670, "total_saved": 12300}


@st.cache_data(ttl=60)
def get_recent_users(limit: int = 10) -> list:
    try:
        db = get_service_client()
        result = db.table("profiles").select("full_name,email,role,created_at").order("created_at", desc=True).limit(limit).execute()
        return result.data or []
    except Exception:
        return [
            {"full_name": "Alice Johnson", "email": "alice@example.com", "role": "user", "created_at": "2025-06-05"},
            {"full_name": "Bob Smith", "email": "bob@example.com", "role": "user", "created_at": "2025-06-04"},
            {"full_name": "Carol White", "email": "carol@example.com", "role": "pro", "created_at": "2025-06-04"},
            {"full_name": "Dan Lee", "email": "dan@example.com", "role": "user", "created_at": "2025-06-03"},
            {"full_name": "Eva Martinez", "email": "eva@example.com", "role": "user", "created_at": "2025-06-03"},
        ]
