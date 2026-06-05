"""
RYNZ Jobs Page – Real-time job board with search and filters
"""
import streamlit as st
from utils.ui import render_page_header, render_empty_state
from utils.auth import require_auth
from utils.database import fetch_jobs, save_job_for_user


def render():
    require_auth()
    render_page_header("Jobs", "Discover 200K+ opportunities matched to your skills", "💼")
    st.markdown('<div class="page-content">', unsafe_allow_html=True)

    # ─── Search & Filters ────────────────────────────────────────────────────
    col_search, col_type, col_loc = st.columns([3, 1.5, 1.5])
    with col_search:
        search = st.text_input("", placeholder="🔍 Search job title, company, or skill...", label_visibility="collapsed")
    with col_type:
        job_type = st.selectbox("Type", ["All", "Full-time", "Part-time", "Contract", "Freelance"], label_visibility="collapsed")
    with col_loc:
        location = st.text_input("", placeholder="📍 Location or 'Remote'", label_visibility="collapsed")

    # Filter chips
    st.markdown("""
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0;">
      <span class="job-tag job-tag-blue" style="cursor:pointer;">🔥 Trending</span>
      <span class="job-tag job-tag-green" style="cursor:pointer;">🌎 Remote</span>
      <span class="job-tag" style="cursor:pointer;">💰 $150K+</span>
      <span class="job-tag" style="cursor:pointer;">🤖 AI/ML</span>
      <span class="job-tag" style="cursor:pointer;">🔒 Security</span>
      <span class="job-tag" style="cursor:pointer;">📱 Mobile</span>
      <span class="job-tag" style="cursor:pointer;">☁️ Cloud</span>
    </div>
    """, unsafe_allow_html=True)

    # ─── Fetch Jobs ───────────────────────────────────────────────────────────
    with st.spinner(""):
        jobs = fetch_jobs(search=search, job_type=job_type, location=location)

    if not jobs:
        render_empty_state("💼", "No jobs found", "Try adjusting your search filters.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Results count
    st.markdown(f'<div style="font-size:14px;color:#64748b;margin-bottom:16px;">Showing <strong style="color:white">{len(jobs)}</strong> opportunities</div>', unsafe_allow_html=True)

    # ─── Job Listings ─────────────────────────────────────────────────────────
    col_list, col_detail = st.columns([2, 1])

    with col_list:
        for i, job in enumerate(jobs):
            with st.container():
                tags_html = "".join([f'<span class="job-tag">{t}</span>' for t in job.get("skills", [])[:4]])
                remote_badge = '<span class="job-tag job-tag-green">🌎 Remote</span>' if job.get("is_remote") else '<span class="job-tag job-tag-orange">🏢 On-site</span>'
                created = job.get("created_at", "")[:10] if job.get("created_at") else ""

                st.markdown(f"""
                <div class="job-card" id="job-{i}">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
                    <div>
                      <div class="job-title">{job['title']}</div>
                      <div class="job-company">🏢 {job.get('company','')} &nbsp;·&nbsp; 📍 {job.get('location','')}</div>
                    </div>
                    <div style="text-align:right;">
                      <div class="job-salary">{job.get('salary','Competitive')}</div>
                      <div class="job-time">{created}</div>
                    </div>
                  </div>
                  <div class="job-tags">{tags_html} {remote_badge}</div>
                  <div style="font-size:13px;color:#475569;margin-top:10px;line-height:1.5;">{job.get('description','')[:120]}...</div>
                </div>
                """, unsafe_allow_html=True)

                btn_col1, btn_col2, btn_col3 = st.columns([2, 1, 1])
                with btn_col1:
                    if job.get("apply_url"):
                        st.markdown(f'<a href="{job["apply_url"]}" target="_blank" class="btn-primary" style="padding:10px 20px;font-size:13px;text-decoration:none;display:inline-block;">Apply Now →</a>', unsafe_allow_html=True)
                with btn_col2:
                    if st.button("🔖 Save", key=f"save_job_{i}_{job.get('id','')}", use_container_width=True):
                        user = st.session_state.get("user", {})
                        result = save_job_for_user(user.get("id", ""), job)
                        if result["success"]:
                            st.success("Saved!")
                        else:
                            st.info("Saved locally!")
                with btn_col3:
                    if st.button("👁 Details", key=f"view_job_{i}_{job.get('id','')}", use_container_width=True):
                        st.session_state["selected_job"] = job

                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # ─── Job Detail Panel ────────────────────────────────────────────────────
    with col_detail:
        selected = st.session_state.get("selected_job")
        if selected:
            st.markdown(f"""
            <div style="position:sticky;top:80px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:28px;">
              <div style="font-size:20px;font-weight:700;color:white;margin-bottom:6px;">{selected['title']}</div>
              <div style="font-size:14px;color:#94a3b8;margin-bottom:16px;">🏢 {selected.get('company','')} · 📍 {selected.get('location','')}</div>
              <div style="display:flex;gap:10px;margin-bottom:20px;flex-wrap:wrap;">
                <span class="job-salary">{selected.get('salary','Competitive')}</span>
                {'<span class="job-tag job-tag-green">Remote</span>' if selected.get('is_remote') else ''}
                <span class="job-tag">{selected.get('job_type','Full-time')}</span>
              </div>
              <div style="font-size:14px;color:#94a3b8;line-height:1.7;margin-bottom:20px;">{selected.get('description','')}</div>
              <div style="margin-bottom:20px;">
                <div style="font-size:13px;font-weight:600;color:white;margin-bottom:8px;">Required Skills</div>
                <div style="display:flex;flex-wrap:wrap;gap:6px;">
                  {"".join([f'<span class=\"job-tag\">{s}</span>' for s in selected.get('skills',[])])}
                </div>
              </div>
              {'<a href="' + selected['apply_url'] + '" target="_blank" class="btn-primary" style="display:block;text-align:center;padding:14px;">Apply Now →</a>' if selected.get('apply_url') else ''}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(255,255,255,0.03);border:1px dashed rgba(255,255,255,0.1);border-radius:20px;padding:40px;text-align:center;">
              <div style="font-size:36px;margin-bottom:12px;">👈</div>
              <div style="font-size:14px;color:#64748b;">Click "Details" on any job to see full information here</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
