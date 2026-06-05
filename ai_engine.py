"""
RYNZ AI Engine – GPT-4o powered career intelligence
"""
import streamlit as st
import os
import json
import re

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def _get_openai_client():
    """Initialize OpenAI client from Streamlit secrets or env."""
    try:
        api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))
    except Exception:
        api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OpenAI API key not configured. Add OPENAI_API_KEY to Streamlit secrets.")
    if not OPENAI_AVAILABLE:
        raise RuntimeError("openai package not installed.")
    return OpenAI(api_key=api_key)


SYSTEM_PROMPT = """You are RYNZ AI, an elite career coach and AI career ecosystem assistant built by RYNZ.

Your expertise covers:
- Career transitions, planning, and roadmaps
- Resume writing and ATS optimization
- Interview preparation (behavioral & technical)
- Skill gap analysis and learning recommendations
- Salary negotiation strategies
- Job search tactics and networking
- Industry trends and market intelligence
- Scholarship and internship guidance

Communication style:
- Be concise, actionable, and encouraging
- Use bullet points and structured formatting
- Provide specific, data-driven advice
- Tailor advice to the user's career stage and goals
- Include relevant examples and resources when helpful

Always maintain a professional yet friendly and motivating tone. You are the world's best career advisor."""


def chat_with_ai(messages: list, user_context: dict = None) -> str:
    """Send conversation to GPT-4o and return response."""
    try:
        client = _get_openai_client()
        system_content = SYSTEM_PROMPT
        if user_context:
            name = user_context.get("full_name", "")
            skills = user_context.get("skills", [])
            goals = user_context.get("career_goals", "")
            if name or skills or goals:
                system_content += f"\n\nUser context: Name: {name}, Skills: {', '.join(skills) if isinstance(skills, list) else skills}, Career goals: {goals}"

        formatted_messages = [{"role": "system", "content": system_content}]
        for msg in messages[-20:]:  # Keep last 20 messages for context
            formatted_messages.append({"role": msg["role"], "content": msg["content"]})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=formatted_messages,
            max_tokens=1500,
            temperature=0.75,
        )
        return response.choices[0].message.content
    except Exception as e:
        return _fallback_response(messages[-1]["content"] if messages else "")


def analyze_resume(resume_text: str, target_role: str = "") -> dict:
    """Analyze resume and return structured ATS feedback."""
    try:
        client = _get_openai_client()
        prompt = f"""Analyze this resume{f' for the role of {target_role}' if target_role else ''} and provide a detailed ATS assessment.

Resume:
{resume_text[:4000]}

Return a JSON object with exactly this structure:
{{
  "ats_score": <number 0-100>,
  "overall_grade": "<A+|A|B+|B|C+|C|D>",
  "strengths": ["<strength1>", "<strength2>", "<strength3>"],
  "weaknesses": ["<weakness1>", "<weakness2>", "<weakness3>"],
  "missing_skills": ["<skill1>", "<skill2>", "<skill3>"],
  "improvements": ["<specific action 1>", "<specific action 2>", "<specific action 3>", "<specific action 4>"],
  "keyword_suggestions": ["<keyword1>", "<keyword2>", "<keyword3>", "<keyword4>", "<keyword5>"],
  "format_score": <number 0-100>,
  "content_score": <number 0-100>,
  "impact_score": <number 0-100>,
  "summary": "<2-3 sentence overall assessment>"
}}"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1200,
            temperature=0.3,
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return _mock_resume_analysis()


def generate_roadmap(current_role: str, target_role: str, skills: list, timeline: str = "6 months") -> dict:
    """Generate personalized career roadmap."""
    try:
        client = _get_openai_client()
        current_skills = ", ".join(skills) if skills else "not specified"
        prompt = f"""Create a detailed career transition roadmap from {current_role} to {target_role} 
in {timeline}. Current skills: {current_skills}.

Return a JSON object:
{{
  "title": "Career Roadmap: {current_role} → {target_role}",
  "timeline": "{timeline}",
  "phases": [
    {{
      "phase": 1,
      "title": "<phase title>",
      "duration": "<e.g. Month 1-2>",
      "focus": "<main focus>",
      "tasks": ["<task1>", "<task2>", "<task3>"],
      "resources": ["<resource1>", "<resource2>"],
      "milestone": "<key achievement>"
    }}
  ],
  "skills_to_learn": ["<skill1>", "<skill2>", "<skill3>", "<skill4>", "<skill5>"],
  "key_certifications": ["<cert1>", "<cert2>"],
  "job_titles_progression": ["<title1>", "<title2>", "<title3>"],
  "salary_range": "<expected salary range at destination>",
  "success_tips": ["<tip1>", "<tip2>", "<tip3>"]
}}

Include 3-4 phases. Be specific and actionable."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.5,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        return _mock_roadmap(current_role, target_role)


