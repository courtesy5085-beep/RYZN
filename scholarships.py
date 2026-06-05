"""
RYNZ Scholarships Page
"""
import streamlit as st
from utils.ui import render_page_header, render_empty_state
from utils.auth import require_auth
from utils.database import fetch_scholarships, save_job_for_user


def render():
    require_auth()
    render_page_header("Scholarships", "Discover funding opportunities worldwide", "🎓")
    st.markdown('<div class="page-content">', unsafe_allow_html=True)

    # ─── Filters ─────────────────────────────────────────────────────────────
    col_s, col_c, col_d = st.columns([3, 1.5, 1.5])
    with col_s:
        search = st.text_input("", placeholder="🔍 Search scholarships...", label_visibility="collapsed")
    with col_c:
        countries = ["All", "USA", "UK", "Germany", "Canada", "Australia", "China", "Netherlands", "Sweden"]
        country = st.selectbox("Country", countries, label_visibility="collapsed")
    with col_d:
        degrees = ["All", "Bachelors", "Masters", "PhD", "Short Course"]
        degree = st.selectbox("Degree Level", degrees, label_visibility="collapsed")

    # Featured scholarship banner
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(99,102,241,0.15),rgba(6,182,212,0.1));border:1px solid rgba(99,102,241,0.25);border-radius:16px;padding:20px 24px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
      <div>
        <div style="font-size:12px;color:#a5b4fc;font-weight:600;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">⭐ Featured</div>
        <div style="font-size:18px;font-weight:700;color:white;">Fulbright Foreign Student Program 2025</div>
        <div style="font-size:13px;color:#94a3b8;margin-top:4px;">Full funding · USA · All fields · Deadline: Oct 1, 2025</div>
      </div>
      <a href="https://foreign.fulbrightonline.org" target="_blank" class="btn-primary" style="padding:12px 24px;font-size:13px;white-space:nowrap;">Apply Now →</a>
    </div>
    """, unsafe_allow_html=True)

    # ─── Fetch & Render ───────────────────────────────────────────────────────
    scholarships = fetch_scholarships(country=country, degree=degree, search=search)

    if not scholarships:
        render_empty_state("🎓", "No scholarships found", "Try different filter combinations.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.markdown(f'<div style="font-size:14px;color:#64748b;margin-bottom:16px;">{len(scholarships)} scholarships found</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    for i, sch in enumerate(scholarships):
        with (col_a if i % 2 == 0 else col_b):
            field_badge = f'<span class="job-tag job-tag-blue">{sch.get("field","")}</span>' if sch.get("field") else ""
            degree_badge = f'<span class="job-tag">{sch.get("degree_level","")}</span>'
            country_flag = {"USA": "🇺🇸", "UK": "🇬🇧", "Germany": "🇩🇪", "Canada": "🇨🇦", "Australia": "🇦🇺", "China": "🇨🇳"}.get(sch.get("country",""), "🌍")

            st.markdown(f"""
            <div class="scholarship-card">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
                <div style="flex:1;">
                  <div class="sch-title">{sch['title']}</div>
                  <div class="sch-org">{country_flag} {sch.get('organization','')} · {sch.get('country','')}</div>
                </div>
              </div>
              <div style="font-size:13px;color:#94a3b8;line-height:1.6;margin-bottom:12px;">{sch.get('description','')[:120]}...</div>
              <div class="job-tags" style="margin-bottom:12px;">{degree_badge} {field_badge}</div>
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                  <div class="sch-amount">{sch.get('amount','')}</div>
                  <div class="sch-deadline">⏰ Deadline: {sch.get('deadline','')}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            b1, b2 = st.columns(2)
            with b1:
                if sch.get("apply_url"):
                    st.markdown(f'<a href="{sch["apply_url"]}" target="_blank" class="btn-primary" style="padding:10px 16px;font-size:12px;display:block;text-align:center;">Apply →</a>', unsafe_allow_html=True)
            with b2:
                if st.button("🔖 Save", key=f"save_sch_{i}", use_container_width=True):
                    user = st.session_state.get("user", {})
                    save_job_for_user(user.get("id", ""), {**sch, "item_type": "scholarship"})
                    st.success("Saved!")

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
