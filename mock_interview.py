"""
RYNZ Mock Interview – AI-powered interview practice with scoring
"""
import streamlit as st
from utils.ui import render_page_header
from utils.auth import require_auth
from utils.ai_engine import generate_mock_interview_questions, evaluate_interview_answer


def render():
    require_auth()
    render_page_header("Mock Interview", "Practice with AI-generated questions and get instant scoring", "🎤")
    st.markdown('<div class="page-content">', unsafe_allow_html=True)

    # Init session
    for key, default in [
        ("interview_questions", []),
        ("interview_answers", {}),
        ("interview_scores", {}),
        ("interview_active", False),
        ("interview_question_idx", 0),
        ("interview_complete", False),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    # ─── Setup Screen ─────────────────────────────────────────────────────────
    if not st.session_state.interview_active and not st.session_state.interview_complete:
        col_setup, col_info = st.columns([1, 1])

        with col_setup:
            st.markdown("""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:32px;">
              <div style="font-weight:700;color:white;font-size:18px;margin-bottom:20px;">⚙️ Configure Your Interview</div>
            """, unsafe_allow_html=True)

            with st.form("interview_setup"):
                role = st.text_input("Job Role", placeholder="e.g. Software Engineer, Data Scientist, PM...")
                difficulty = st.select_slider("Difficulty Level", ["Easy", "Medium", "Hard", "Expert"], value="Medium")
                num_questions = st.select_slider("Number of Questions", [5, 7, 10, 12, 15], value=7)
                focus = st.multiselect(
                    "Question Focus",
                    ["Behavioral", "Technical", "System Design", "Situational", "Leadership"],
                    default=["Behavioral", "Technical"]
                )

                start_btn = st.form_submit_button("🚀 Start Interview", use_container_width=True)

                if start_btn:
                    if not role.strip():
                        st.error("Please enter a job role.")
                    else:
                        with st.spinner(f"Generating {num_questions} AI interview questions..."):
                            questions = generate_mock_interview_questions(role.strip(), difficulty, num_questions)

                        if questions:
                            st.session_state.interview_questions = questions
                            st.session_state.interview_active = True
                            st.session_state.interview_question_idx = 0
                            st.session_state.interview_answers = {}
                            st.session_state.interview_scores = {}
                            st.session_state.interview_complete = False
                            st.session_state.interview_role = role.strip()
                            st.session_state.interview_difficulty = difficulty
                            st.rerun()
                        else:
                            st.error("Failed to generate questions. Please try again.")

            st.markdown('</div>', unsafe_allow_html=True)

        with col_info:
            st.markdown("""
            <div style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);border-radius:20px;padding:32px;">
              <div style="font-weight:700;color:white;font-size:18px;margin-bottom:16px;">🎯 How It Works</div>
              <div style="display:flex;flex-direction:column;gap:20px;">
                <div style="display:flex;gap:14px;align-items:flex-start;">
                  <div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:white;font-weight:700;min-width:32px;">1</div>
                  <div><div style="font-weight:600;color:white;font-size:14px;">Configure</div><div style="font-size:13px;color:#64748b;margin-top:2px;">Choose your role, difficulty, and question types</div></div>
                </div>
                <div style="display:flex;gap:14px;align-items:flex-start;">
                  <div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:white;font-weight:700;min-width:32px;">2</div>
                  <div><div style="font-weight:600;color:white;font-size:14px;">Answer</div><div style="font-size:13px;color:#64748b;margin-top:2px;">Write detailed answers to each AI-generated question</div></div>
                </div>
                <div style="display:flex;gap:14px;align-items:flex-start;">
                  <div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:white;font-weight:700;min-width:32px;">3</div>
                  <div><div style="font-weight:600;color:white;font-size:14px;">Get Scored</div><div style="font-size:13px;color:#64748b;margin-top:2px;">Receive AI scoring and detailed improvement feedback</div></div>
                </div>
                <div style="display:flex;gap:14px;align-items:flex-start;">
                  <div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:white;font-weight:700;min-width:32px;">4</div>
                  <div><div style="font-weight:600;color:white;font-size:14px;">Improve</div><div style="font-size:13px;color:#64748b;margin-top:2px;">Review detailed feedback and practice until confident</div></div>
                </div>
              </div>
            </div>

            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:24px;margin-top:16px;">
              <div style="font-weight:700;color:white;font-size:14px;margin-bottom:12px;">🏆 Pro Tips</div>
              <div style="font-size:13px;color:#94a3b8;line-height:1.9;">
                • Use the STAR method: Situation, Task, Action, Result<br>
                • Quantify your achievements with specific metrics<br>
                • Keep answers focused: 1-3 minutes speaking time<br>
                • Show enthusiasm and cultural fit in every answer<br>
                • Prepare questions for the interviewer too
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ─── Active Interview ──────────────────────────────────────────────────────
    elif st.session_state.interview_active:
        questions = st.session_state.interview_questions
        idx = st.session_state.interview_question_idx
        total = len(questions)
        progress = (idx + 1) / total

        # Progress bar
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;margin-bottom:20px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <div style="font-weight:700;color:white;">Question {idx+1} of {total}</div>
            <div style="display:flex;gap:10px;align-items:center;">
              <span style="font-size:13px;color:#64748b;">Role: <strong style="color:white">{st.session_state.get('interview_role','')}</strong></span>
              <span class="job-tag">{st.session_state.get('interview_difficulty','Medium')}</span>
            </div>
          </div>
          <div style="background:rgba(255,255,255,0.06);border-radius:6px;height:6px;overflow:hidden;">
            <div style="width:{int(progress*100)}%;height:100%;background:linear-gradient(90deg,#6366f1,#06b6d4);border-radius:6px;transition:width 0.4s;"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if idx < total:
            q = questions[idx]
            type_colors = {"Behavioral": "#818cf8", "Technical": "#06b6d4", "System Design": "#f59e0b", "Situational": "#22c55e", "Leadership": "#ec4899"}
            type_color = type_colors.get(q.get("type", ""), "#818cf8")

            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:28px;margin-bottom:20px;">
              <div style="display:flex;gap:10px;margin-bottom:16px;align-items:center;">
                <span style="background:rgba(99,102,241,0.15);color:#a5b4fc;padding:4px 12px;border-radius:100px;font-size:12px;font-weight:600;">Q{idx+1}</span>
                <span style="background:rgba(99,102,241,0.1);color:{type_color};padding:4px 12px;border-radius:100px;font-size:12px;font-weight:600;">{q.get('type','')}</span>
                <span style="background:rgba(255,255,255,0.05);color:#64748b;padding:4px 12px;border-radius:100px;font-size:12px;">{q.get('category','')}</span>
              </div>
              <div style="font-size:18px;font-weight:600;color:white;line-height:1.5;margin-bottom:16px;">{q.get('question','')}</div>
              <div style="background:rgba(99,102,241,0.06);border-left:3px solid #6366f1;padding:12px 16px;border-radius:0 8px 8px 0;">
                <div style="font-size:12px;font-weight:600;color:#a5b4fc;margin-bottom:4px;">💡 TIP</div>
                <div style="font-size:13px;color:#94a3b8;">{q.get('tips','')}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Answer form
            answer_key = f"answer_{idx}"
            with st.form(f"answer_form_{idx}"):
                answer = st.text_area(
                    "Your Answer",
                    placeholder="Type your answer here. Use the STAR method: Situation → Task → Action → Result...",
                    height=180,
                    key=answer_key,
                    label_visibility="collapsed"
                )

                col_skip, col_submit = st.columns([1, 3])
                with col_skip:
                    skip = st.form_submit_button("⏭ Skip", use_container_width=True)
                with col_submit:
                    submit = st.form_submit_button("✅ Submit & Get Score", use_container_width=True)

                if submit:
                    if not answer.strip():
                        st.error("Please provide an answer before submitting.")
                    else:
                        with st.spinner("🤖 AI is scoring your answer..."):
                            score_result = evaluate_interview_answer(
                                q.get("question", ""),
                                answer.strip(),
                                st.session_state.get("interview_role", "")
                            )
                        st.session_state.interview_answers[idx] = answer.strip()
                        st.session_state.interview_scores[idx] = score_result

                        if idx + 1 >= total:
                            st.session_state.interview_active = False
                            st.session_state.interview_complete = True
                        else:
                            st.session_state.interview_question_idx = idx + 1
                        st.rerun()

                if skip:
                    if idx + 1 >= total:
                        st.session_state.interview_active = False
                        st.session_state.interview_complete = True
                    else:
                        st.session_state.interview_question_idx = idx + 1
                    st.rerun()

            # Show score if answered
            if idx in st.session_state.interview_scores:
                score_data = st.session_state.interview_scores[idx]
                sc = score_data.get("score", 0)
                sc_color = "#22c55e" if sc >= 80 else "#f59e0b" if sc >= 60 else "#ef4444"
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;margin-top:16px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                    <span style="font-weight:700;color:white;">Score: <span style="color:{sc_color};">{sc}/100</span> · Grade: <span style="color:{sc_color};">{score_data.get('grade','')}</span></span>
                  </div>
                  <p style="font-size:14px;color:#94a3b8;">{score_data.get('feedback','')}</p>
                  <div style="font-size:13px;color:#64748b;margin-top:8px;font-style:italic;">Follow-up: "{score_data.get('follow_up','')}"</div>
                </div>
                """, unsafe_allow_html=True)

    # ─── Results Screen ────────────────────────────────────────────────────────
    elif st.session_state.interview_complete:
        scores = st.session_state.interview_scores
        questions = st.session_state.interview_questions

        answered = len(st.session_state.interview_answers)
        avg_score = int(sum([v.get("score", 0) for v in scores.values()]) / max(len(scores), 1))
        avg_grade = "A" if avg_score >= 90 else "B+" if avg_score >= 80 else "B" if avg_score >= 70 else "C+" if avg_score >= 60 else "C"
        grade_color = "#22c55e" if avg_score >= 80 else "#f59e0b" if avg_score >= 60 else "#ef4444"

        st.markdown(f"""
        <div style="text-align:center;padding:40px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:24px;margin-bottom:28px;">
          <div style="font-size:48px;margin-bottom:16px;">🏆</div>
          <div style="font-size:32px;font-weight:800;color:{grade_color};margin-bottom:8px;">{avg_score}/100</div>
          <div style="font-size:20px;font-weight:700;color:white;margin-bottom:6px;">Interview Complete!</div>
          <div style="font-size:14px;color:#64748b;">You answered {answered} of {len(questions)} questions · Average grade: <strong style="color:{grade_color};">{avg_grade}</strong></div>
        </div>
        """, unsafe_allow_html=True)

        # Per-question breakdown
        st.markdown('<div style="font-weight:700;color:white;font-size:16px;margin-bottom:16px;">📊 Question-by-Question Breakdown</div>', unsafe_allow_html=True)
        for i, q in enumerate(questions):
            score_data = scores.get(i, {})
            sc = score_data.get("score", 0)
            sc_color = "#22c55e" if sc >= 80 else "#f59e0b" if sc >= 60 else "#ef4444"
            with st.expander(f"Q{i+1}: {q.get('question','')[:70]}... — Score: {sc}/100"):
                col_ans, col_fb = st.columns([1, 1])
                with col_ans:
                    ans = st.session_state.interview_answers.get(i, "*Skipped*")
                    st.markdown(f'<div style="font-size:13px;color:#94a3b8;">{ans}</div>', unsafe_allow_html=True)
                with col_fb:
                    if score_data:
                        st.markdown(f'<div style="color:{sc_color};font-weight:700;font-size:16px;margin-bottom:8px;">{sc}/100 · {score_data.get("grade","")}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="font-size:13px;color:#94a3b8;">{score_data.get("feedback","")}</div>', unsafe_allow_html=True)
                        strengths = score_data.get("strengths", [])
                        improvements = score_data.get("improvements", [])
                        if strengths:
                            st.markdown("**Strengths:** " + " · ".join(strengths))
                        if improvements:
                            st.markdown("**Improve:** " + " · ".join(improvements))

        if st.button("🔄 Start New Interview", use_container_width=True):
            for key in ["interview_questions", "interview_answers", "interview_scores", "interview_active", "interview_complete", "interview_question_idx"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
