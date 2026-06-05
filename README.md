# ⚡ RYNZ – AI-Powered Career Ecosystem

<div align="center">

![RYNZ Banner](https://img.shields.io/badge/RYNZ-AI%20Career%20Ecosystem-6366f1?style=for-the-badge&logo=lightning&logoColor=white)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rynz.streamlit.app)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**The world's most advanced AI-powered career ecosystem**  
Land your dream job with GPT-4o career guidance, real-time opportunities, ATS resume analysis, mock interviews, and personalized roadmaps.

</div>

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Career Assistant** | GPT-4o powered career coach for guidance, resume help, and interview prep |
| 💼 **Real-Time Jobs** | 200K+ live job listings with smart search & filters |
| 🎯 **Internships** | Company-wise, remote & paid internship listings |
| 🎓 **Scholarships** | Global scholarships filtered by country, degree, and field |
| 📄 **Resume Analyzer** | AI-powered ATS scoring, gap analysis & improvement tips |
| 🗺️ **Career Roadmaps** | Personalized step-by-step career transition plans |
| 🎤 **Mock Interviews** | AI-generated questions with scoring & detailed feedback |
| 📰 **News Feed** | Tech, AI, Business & Startup news aggregation |
| 📊 **Admin Dashboard** | Analytics, user management & platform metrics |
| 🔐 **Auth System** | Supabase Auth with email verification & session persistence |

---

## 📁 Project Structure

```
RYNZ/
├── app.py                    # Main app + landing page router
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
│
├── pages/
│   ├── dashboard.py          # User dashboard + profile
│   ├── jobs.py               # Job board
│   ├── internships.py        # Internship listings
│   ├── scholarships.py       # Scholarship search
│   ├── ai_assistant.py       # GPT-4o chat interface
│   ├── resume_analyzer.py    # AI resume analysis
│   ├── news.py               # News aggregation
│   ├── mock_interview.py     # Mock interview system
│   └── admin.py              # Admin analytics
│
├── utils/
│   ├── auth.py               # Supabase authentication
│   ├── database.py           # DB queries + mock data
│   ├── ai_engine.py          # GPT-4o integrations
│   └── ui.py                 # Global CSS + UI components
│
├── database/
│   └── schema.sql            # Complete Supabase schema + RLS
│
└── .streamlit/
    └── config.toml           # Streamlit theme configuration
```

---

## ⚡ Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/your-username/rynz.git
cd rynz
pip install -r requirements.txt
```

### 2. Set Up Supabase

1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Go to **SQL Editor** and run `database/schema.sql`
4. Copy your Project URL, Anon Key, and Service Key from **Settings → API**

### 3. Configure Secrets

Create `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
OPENAI_API_KEY = "sk-proj-..."
```

### 4. Run

```bash
streamlit run app.py
```

🎉 Open [http://localhost:8501](http://localhost:8501) in your browser!

---

## ☁️ Deploy to Streamlit Cloud

1. Push code to GitHub (don't include `.streamlit/secrets.toml`)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Connect your GitHub repo → set **Main file** to `app.py`
4. Click **Advanced settings** → add your 4 secrets
5. Click **Deploy** 🚀

---

## 🔒 Security Architecture

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Authentication | Supabase Auth | JWT-based secure login/signup |
| Database | Supabase PostgreSQL | Row-Level Security (RLS) policies |
| API Keys | Streamlit Secrets | Server-side only, never exposed to client |
| Input Validation | Python validators | SQL injection prevention |
| Session | Streamlit Session State | Secure client-side session management |

### Row Level Security Policies
- **Profiles**: Users can only read/write their own profile
- **Saved Items**: Users can only access their own saved items
- **Chat History**: Users can only view their own messages
- **Jobs/Scholarships**: Public read access (no auth required)

---

## 🗄️ Database Schema

### Core Tables
| Table | Purpose |
|-------|---------|
| `profiles` | User profiles extending Supabase auth |
| `jobs` | Job listings |
| `internships` | Internship opportunities |
| `scholarships` | Scholarship database |
| `saved_items` | User's saved jobs/scholarships/internships |
| `chat_history` | AI assistant conversation history |
| `resume_analyses` | Resume analysis results |
| `mock_interviews` | Interview session results |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend/Backend** | Python + Streamlit |
| **AI Engine** | OpenAI GPT-4o |
| **Database** | Supabase (PostgreSQL) |
| **Authentication** | Supabase Auth |
| **Charts** | Plotly |
| **PDF Processing** | PyPDF2 + pdfplumber |
| **Word Processing** | python-docx |
| **Styling** | Custom CSS (injected) |
| **Deployment** | Streamlit Cloud |

---

## 🎨 Design System

- **Colors**: Deep space dark (`#020408`) with electric indigo (`#6366f1`) and cyan (`#06b6d4`) accents
- **Typography**: Inter (body) + Space Grotesk (headings)
- **Style**: Glassmorphism cards, gradient buttons, neon glow effects
- **Inspiration**: Apple, Linear, OpenAI, Stripe, Vercel

---

## 📊 Admin Access

To enable admin access:
1. After signup, go to Supabase → Table Editor → profiles
2. Find your user record and set `role` to `admin`
3. The **Admin** nav item will appear in your sidebar

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

MIT License – see [LICENSE](LICENSE) for details.

---

<div align="center">
  <strong>Built with ❤️ by the RYNZ Team</strong><br>
  <em>Empowering 50,000+ professionals to land their dream careers</em>
</div>
