"""
RYNZ AI Assistant Page – GPT-4o powered career coach
"""
import streamlit as st
from utils.ui import render_page_header
from utils.auth import require_auth
from utils.ai_engine import chat_with_ai, generate_roadmap
from utils.database import save_chat_message


def render():
    require_auth()
    user = st.session_state.get("user", {})

    render_page_header("AI Career Assistant", "Your personal GPT-4o powered career coach", "🤖")
    st.markdown('<div class="page-content">', unsafe_allow_html=True)

    # Initialize chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    col_chat, col_tools = st.columns([3, 1])

    with col_chat:
        # ─── Chat Interface ───────────────────────────────────────────────────
        st.markdown("""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:20px;overflow:hidden;">
          <div style="display:flex;align-items:center;gap:12px;padding:18px 24px;background:rgba(255,255,255,0.03);border-bottom:1px solid rgba(255,255,255,0.06);">
            <div style="width:36px;height:36px;background:linear-gradient(135deg,#6366f1,#06b6d4);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;">⚡</div>
            <div>
              <div style="font-weight:700;color:white;font-size:14px;">RYNZ AI</div>
              <div style="font-size:12px;color:#22c55e;">● Online · GPT-4o Powered</div>
            </div>
            <div style="margin-left:auto;">
        """, unsafe_allow_html=True)

        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

        st.markdown('</div></div>', unsafe_allow_html=True)

        # Messages display
        chat_html = '<div class="chat-container" style="background:transparent;padding:24px;max-height:480px;overflow-y:auto;">'

        if not st.session_state.chat_history:
            chat_html += """
            <div class="msg-wrapper">
              <div class="ai-avatar">⚡</div>
              <div class="ai-msg-bubble">
                👋 Hi! I'm <strong>RYNZ AI</strong>, your personal career coach powered by GPT-4o.<br><br>
                I can help you with:<br>
                📄 <strong>Resume review</strong> & ATS optimization<br>
                🎤 <strong>Interview prep</strong> & mock interviews<br>
                🗺️ <strong>Career roadmaps</strong> & skill gap analysis<br>
                💰 <strong>Salary negotiation</strong> strategies<br>
                💼 <strong>Job search</strong> tactics & networking<br><br>
                What would you like to work on today?
              </div>
            </div>"""

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html += f'<div class="msg-wrapper user"><div class="user-msg-bubble">{msg["content"]}</div></div>'
            else:
                content = msg["content"].replace("\n", "<br>").replace("**", "<strong>").replace("**", "</strong>")
                # Simple bold formatting
                import re
                content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', msg["content"].replace("\n", "<br>"))
                chat_html += f'<div class="msg-wrapper"><div class="ai-avatar">⚡</div><div class="ai-msg-bubble">{content}</div></div>'

        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

        # Input
        st.markdown('<div style="padding:0 0 16px;">', unsafe_allow_html=True)
        with st.form("chat_form", clear_on_submit=True):
            inp_col, btn_col = st.columns([5, 1])
            with inp_col:
                user_input = st.text_input(
                    "",
                    placeholder="Ask me anything about your career...",
                    label_visibility="collapsed",
                    key="chat_input"
                )
            with btn_col:
                submitted = st.form_submit_button("Send ↑", use_container_width=True)

            if submitted and user_input.strip():
                # Add user message
                st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
                save_chat_message(user.get("id", ""), "user", user_input.strip())

                # Get AI response
                with st.spinner("RYNZ AI is thinking..."):
                    response = chat_with_ai(st.session_state.chat_history, user_context=user)

                st.session_state.chat_history.append({"role": "assistant", "content": response})
                save_chat_message(user.get("id", ""), "assistant", response)
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_tools:
        # ─── Quick Prompts ────────────────────────────────────────────────────
        st.markdown("""
        <div style="font-weight:700;color:white;font-size:15px;margin-bottom:12px;">⚡ Quick Prompts</div>
        """, unsafe_allow_html=True)

        quick_prompts = [
            ("📄", "Review my resume"),
            ("🎤", "Prepare me for interviews"),
            ("🗺️", "Create my career roadmap"),
            ("💰", "Help me negotiate salary"),
            ("💼", "How to find remote jobs"),
            ("🔄", "Career change advice"),
            ("🎓", "Recommend courses for me"),
            ("🤝", "LinkedIn networking tips"),
        ]
        for icon, prompt in quick_prompts:
            if st.button(f"{icon} {prompt}", key=f"qp_{prompt[:10]}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                with st.spinner(""):
                    response = chat_with_ai(st.session_state.chat_history, user_context=user)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # ─── Roadmap Generator ────────────────────────────────────────────────
        st.markdown("""
        <div style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.25);border-radius:16px;padding:20px;margin-top:8px;">
          <div style="font-weight:700;color:white;font-size:14px;margin-bottom:12px;">🗺️ AI Roadmap Generator</div>
        """, unsafe_allow_html=True)

        with st.form("roadmap_form"):
            current = st.text_input("Current Role", placeholder="e.g. Backend Developer")
            target = st.text_input("Target Role", placeholder="e.g. ML Engineer")
            timeline = st.selectbox("Timeline", ["3 months", "6 months", "12 months", "18 months"])
            gen_btn = st.form_submit_button("Generate Roadmap 🚀", use_container_width=True)

            if gen_btn and current and target:
                with st.spinner("Generating your personalized roadmap..."):
                    skills = user.get("skills", [])
                    roadmap = generate_roadmap(current, target, skills, timeline)

                if roadmap:
                    st.markdown('<div style="margin-top:16px;">', unsafe_allow_html=True)
                    st.markdown(f'<div style="font-weight:700;color:white;font-size:13px;margin-bottom:12px;">{roadmap.get("title","Roadmap")}</div>', unsafe_allow_html=True)

                    for phase in roadmap.get("phases", []):
                        with st.expander(f"Phase {phase['phase']}: {phase['title']} – {phase['duration']}"):
                            st.markdown(f"**Focus:** {phase['focus']}")
                            st.markdown("**Tasks:**")
                            for task in phase.get("tasks", []):
                                st.markdown(f"• {task}")
                            st.markdown(f"**🏆 Milestone:** {phase.get('milestone','')}")

                    salary = roadmap.get("salary_range", "")
                    if salary:
                        st.markdown(f'<div style="margin-top:12px;padding:12px;background:rgba(34,197,94,0.1);border-radius:10px;font-size:13px;color:#86efac;">💰 Expected Salary: {salary}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Chat history count
        count = len([m for m in st.session_state.chat_history if m["role"] == "user"])
        st.markdown(f'<div style="text-align:center;font-size:12px;color:#475569;margin-top:12px;">{count} messages in this session</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