def generate_mock_interview_questions(role: str, difficulty: str = "Medium", count: int = 10) -> list:
    """Generate mock interview questions for a role."""
    try:
        client = _get_openai_client()
        prompt = f"""Generate {count} {difficulty}-level interview questions for a {role} position.

Return a JSON array:
[
  {{
    "id": 1,
    "type": "<Behavioral|Technical|Situational|System Design>",
    "question": "<the interview question>",
    "difficulty": "{difficulty}",
    "category": "<e.g. Problem Solving|Communication|Technical Skills|Leadership>",
    "tips": "<brief tip on how to answer this question>"
  }}
]

Mix behavioral, technical, and situational questions. Make them realistic and challenging."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.6,
            response_format={"type": "json_object"},
        )
        data = json.loads(response.choices[0].message.content)
        # Handle both {"questions": [...]} and direct array
        if isinstance(data, list):
            return data
        return data.get("questions", data.get("items", []))
    except Exception:
        return _mock_interview_questions(role)


def evaluate_interview_answer(question: str, answer: str, role: str) -> dict:
    """Evaluate a mock interview answer."""
    try:
        client = _get_openai_client()
        prompt = f"""Evaluate this interview answer for a {role} position.

Question: {question}
Answer: {answer}

Return JSON:
{{
  "score": <0-100>,
  "grade": "<A|B|C|D|F>",
  "strengths": ["<strength1>", "<strength2>"],
  "improvements": ["<improvement1>", "<improvement2>"],
  "ideal_elements": ["<what a perfect answer includes>"],
  "feedback": "<2-3 sentence detailed feedback>",
  "follow_up": "<a follow-up question the interviewer might ask>"
}}"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.4,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {"score": 72, "grade": "B", "strengths": ["Clear structure", "Relevant example"], "improvements": ["Add metrics", "More specific impact"], "ideal_elements": ["STAR format", "Quantifiable results"], "feedback": "Good answer with room for improvement. Add specific metrics to strengthen impact.", "follow_up": "Can you elaborate on the specific outcome?"}


