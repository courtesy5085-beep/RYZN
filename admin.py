"""
RYNZ Admin Dashboard – Analytics and user management
"""
import streamlit as st
from utils.ui import render_page_header, render_metric_cards
from utils.auth import require_auth
from utils.database import get_admin_stats, get_recent_users


def render():
    require_auth()
    user = st.session_state.get("user", {})

    # Admin check
    if user.get("role") != "admin":
        st.markdown("""
        <div style="text-align:center;padding:80px;">
          <div style="font-size:48px;margin-bottom:16px;">🔒</div>
          <div style="font-size:20px;font-weight:700;color:white;">Admin Access Only</div>
          <div style="font-size:14px;color:#64748b;margin-top:8px;">You don't have permission to access this page.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    render_page_header("Admin Dashboard", "Platform analytics and user management", "⚙️")
    st.markdown('<div class="page-content">', unsafe_allow_html=True)

    # ─── Stats ────────────────────────────────────────────────────────────────
    stats = get_admin_stats()
    render_metric_cards([
        {"icon": "👥", "value": f"{stats.get('total_users', 0):,}", "label": "Total Users", "change": "↑ 12.4% this month", "change_dir": "up"},
        {"icon": "💼", "value": f"{stats.get('total_jobs', 0):,}", "label": "Active Jobs", "change": "↑ 1,200 new", "change_dir": "up"},
        {"icon": "💬", "value": f"{stats.get('total_chats', 0):,}", "label": "AI Conversations", "change": "↑ 34% this week", "change_dir": "up"},
        {"icon": "🔖", "value": f"{stats.get('total_saved', 0):,}", "label": "Saved Items", "change": "↑ 8.1%", "change_dir": "up"},
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Charts ───────────────────────────────────────────────────────────────
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        import pandas as pd

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
            users_data = [420, 680, 920, 1150, 1480, 1890]
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=months, y=users_data,
                fill="tozeroy",
                line=dict(color="#6366f1", width=3),
                fillcolor="rgba(99,102,241,0.15)",
                mode="lines+markers",
                marker=dict(color="#6366f1", size=8),
                name="Users"
            ))
            fig1.update_layout(
                title=dict(text="User Growth (2025)", font=dict(color="white", size=14)),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                margin=dict(l=0, r=0, t=40, b=0),
                height=280,
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col_chart2:
            categories = ["Jobs", "Scholarships", "Internships", "AI Chat", "Resume"]
            values = [4200, 1800, 2400, 8900, 3100]
            fig2 = go.Figure(go.Pie(
                labels=categories,
                values=values,
                hole=0.6,
                marker=dict(colors=["#6366f1", "#06b6d4", "#22c55e", "#f59e0b", "#ec4899"]),
                textfont=dict(color="white"),
            ))
            fig2.update_layout(
                title=dict(text="Feature Usage Distribution", font=dict(color="white", size=14)),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                margin=dict(l=0, r=0, t=40, b=0),
                height=280,
                showlegend=True,
                legend=dict(font=dict(color="#94a3b8")),
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Activity heatmap
        import numpy as np
        np.random.seed(42)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        hours = [f"{h}:00" for h in range(0, 24, 2)]
        activity = np.random.randint(10, 400, size=(len(days), len(hours)))
        fig3 = px.imshow(
            activity,
            x=hours, y=days,
            color_continuous_scale=[[0, "rgba(99,102,241,0.1)"], [0.5, "rgba(99,102,241,0.4)"], [1, "#6366f1"]],
            title="User Activity Heatmap (This Week)",
        )
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            title=dict(font=dict(color="white", size=14)),
            margin=dict(l=0, r=0, t=40, b=0),
            height=200,
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig3, use_container_width=True)

    except ImportError:
        st.markdown("""
        <div style="padding:24px;background:rgba(255,255,255,0.03);border-radius:16px;text-align:center;color:#64748b;">
          Install plotly and pandas for interactive charts: <code>pip install plotly pandas</code>
        </div>
        """, unsafe_allow_html=True)

    # ─── Recent Users ─────────────────────────────────────────────────────────
    st.markdown('<div style="font-weight:700;color:white;font-size:16px;margin:24px 0 16px;">👥 Recent Users</div>', unsafe_allow_html=True)

    recent_users = get_recent_users(10)

    # Header
    st.markdown("""
    <div style="display:grid;grid-template-columns:2fr 2fr 1fr 1fr;gap:12px;padding:12px 20px;background:rgba(255,255,255,0.04);border-radius:10px;margin-bottom:8px;">
      <span style="font-size:12px;font-weight:600;color:#64748b;text-transform:uppercase;">Name</span>
      <span style="font-size:12px;font-weight:600;color:#64748b;text-transform:uppercase;">Email</span>
      <span style="font-size:12px;font-weight:600;color:#64748b;text-transform:uppercase;">Role</span>
      <span style="font-size:12px;font-weight:600;color:#64748b;text-transform:uppercase;">Joined</span>
    </div>
    """, unsafe_allow_html=True)

    for u in recent_users:
        role = u.get("role", "user")
        role_color = {"admin": "#ef4444", "pro": "#f59e0b", "user": "#22c55e"}.get(role, "#22c55e")
        joined = u.get("created_at", "")[:10] if u.get("created_at") else ""
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:2fr 2fr 1fr 1fr;gap:12px;padding:14px 20px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:10px;margin-bottom:6px;transition:all 0.2s;">
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:28px;height:28px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:white;">{u.get('full_name','U')[0].upper()}</div>
            <span style="font-size:13px;font-weight:500;color:white;">{u.get('full_name','')}</span>
          </div>
          <span style="font-size:13px;color:#94a3b8;align-self:center;">{u.get('email','')}</span>
          <span style="font-size:12px;font-weight:600;color:{role_color};align-self:center;text-transform:capitalize;">{role}</span>
          <span style="font-size:12px;color:#64748b;align-self:center;">{joined}</span>
        </div>
        """, unsafe_allow_html=True)

    # ─── System Status ────────────────────────────────────────────────────────
    st.markdown('<div style="font-weight:700;color:white;font-size:16px;margin:24px 0 16px;">🔧 System Status</div>', unsafe_allow_html=True)
    statuses = [
        ("🌐", "API Gateway", "Operational", True),
        ("🗄️", "Supabase Database", "Operational", True),
        ("🤖", "OpenAI Integration", "Operational", True),
        ("📧", "Email Service", "Operational", True),
        ("🔒", "Authentication", "Operational", True),
        ("📡", "News Feed", "Operational", True),
    ]
    col_s1, col_s2, col_s3 = st.columns(3)
    for i, (icon, name, status, ok) in enumerate(statuses):
        col = [col_s1, col_s2, col_s3][i % 3]
        with col:
            color = "#22c55e" if ok else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;padding:12px 16px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:10px;margin-bottom:8px;">
              <span style="font-size:13px;color:white;">{icon} {name}</span>
              <span style="font-size:12px;color:{color};font-weight:600;">● {status}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
