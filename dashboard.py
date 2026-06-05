"""
RYNZ Dashboard Page – User overview, stats, and personalized recommendations
"""
import streamlit as st
from utils.ui import render_page_header, render_metric_cards
from utils.auth import require_auth
from utils.database import get_dashboard_stats, fetch_jobs
from utils.ai_engine import get_career_suggestions


def render():
    require_auth()
    user = st.session_state.get("user", {})
    name = user.get("full_name", "User")
    first_name = name.split()[0] if name else "User"

    render_page_header("Dashboard", f"Welcome back, {first_name} 👋", "🏠")

    st.markdown('<div class="page-content">', unsafe_allow_html=True)

    # ─── Quick Stats ─────────────────────────────────────────────────────────
    stats = get_dashboard_stats(user.get("id", ""))
    render_metric_cards([
        {"icon": "💼", "value": "200K+", "label": "Jobs Available", "change": "↑ 1.2K today", "change_dir": "up"},
        {"icon": "🎓", "value": "8,400+", "label": "Scholarships", "change": "↑ 12 new", "change_dir": "up"},
        {"icon": "🎯", "value": "6,200+", "label": "Internships", "change": "↑ 85 this week", "change_dir": "up"},
        {"icon": "🔖", "value": str(stats.get("saved_count", 0)), "label": "Saved Items", "change": "", "change_dir": ""},
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Main Grid ───────────────────────────────────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Career Suggestions
        st.markdown("""
        <div style="margin-bottom:20px;">
          <span class="section-tag">AI Recommendations</span>
          <h3 style="font-size:18px;font-weight:700;color:white;margin-top:8px;">Career paths for you</h3>
        </div>
        """, unsafe_allow_html=True)

        suggestions = get_career_suggestions(user)
        for s in suggestions[:3]:
            score = s.get("match_score", 80)
            skills_html = "".join([f'<span class="job-tag">{sk}</span>' for sk in s.get("skills_needed", [])[:3]])
            companies_str = " · ".join(s.get("companies", [])[:3])
            st.markdown(f"""
            <div class="job-card" style="margin-bottom:12px;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                <div>
                  <div class="job-title">{s['title']}</div>
                  <div class="job-company">{s['reason']}</div>
                </div>
                <div style="text-align:right;">
                  <div style="font-size:22px;font-weight:800;background:linear-gradient(135deg,#6366f1,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{score}%</div>
                  <div style="font-size:11px;color:#64748b;">match</div>
                </div>
              </div>
              <div class="job-tags" style="margin-bottom:10px;">{skills_html}</div>
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <span class="job-salary">{s.get('avg_salary','')}</span>
                <span style="font-size:12px;color:#94a3b8;">{companies_str}</span>
              </div>
              <div style="background:rgba(255,255,255,0.05);border-radius:6px;height:4px;margin-top:12px;overflow:hidden;">
                <div style="width:{score}%;height:100%;background:linear-gradient(90deg,#6366f1,#06b6d4);border-radius:6px;"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Recent Jobs
        st.markdown("""
        <div style="margin:24px 0 16px;">
          <span class="section-tag">Latest Jobs</span>
          <h3 style="font-size:18px;font-weight:700;color:white;margin-top:8px;">Hot opportunities</h3>
        </div>
        """, unsafe_allow_html=True)

        jobs = fetch_jobs(limit=4)
        for job in jobs[:4]:
            tags_html = "".join([f'<span class="job-tag">{t}</span>' for t in job.get("skills", [])[:3]])
            remote_badge = '<span class="job-tag job-tag-green">Remote</span>' if job.get("is_remote") else ""
            st.markdown(f"""
            <div class="job-card">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                  <div class="job-title">{job['title']}</div>
                  <div class="job-company">🏢 {job['company']} · {job.get('location','')}</div>
                </div>
                <span class="job-salary">{job.get('salary','')}</span>
              </div>
              <div class="job-tags" style="margin-top:12px;">{tags_html} {remote_badge}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        # Profile Completion
        skills = user.get("skills", [])
        bio = user.get("bio", "")
        completion = 40 + (20 if skills else 0) + (20 if bio else 0) + (10 if user.get("education") else 0) + (10 if user.get("phone") else 0)

        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:24px;margin-bottom:20px;">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
            <div class="t-avatar" style="width:48px;height:48px;font-size:18px;">{name[0].upper()}</div>
            <div>
              <div style="font-weight:700;color:white;font-size:15px;">{name}</div>
              <div style="font-size:12px;color:#64748b;">{user.get('email','')}</div>
            </div>
          </div>
          <div style="font-size:13px;color:#94a3b8;margin-bottom:8px;">Profile completion</div>
          <div style="background:rgba(255,255,255,0.06);border-radius:6px;height:6px;margin-bottom:8px;overflow:hidden;">
            <div style="width:{completion}%;height:100%;background:linear-gradient(90deg,#6366f1,#06b6d4);border-radius:6px;transition:width 0.5s;"></div>
          </div>
          <div style="font-size:12px;color:#64748b;">{completion}% complete</div>
        </div>
        """, unsafe_allow_html=True)

        # Skills
        if skills:
            skills_display = skills if isinstance(skills, list) else skills.split(",")
            skills_html = "".join([f'<span class="job-tag" style="margin:3px;">{s.strip()}</span>' for s in skills_display[:8]])
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:24px;margin-bottom:20px;">
              <div style="font-weight:700;color:white;font-size:15px;margin-bottom:12px;">🛠️ Your Skills</div>
              <div style="display:flex;flex-wrap:wrap;gap:4px;">{skills_html}</div>
            </div>
            """, unsafe_allow_html=True)

        # Quick Actions
        st.markdown("""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:24px;margin-bottom:20px;">
          <div style="font-weight:700;color:white;font-size:15px;margin-bottom:16px;">⚡ Quick Actions</div>
        """, unsafe_allow_html=True)

        actions = [
            ("ai_assistant", "🤖", "Chat with AI"),
            ("resume_analyzer", "📄", "Analyze Resume"),
            ("mock_interview", "🎤", "Mock Interview"),
            ("jobs", "💼", "Browse Jobs"),
        ]
        for page_key, icon, label in actions:
            if st.button(f"{icon} {label}", key=f"qa_{page_key}", use_container_width=True):
                st.query_params["page"] = page_key
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # News preview
        from utils.database import fetch_news
        news = fetch_news("Tech")[:4]
        st.markdown("""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:24px;">
          <div style="font-weight:700;color:white;font-size:15px;margin-bottom:16px;">📰 Tech News</div>
        """, unsafe_allow_html=True)
        for n in news[:3]:
            st.markdown(f"""
            <a href="{n['url']}" target="_blank" class="news-card" style="padding:12px;margin-bottom:8px;">
              <div class="news-title" style="font-size:13px;">{n['title'][:80]}...</div>
              <div class="news-meta"><span class="news-source">{n['source']}</span><span>{n['published']}</span></div>
            </a>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ─── Edit Profile ─────────────────────────────────────────────────────────
    with st.expander("✏️ Edit Profile"):
        with st.form("profile_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_name = st.text_input("Full Name", value=name)
                new_phone = st.text_input("Phone", value=user.get("phone", ""))
                new_education = st.text_input("Education", value=user.get("education", ""))
            with c2:
                new_goals = st.text_area("Career Goals", value=user.get("career_goals", ""), height=100)
                skills_input = ", ".join(skills) if isinstance(skills, list) else (skills or "")
                new_skills = st.text_input("Skills (comma-separated)", value=skills_input)

            new_bio = st.text_area("Bio", value=user.get("bio", ""), height=80)
            if st.form_submit_button("Save Profile", use_container_width=True):
                from utils.auth import update_profile
                skills_list = [s.strip() for s in new_skills.split(",") if s.strip()]
                result = update_profile(user["id"], {
                    "full_name": new_name, "phone": new_phone,
                    "education": new_education, "career_goals": new_goals,
                    "skills": skills_list, "bio": new_bio,
                })
                if result["success"]:
                    st.success("✅ Profile updated!")
                    st.rerun()
                else:
                    st.error(result["error"])

    st.markdown('</div>', unsafe_allow_html=True)
