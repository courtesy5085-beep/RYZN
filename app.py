"""
RYNZ - AI-Powered Career Ecosystem Platform
Main application entry point with landing page
"""

import streamlit as st
import time
from utils.ui import inject_global_css, render_navbar, render_footer
from utils.auth import init_session, is_authenticated, logout_user
from utils.database import init_supabase

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="RYNZ – AI Career Ecosystem",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "https://github.com/rynz-ai",
        "About": "RYNZ – AI-Powered Career Ecosystem Platform"
    }
)

# ─── Initialize Session & Global CSS ──────────────────────────────────────────
inject_global_css()
init_session()

# ─── Landing Page ─────────────────────────────────────────────────────────────

def render_hero():
    st.markdown("""
    <div class="hero-section">
      <div class="hero-badge">✦ Powered by GPT-4o &nbsp;|&nbsp; Trusted by 50,000+ professionals</div>
      <h1 class="hero-title">
        Your AI Career<br>
        <span class="gradient-text">Ecosystem</span>
      </h1>
      <p class="hero-subtitle">
        Land your dream job with AI-powered career guidance, real-time opportunities,<br>
        resume analysis, mock interviews, and personalized roadmaps — all in one place.
      </p>
      <div class="hero-cta-group">
        <a href="?page=signup" class="btn-primary">Get Started Free →</a>
        <a href="?page=login" class="btn-secondary">Sign In</a>
      </div>
      <div class="hero-stats">
        <div class="stat-item"><span class="stat-num">50K+</span><span class="stat-label">Users</span></div>
        <div class="stat-divider"></div>
        <div class="stat-item"><span class="stat-num">200K+</span><span class="stat-label">Jobs Listed</span></div>
        <div class="stat-divider"></div>
        <div class="stat-item"><span class="stat-num">98%</span><span class="stat-label">Satisfaction</span></div>
        <div class="stat-divider"></div>
        <div class="stat-item"><span class="stat-num">4.9★</span><span class="stat-label">Rating</span></div>
      </div>
      <div class="hero-glow"></div>
    </div>
    """, unsafe_allow_html=True)


