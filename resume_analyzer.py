"""
RYNZ Resume Analyzer – AI-powered ATS scoring and improvement
"""
import streamlit as st
from utils.ui import render_page_header
from utils.auth import require_auth
from utils.ai_engine import analyze_resume


def extract_text(uploaded_file) -> str:
    """Extract text from PDF or DOCX."""
    file_type = uploaded_file.type

    if file_type == "application/pdf":
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded_file)
            return "\n".join([page.extract_text() or "" for page in reader.pages])
        except ImportError:
            pass
        try:
            import pdfplumber
            with pdfplumber.open(uploaded_file) as pdf:
                return "\n".join([p.extract_text() or "" for p in pdf.pages])
        except Exception:
            return uploaded_file.read().decode("utf-8", errors="ignore")

    elif file_type in ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"):
        try:
            import docx
            from io import BytesIO
            doc = docx.Document(BytesIO(uploaded_file.read()))
            return "\n".join([para.text for para in doc.paragraphs])
        except ImportError:
            return uploaded_file.read().decode("utf-8", errors="ignore")

    return uploaded_file.read().decode("utf-8", errors="ignore")


def render_score_gauge(score: int, label: str = "", size: int = 90):
    color = "#22c55e" if score >= 80 else "#f59e0b" if score >= 60 else "#ef4444"
    st.markdown(f"""
    <div style="text-align:center;padding:12px;">
      <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
        <circle cx="{size//2}" cy="{size//2}" r="{size//2-8}" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="8"/>
        <circle cx="{size//2}" cy="{size//2}" r="{size//2-8}" fill="none" stroke="{color}" stroke-width="8"
          stroke-dasharray="{int(score/100*(2*3.14159*(size//2-8)))} {int(2*3.14159*(size//2-8))}"
          stroke-dashoffset="{int(0.25*2*3.14159*(size//2-8))}"
          stroke-linecap="round"/>
        <text x="50%" y="50%" text-anchor="middle" dy="0.3em" fill="white" font-size="{size//5}px" font-weight="800">{score}</text>
      </svg>
      {f'<div style="font-size:12px;color:#94a3b8;margin-top:4px;">{label}</div>' if label else ''}
    </div>
    """, unsafe_allow_html=True)


