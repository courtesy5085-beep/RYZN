"""
RYNZ Internships Page
"""
import streamlit as st
from utils.ui import render_page_header, render_empty_state
from utils.auth import require_auth
from utils.database import fetch_internships, save_job_for_user


def render():
    require_auth()
    render_page_header("Internships", "Launch your career with world-class internships", "🎯")
    st.markdown('<div class="page-content">', unsafe_allow_html=True)

    # ─── Filters ─────────────────────────────────────────────────────────────
    col_s, col_r, col_p = st.columns([3, 1, 1])
    with col_s:
        search = st.text_input("", placeholder="🔍 Search internships...", label_visibility="collapsed")
    with col_r:
        remote_only = st.checkbox("🌎 Remote Only")
    with col_p:
        paid_only = st.checkbox("💰 Paid Only")

    # Stats bar
    st.markdown("""
    <div style="display:flex;gap:16px;margin:16px 0;padding:16px 20px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:12px;flex-wrap:wrap;">
      <span style="font-size:13px;color:#94a3b8;">🏢 <strong style="color:white">Top Companies:</strong> Google · Meta · OpenAI · Stripe · Anthropic · DeepMind</span>
    </div>
    """, unsafe_allow_html=True)

    # ─── Fetch & Render ───────────────────────────────────────────────────────
    internships = fetch_internships(search=search)
    if remote_only:
        internships = [i for i in internships if i.get("is_remote")]
    if paid_only:
        internships = [i for i in internships if i.get("is_paid")]

    if not internships:
        render_empty_state("🎯", "No internships found", "Try adjusting your filters.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.markdown(f'<div style="font-size:14px;color:#64748b;margin-bottom:16px;">{len(internships)} internships found</div>', unsafe_allow_html=True)

    for i, intern in enumerate(internships):
        skills_html = "".join([f'<span class="job-tag">{s}</span>' for s in intern.get("skills", [])[:4]])
        remote_badge = '<span class="job-tag job-tag-green">🌎 Remote</span>' if intern.get("is_remote") else '<span class="job-tag job-tag-orange">🏢 On-site</span>'
        paid_badge = '<span class="job-tag" style="background:rgba(34,197,94,0.12);color:#86efac;">💰 Paid</span>' if intern.get("is_paid") else '<span class="job-tag">Unpaid</span>'

        with st.container():
            st.markdown(f"""
            <div class="scholarship-card">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                  <div class="sch-title">{intern['title']}</div>
                  <div class="sch-org">🏢 {intern.get('company','')} · ⏱ {intern.get('duration','')} · 📍 {intern.get('location','')}</div>
                </div>
                <div style="text-align:right;">
                  <div class="sch-amount">{intern.get('stipend','')}</div>
                  <div class="sch-deadline">Deadline: {intern.get('deadline','')}</div>
                </div>
              </div>
              <div class="job-tags" style="margin-top:12px;">{skills_html} {remote_badge} {paid_badge}</div>
            </div>
            """, unsafe_allow_html=True)

            b1, b2, _ = st.columns([1, 1, 2])
            with b1:
                if intern.get("apply_url"):
                    st.markdown(f'<a href="{intern["apply_url"]}" target="_blank" class="btn-primary" style="padding:10px 18px;font-size:13px;display:inline-block;">Apply →</a>', unsafe_allow_html=True)
            with b2:
                if st.button("🔖 Save", key=f"save_int_{i}", use_container_width=True):
                    user = st.session_state.get("user", {})
                    save_job_for_user(user.get("id", ""), {**intern, "item_type": "internship"})
                    st.success("Saved!")

            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