def render_features():
    st.markdown('<div class="section-header"><span class="section-tag">Core Features</span><h2 class="section-title">Everything you need to<br><span class="gradient-text">accelerate your career</span></h2></div>', unsafe_allow_html=True)

    features = [
        {"icon": "🤖", "title": "AI Career Assistant", "desc": "Chat with our GPT-4o powered assistant for instant career guidance, interview prep, and personalized advice.", "tag": "AI-Powered", "wide": True},
        {"icon": "💼", "title": "Real-Time Jobs", "desc": "Browse 200K+ live job postings with smart filters, one-click apply, and saved searches.", "tag": "Live Data"},
        {"icon": "🎓", "title": "Scholarships", "desc": "Discover thousands of scholarships filtered by country, degree level, and field of study.", "tag": "Education"},
        {"icon": "📄", "title": "Resume Analyzer", "desc": "Upload your resume for instant ATS score, gap analysis, and AI-powered improvement suggestions.", "tag": "AI Analysis", "wide": True},
        {"icon": "🗺️", "title": "AI Roadmap Generator", "desc": "Get a personalized learning roadmap to reach your dream career in the shortest time possible.", "tag": "Personalized"},
        {"icon": "🎤", "title": "Mock Interviews", "desc": "Practice with AI-generated interview questions, get scored, and receive detailed feedback.", "tag": "Practice"},
    ]

    st.markdown('<div class="bento-grid">', unsafe_allow_html=True)
    for f in features:
        wide_class = "bento-wide" if f.get("wide") else ""
        st.markdown(f"""
        <div class="bento-card {wide_class}">
          <div class="bento-icon">{f['icon']}</div>
          <span class="bento-tag">{f['tag']}</span>
          <h3 class="bento-title">{f['title']}</h3>
          <p class="bento-desc">{f['desc']}</p>
          <div class="bento-arrow">→</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_ai_preview():
    st.markdown("""
    <div class="ai-preview-section">
      <div class="section-header">
        <span class="section-tag">AI Assistant</span>
        <h2 class="section-title">Your personal career<br><span class="gradient-text">co-pilot</span></h2>
      </div>
      <div class="chat-preview">
        <div class="chat-header">
          <div class="chat-avatar">⚡</div>
          <div class="chat-info">
            <span class="chat-name">RYNZ AI</span>
            <span class="chat-status">● Online</span>
          </div>
        </div>
        <div class="chat-messages">
          <div class="chat-msg assistant">
            <div class="msg-bubble">Hi! I'm RYNZ AI. I can help you with career guidance, resume review, interview prep, and more. What would you like to work on today?</div>
          </div>
          <div class="chat-msg user">
            <div class="msg-bubble">I want to transition from backend to ML engineering. Where do I start?</div>
          </div>
          <div class="chat-msg assistant">
            <div class="msg-bubble">Great choice! Given your backend experience, here's your personalized roadmap:<br><br>
            <strong>Phase 1 (Month 1-2):</strong> Python for ML, NumPy, Pandas<br>
            <strong>Phase 2 (Month 3-4):</strong> Scikit-learn, ML fundamentals<br>
            <strong>Phase 3 (Month 5-6):</strong> Deep Learning with PyTorch<br>
            <strong>Phase 4 (Month 7+):</strong> MLOps, production deployments<br><br>
            Want me to generate your full interactive roadmap? 🚀</div>
          </div>
          <div class="chat-typing">
            <span></span><span></span><span></span>
          </div>
        </div>
        <div class="chat-input-preview">
          <input type="text" placeholder="Ask RYNZ AI anything about your career..." disabled/>
          <button class="chat-send">↑</button>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_testimonials():
    testimonials = [
        {"name": "Sarah Chen", "role": "Software Engineer @ Google", "avatar": "SC", "text": "RYNZ's AI mock interview helped me crack Google's technical rounds. The personalized feedback was incredible!", "rating": "★★★★★"},
        {"name": "Marcus Johnson", "role": "Data Scientist @ Meta", "avatar": "MJ", "text": "The roadmap generator gave me a clear path from analyst to data scientist. Landed Meta in 6 months!", "rating": "★★★★★"},
        {"name": "Priya Sharma", "role": "ML Engineer @ OpenAI", "avatar": "PS", "text": "Resume analyzer boosted my ATS score from 42 to 91. Got 3x more callbacks. Absolutely game-changing.", "rating": "★★★★★"},
        {"name": "Alex Rivera", "role": "Product Manager @ Stripe", "avatar": "AR", "text": "Found my scholarship through RYNZ, got the PM role through their job board. One platform changed everything.", "rating": "★★★★★"},
    ]
    st.markdown('<div class="section-header"><span class="section-tag">Testimonials</span><h2 class="section-title">Loved by <span class="gradient-text">50,000+ professionals</span></h2></div>', unsafe_allow_html=True)
    st.markdown('<div class="testimonials-grid">', unsafe_allow_html=True)
    for t in testimonials:
        st.markdown(f"""
        <div class="testimonial-card">
          <div class="t-rating">{t['rating']}</div>
          <p class="t-text">"{t['text']}"</p>
          <div class="t-author">
            <div class="t-avatar">{t['avatar']}</div>
            <div class="t-info">
              <span class="t-name">{t['name']}</span>
              <span class="t-role">{t['role']}</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_pricing():
    st.markdown('<div class="section-header"><span class="section-tag">Pricing</span><h2 class="section-title">Simple, transparent<br><span class="gradient-text">pricing</span></h2></div>', unsafe_allow_html=True)

    plans = [
        {
            "name": "Free", "price": "$0", "period": "/month", "badge": "",
            "features": ["AI Career Assistant (10 msgs/day)", "Job Board Access", "Basic Resume Tips", "Scholarship Search", "Community Access"],
            "cta": "Get Started Free", "highlight": False
        },
        {
            "name": "Pro", "price": "$19", "period": "/month", "badge": "Most Popular",
            "features": ["Unlimited AI Career Assistant", "Resume Analyzer + ATS Score", "AI Mock Interviews (20/month)", "Personalized Roadmaps", "Priority Job Alerts", "Internship Access", "Advanced Analytics"],
            "cta": "Start Pro Trial", "highlight": True
        },
        {
            "name": "Enterprise", "price": "$99", "period": "/month", "badge": "",
            "features": ["Everything in Pro", "Unlimited Mock Interviews", "Custom AI Persona", "Team Dashboard", "API Access", "Dedicated Success Manager", "White-label Option"],
            "cta": "Contact Sales", "highlight": False
        },
    ]
    st.markdown('<div class="pricing-grid">', unsafe_allow_html=True)
    for p in plans:
        highlight_class = "pricing-card-highlight" if p["highlight"] else "pricing-card"
        badge_html = f'<span class="pricing-badge">{p["badge"]}</span>' if p["badge"] else ""
        features_html = "".join([f'<li class="pricing-feature"><span class="pf-check">✓</span>{f}</li>' for f in p["features"]])
        st.markdown(f"""
        <div class="{highlight_class}">
          {badge_html}
          <div class="pricing-name">{p['name']}</div>
          <div class="pricing-price">{p['price']}<span class="pricing-period">{p['period']}</span></div>
          <ul class="pricing-features">{features_html}</ul>
          <a href="?page=signup" class="{'btn-primary' if p['highlight'] else 'btn-outline'}">{p['cta']}</a>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_auth_forms():
    """Render login/signup forms based on URL params"""
    params = st.query_params
    page = params.get("page", "")

    if page == "login":
        render_login_modal()
    elif page == "signup":
        render_signup_modal()


def render_login_modal():
    st.markdown('<div class="auth-overlay">', unsafe_allow_html=True)
    st.markdown('<div class="auth-modal">', unsafe_allow_html=True)
    st.markdown('<div class="auth-header"><span class="auth-logo">⚡ RYNZ</span><h2>Welcome back</h2><p>Sign in to your career ecosystem</p></div>', unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        col1, col2 = st.columns(2)
        with col1:
            remember = st.checkbox("Remember me")
        submitted = st.form_submit_button("Sign In →", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                from utils.auth import login_user
                result = login_user(email, password)
                if result["success"]:
                    st.success("Welcome back! Redirecting...")
                    st.query_params.clear()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(result["error"])

    st.markdown("""
    <div class="auth-footer">
      <p>Don't have an account? <a href="?page=signup">Sign up free</a></p>
      <p><a href="?page=forgot">Forgot password?</a></p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_signup_modal():
    st.markdown('<div class="auth-overlay">', unsafe_allow_html=True)
    st.markdown('<div class="auth-modal">', unsafe_allow_html=True)
    st.markdown('<div class="auth-header"><span class="auth-logo">⚡ RYNZ</span><h2>Create your account</h2><p>Join 50,000+ professionals accelerating their careers</p></div>', unsafe_allow_html=True)

    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", placeholder="John")
        with col2:
            last_name = st.text_input("Last Name", placeholder="Doe")
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="Min. 8 characters")
        password2 = st.text_input("Confirm Password", type="password", placeholder="••••••••")
        agree = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        submitted = st.form_submit_button("Create Account →", use_container_width=True)

        if submitted:
            if not all([first_name, last_name, email, password, password2]):
                st.error("Please fill in all fields.")
            elif password != password2:
                st.error("Passwords do not match.")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters.")
            elif not agree:
                st.error("Please agree to the Terms of Service.")
            else:
                from utils.auth import signup_user
                result = signup_user(email, password, first_name, last_name)
                if result["success"]:
                    st.success("✅ Account created! Please check your email to verify.")
                    time.sleep(2)
                    st.query_params["page"] = "login"
                    st.rerun()
                else:
                    st.error(result["error"])

    st.markdown('<div class="auth-footer"><p>Already have an account? <a href="?page=login">Sign in</a></p></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_forgot_modal():
    st.markdown('<div class="auth-overlay">', unsafe_allow_html=True)
    st.markdown('<div class="auth-modal">', unsafe_allow_html=True)
    st.markdown('<div class="auth-header"><span class="auth-logo">⚡ RYNZ</span><h2>Reset Password</h2><p>We\'ll send a reset link to your email</p></div>', unsafe_allow_html=True)

    with st.form("forgot_form"):
        email = st.text_input("Email", placeholder="you@example.com")
        submitted = st.form_submit_button("Send Reset Link →", use_container_width=True)
        if submitted and email:
            from utils.auth import reset_password
            result = reset_password(email)
            if result["success"]:
                st.success("Reset link sent! Check your inbox.")
            else:
                st.error(result["error"])

    st.markdown('<div class="auth-footer"><p><a href="?page=login">← Back to Sign In</a></p></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


# ─── App Router ───────────────────────────────────────────────────────────────

def main():
    params = st.query_params
    page = params.get("page", "home")

    # Auth pages handled inline
    if page in ["login", "signup", "forgot"]:
        render_navbar(authenticated=False)
        if page == "login":
            render_login_modal()
        elif page == "signup":
            render_signup_modal()
        elif page == "forgot":
            render_forgot_modal()
        render_footer()
        return

    # Handle logout
    if page == "logout":
        logout_user()
        st.query_params.clear()
        st.rerun()

    # Authenticated inner pages
    if is_authenticated():
        inner_page = page if page else "dashboard"

        # Build sidebar nav
        render_navbar(authenticated=True)
        with st.sidebar:
            st.markdown('<div class="sidebar-logo">⚡ RYNZ</div>', unsafe_allow_html=True)
            user = st.session_state.get("user", {})
            st.markdown(f'<div class="sidebar-user"><div class="sidebar-avatar">{user.get("full_name","U")[0].upper()}</div><div><p class="sidebar-name">{user.get("full_name","User")}</p><p class="sidebar-email">{user.get("email","")}</p></div></div>', unsafe_allow_html=True)
            st.markdown("---")
            nav_items = [
                ("dashboard", "🏠", "Dashboard"),
                ("jobs", "💼", "Jobs"),
                ("internships", "🎯", "Internships"),
                ("scholarships", "🎓", "Scholarships"),
                ("ai_assistant", "🤖", "AI Assistant"),
                ("resume_analyzer", "📄", "Resume Analyzer"),
                ("news", "📰", "News"),
                ("mock_interview", "🎤", "Mock Interview"),
            ]
            if user.get("role") == "admin":
                nav_items.append(("admin", "⚙️", "Admin"))

            for nav_page, icon, label in nav_items:
                active = "nav-active" if inner_page == nav_page else ""
                if st.button(f"{icon}  {label}", key=f"nav_{nav_page}", use_container_width=True):
                    st.query_params["page"] = nav_page
                    st.rerun()

            st.markdown("---")
            if st.button("🚪  Sign Out", use_container_width=True, key="signout_btn"):
                logout_user()
                st.query_params.clear()
                st.rerun()

        # Route to pages
        if inner_page == "dashboard":
            from pages.dashboard import render
            render()
        elif inner_page == "jobs":
            from pages.jobs import render
            render()
        elif inner_page == "internships":
            from pages.internships import render
            render()
        elif inner_page == "scholarships":
            from pages.scholarships import render
            render()
        elif inner_page == "ai_assistant":
            from pages.ai_assistant import render
            render()
        elif inner_page == "resume_analyzer":
            from pages.resume_analyzer import render
            render()
        elif inner_page == "news":
            from pages.news import render
            render()
        elif inner_page == "mock_interview":
            from pages.mock_interview import render
            render()
        elif inner_page == "admin":
            from pages.admin import render
            render()
        else:
            from pages.dashboard import render
            render()
    else:
        # Public landing page
        render_navbar(authenticated=False)
        render_hero()
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        render_features()
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        render_ai_preview()
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        render_testimonials()
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        render_pricing()
        render_footer()


if __name__ == "__main__":
    main()