def get_career_suggestions(user_profile: dict) -> list:
    """Get personalized career recommendations based on profile."""
    try:
        client = _get_openai_client()
        skills = user_profile.get("skills", [])
        education = user_profile.get("education", "")
        goals = user_profile.get("career_goals", "")

        prompt = f"""Based on this profile, suggest 5 career paths:
Skills: {', '.join(skills) if isinstance(skills, list) else skills}
Education: {education}
Goals: {goals}

Return JSON array:
[
  {{
    "title": "<job title>",
    "match_score": <70-99>,
    "reason": "<why it's a match>",
    "avg_salary": "<salary range>",
    "growth": "<growth rate e.g. 25% YoY>",
    "skills_needed": ["<skill1>", "<skill2>"],
    "companies": ["<company1>", "<company2>", "<company3>"]
  }}
]"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.5,
            response_format={"type": "json_object"},
        )
        data = json.loads(response.choices[0].message.content)
        if isinstance(data, list):
            return data
        return data.get("careers", data.get("suggestions", []))
    except Exception:
        return _mock_career_suggestions()


# ─── FALLBACK / MOCK DATA ─────────────────────────────────────────────────────

def _fallback_response(user_message: str) -> str:
    user_lower = user_message.lower()
    if any(w in user_lower for w in ["resume", "cv"]):
        return "📄 **Resume Tips**\n\n1. **Quantify everything** – Use metrics (increased sales by 35%, reduced load time by 2s)\n2. **ATS keywords** – Mirror exact language from job descriptions\n3. **One page for <5 years** – Keep it concise and scannable\n4. **Action verbs** – Start bullets with Led, Built, Designed, Reduced\n5. **Tailor per application** – Customize your resume for each role\n\nWant me to analyze your specific resume?"
    if any(w in user_lower for w in ["interview", "preparation", "prepare"]):
        return "🎤 **Interview Preparation Guide**\n\n**Before the interview:**\n- Research the company deeply (products, culture, recent news)\n- Practice STAR method for behavioral questions\n- Prepare 5 questions to ask the interviewer\n\n**Common questions to prep:**\n1. Tell me about yourself\n2. Why this company/role?\n3. Greatest achievement?\n4. Biggest weakness?\n5. Where do you see yourself in 5 years?\n\nWant me to run a mock interview for a specific role?"
    if any(w in user_lower for w in ["salary", "negotiate", "pay"]):
        return "💰 **Salary Negotiation Strategy**\n\n1. **Research market rates** – Use Levels.fyi, Glassdoor, LinkedIn Salary\n2. **Delay the conversation** – Let them make the first offer\n3. **Anchor high** – Ask for 15-20% above your target\n4. **Negotiate the total package** – Equity, bonuses, PTO, remote work\n5. **Get it in writing** – Always confirm offers via email\n\n**Magic phrase:** *\"I'm very excited about this role. Based on my research and experience, I was expecting something in the range of $X-$Y. Is there flexibility there?\"*"
    return "👋 Hi! I'm **RYNZ AI**, your personal career coach.\n\nI can help you with:\n- 📄 Resume review & ATS optimization\n- 🎤 Interview preparation & mock interviews\n- 🗺️ Career roadmap generation\n- 💼 Job search strategies\n- 💰 Salary negotiation\n- 🎓 Skill development recommendations\n\nWhat would you like to work on today?"


def _mock_resume_analysis():
    return {
        "ats_score": 72,
        "overall_grade": "B+",
        "strengths": ["Strong technical skills section", "Relevant work experience", "Clear education background"],
        "weaknesses": ["Missing quantifiable achievements", "Generic objective statement", "No LinkedIn/GitHub links"],
        "missing_skills": ["Docker/Kubernetes", "CI/CD pipelines", "Cloud certifications"],
        "improvements": [
            "Add metrics to each bullet (e.g., 'Increased performance by 40%')",
            "Replace objective with a professional summary",
            "Add links to portfolio, GitHub, and LinkedIn",
            "Tailor keywords to match job descriptions",
        ],
        "keyword_suggestions": ["agile", "microservices", "REST APIs", "CI/CD", "cloud infrastructure"],
        "format_score": 78,
        "content_score": 68,
        "impact_score": 65,
        "summary": "Your resume has a solid foundation with good technical skills coverage. The main areas for improvement are quantifying your achievements with specific metrics and tailoring keywords to match ATS requirements for your target roles.",
    }


def _mock_roadmap(current: str, target: str):
    return {
        "title": f"Career Roadmap: {current} → {target}",
        "timeline": "6 months",
        "phases": [
            {"phase": 1, "title": "Foundation & Assessment", "duration": "Month 1-2", "focus": "Core skills and gaps", "tasks": ["Complete skills assessment", "Identify top 5 skill gaps", "Join 2 online communities"], "resources": ["Coursera", "freeCodeCamp"], "milestone": "Clear development plan"},
            {"phase": 2, "title": "Skill Building", "duration": "Month 3-4", "focus": "Hands-on projects", "tasks": ["Build 2 portfolio projects", "Complete relevant certification", "Contribute to open source"], "resources": ["GitHub", "Udemy"], "milestone": "Portfolio with 2+ projects"},
            {"phase": 3, "title": "Job Search", "duration": "Month 5-6", "focus": "Applications & networking", "tasks": ["Optimize LinkedIn", "Apply to 5 companies/week", "Network with professionals"], "resources": ["LinkedIn", "RYNZ Jobs Board"], "milestone": "2+ interview invitations"},
        ],
        "skills_to_learn": ["Python", "Machine Learning", "Cloud Platforms", "Data Analysis", "SQL"],
        "key_certifications": ["AWS Solutions Architect", "Google Cloud Professional"],
        "job_titles_progression": [f"Junior {target}", target, f"Senior {target}"],
        "salary_range": "$90K - $160K",
        "success_tips": ["Network consistently", "Build in public on LinkedIn", "Track applications in a spreadsheet"],
    }


def _mock_interview_questions(role: str):
    return [
        {"id": 1, "type": "Behavioral", "question": f"Tell me about yourself and why you want to be a {role}.", "difficulty": "Easy", "category": "Communication", "tips": "Use the Present-Past-Future framework."},
        {"id": 2, "type": "Behavioral", "question": "Describe a time you faced a major technical challenge. How did you solve it?", "difficulty": "Medium", "category": "Problem Solving", "tips": "Use STAR: Situation, Task, Action, Result."},
        {"id": 3, "type": "Technical", "question": "What is the difference between a stack and a queue? When would you use each?", "difficulty": "Medium", "category": "Technical Skills", "tips": "Give real-world examples for each."},
        {"id": 4, "type": "Situational", "question": "Your team disagrees on the technical approach for a critical feature. How do you proceed?", "difficulty": "Medium", "category": "Leadership", "tips": "Show collaborative decision-making skills."},
        {"id": 5, "type": "Technical", "question": "How would you design a URL shortener like bit.ly? Walk me through the system design.", "difficulty": "Hard", "category": "System Design", "tips": "Cover: requirements, API, DB schema, scaling."},
    ]


def _mock_career_suggestions():
    return [
        {"title": "ML Engineer", "match_score": 94, "reason": "Your programming background aligns perfectly with ML pipelines.", "avg_salary": "$160K - $220K", "growth": "32% YoY", "skills_needed": ["PyTorch", "MLOps"], "companies": ["OpenAI", "Google", "Meta"]},
        {"title": "Data Scientist", "match_score": 88, "reason": "Strong analytical skills match data science requirements.", "avg_salary": "$130K - $190K", "growth": "28% YoY", "skills_needed": ["Statistics", "Spark"], "companies": ["Netflix", "Airbnb", "Stripe"]},
        {"title": "Backend Engineer", "match_score": 85, "reason": "Server-side architecture experience is highly relevant.", "avg_salary": "$140K - $200K", "growth": "22% YoY", "skills_needed": ["Distributed Systems", "Go"], "companies": ["GitHub", "Notion", "Linear"]},
    ]