def render():
    require_auth()
    render_page_header("Resume Analyzer", "AI-powered ATS scoring, gap analysis & improvement suggestions", "📄")
    st.markdown('<div class="page-content">', unsafe_allow_html=True)

    if "resume_result" not in st.session_state:
        st.session_state.resume_result = None

    col_upload, col_result = st.columns([1, 2])

    with col_upload:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:28px;">
          <div style="font-weight:700;color:white;font-size:16px;margin-bottom:6px;">📤 Upload Resume</div>
          <div style="font-size:13px;color:#64748b;margin-bottom:20px;">Supports PDF and DOCX formats</div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Upload",
            type=["pdf", "docx", "doc"],
            label_visibility="collapsed",
            key="resume_upload"
        )

        target_role = st.text_input(
            "Target Role (optional)",
            placeholder="e.g. Senior Software Engineer",
            key="target_role_input"
        )

        if uploaded:
            file_size = len(uploaded.getvalue()) / 1024
            st.markdown(f"""
            <div style="background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.2);border-radius:10px;padding:12px;margin-bottom:12px;">
              <div style="font-size:13px;font-weight:600;color:#86efac;">✅ {uploaded.name}</div>
              <div style="font-size:12px;color:#64748b;">{file_size:.1f} KB · {uploaded.type.split('/')[-1].upper()}</div>
            </div>
            """, unsafe_allow_html=True)

        analyze_btn = st.button("🔍 Analyze with AI", use_container_width=True, key="analyze_btn")

        if analyze_btn:
            if not uploaded:
                st.error("Please upload your resume first.")
            else:
                with st.spinner("🤖 AI is analyzing your resume..."):
                    resume_text = extract_text(uploaded)
                    if not resume_text.strip():
                        st.error("Could not extract text from the file. Please ensure it's readable.")
                    else:
                        result = analyze_resume(resume_text, target_role=target_role)
                        st.session_state.resume_result = result
                        st.rerun()

        # Tips
        st.markdown("""
        <div style="margin-top:20px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.06);">
          <div style="font-size:13px;font-weight:600;color:white;margin-bottom:12px;">💡 ATS Tips</div>
          <div style="font-size:12px;color:#64748b;line-height:1.8;">
            ✓ Use standard section headings<br>
            ✓ Match keywords from job description<br>
            ✓ Avoid tables and complex formatting<br>
            ✓ Use standard fonts (Arial, Calibri)<br>
            ✓ Quantify all achievements<br>
            ✓ Include contact info at the top
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_result:
        result = st.session_state.resume_result

        if not result:
            st.markdown("""
            <div style="background:rgba(255,255,255,0.03);border:1px dashed rgba(255,255,255,0.1);border-radius:20px;padding:80px 40px;text-align:center;height:100%;">
              <div style="font-size:48px;margin-bottom:16px;">📄</div>
              <div style="font-size:18px;font-weight:700;color:white;margin-bottom:8px;">Upload your resume to begin</div>
              <div style="font-size:14px;color:#64748b;">Our AI will analyze your resume for ATS compatibility,<br>identify weaknesses, and suggest specific improvements.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            ats_score = result.get("ats_score", 0)
            grade = result.get("overall_grade", "B")
            grade_color = {"A+": "#22c55e", "A": "#22c55e", "B+": "#86efac", "B": "#f59e0b", "C+": "#f59e0b", "C": "#ef4444", "D": "#ef4444"}.get(grade, "#f59e0b")

            # Score overview
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:28px;margin-bottom:20px;">
              <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:20px;">
                <div>
                  <div style="font-size:14px;color:#64748b;margin-bottom:4px;">ATS Score</div>
                  <div style="font-size:52px;font-weight:800;background:linear-gradient(135deg,#6366f1,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{ats_score}</div>
                  <div style="font-size:13px;color:#64748b;">out of 100</div>
                </div>
                <div style="text-align:center;">
                  <div style="font-size:14px;color:#64748b;margin-bottom:4px;">Grade</div>
                  <div style="font-size:42px;font-weight:800;color:{grade_color};">{grade}</div>
                </div>
                <div style="flex:1;min-width:200px;">
                  <div style="font-size:13px;color:#94a3b8;line-height:1.7;">{result.get('summary','')}</div>
                </div>
              </div>
              <div style="margin-top:16px;background:rgba(255,255,255,0.04);border-radius:8px;height:8px;overflow:hidden;">
                <div style="width:{ats_score}%;height:100%;background:linear-gradient(90deg,#6366f1,#06b6d4);border-radius:8px;transition:width 1s;"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Sub-scores
            format_s = result.get("format_score", 0)
            content_s = result.get("content_score", 0)
            impact_s = result.get("impact_score", 0)
            c1, c2, c3 = st.columns(3)
            with c1:
                render_score_gauge(format_s, "Format", 80)
            with c2:
                render_score_gauge(content_s, "Content", 80)
            with c3:
                render_score_gauge(impact_s, "Impact", 80)

            # Strengths & Weaknesses
            col_str, col_weak = st.columns(2)
            with col_str:
                strengths = result.get("strengths", [])
                items_html = "".join([f'<div style="display:flex;gap:8px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04);">'
                                      f'<span style="color:#22c55e;font-weight:700;">✓</span>'
                                      f'<span style="font-size:13px;color:#94a3b8;">{s}</span></div>' for s in strengths])
                st.markdown(f"""
                <div style="background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.15);border-radius:16px;padding:20px;">
                  <div style="font-weight:700;color:white;margin-bottom:12px;">✅ Strengths</div>
                  {items_html}
                </div>""", unsafe_allow_html=True)

            with col_weak:
                weaknesses = result.get("weaknesses", [])
                items_html = "".join([f'<div style="display:flex;gap:8px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04);">'
                                      f'<span style="color:#ef4444;font-weight:700;">✗</span>'
                                      f'<span style="font-size:13px;color:#94a3b8;">{w}</span></div>' for w in weaknesses])
                st.markdown(f"""
                <div style="background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.15);border-radius:16px;padding:20px;">
                  <div style="font-weight:700;color:white;margin-bottom:12px;">⚠️ Weaknesses</div>
                  {items_html}
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Improvements
            improvements = result.get("improvements", [])
            if improvements:
                improvements_html = "".join([
                    f'<div style="display:flex;gap:12px;padding:12px;background:rgba(255,255,255,0.03);border-radius:10px;margin-bottom:8px;">'
                    f'<span style="background:linear-gradient(135deg,#6366f1,#8b5cf6);color:white;width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;min-width:24px;">{j+1}</span>'
                    f'<span style="font-size:13px;color:#94a3b8;line-height:1.6;">{imp}</span></div>'
                    for j, imp in enumerate(improvements)])
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;margin-bottom:16px;">
                  <div style="font-weight:700;color:white;margin-bottom:12px;">💡 AI Recommendations</div>
                  {improvements_html}
                </div>""", unsafe_allow_html=True)

            # Missing skills & keywords
            col_miss, col_kw = st.columns(2)
            with col_miss:
                missing = result.get("missing_skills", [])
                if missing:
                    tags = "".join([f'<span class="job-tag" style="margin:3px;">{s}</span>' for s in missing])
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;">
                      <div style="font-weight:700;color:white;margin-bottom:12px;">📚 Skills to Add</div>
                      <div style="display:flex;flex-wrap:wrap;">{tags}</div>
                    </div>""", unsafe_allow_html=True)
            with col_kw:
                keywords = result.get("keyword_suggestions", [])
                if keywords:
                    tags = "".join([f'<span class="job-tag job-tag-blue" style="margin:3px;">{k}</span>' for k in keywords])
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;">
                      <div style="font-weight:700;color:white;margin-bottom:12px;">🔑 ATS Keywords</div>
                      <div style="display:flex;flex-wrap:wrap;">{tags}</div>
                    </div>""", unsafe_allow_html=True)

            if st.button("🔄 Analyze Another Resume", use_container_width=True):
                st.session_state.resume_result = None
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
