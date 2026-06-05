"""
RYNZ News Page – Tech, AI, Business, Startup news
"""
import streamlit as st
from utils.ui import render_page_header
from utils.auth import require_auth
from utils.database import fetch_news


def render():
    require_auth()
    render_page_header("News", "Stay ahead with the latest in tech, AI, and business", "📰")
    st.markdown('<div class="page-content">', unsafe_allow_html=True)

    # Category tabs
    categories = ["Tech", "AI", "Business", "Startups"]
    tab_tech, tab_ai, tab_biz, tab_startups = st.tabs(["🖥️ Tech", "🤖 AI & ML", "📈 Business", "🚀 Startups"])

    def render_news_list(category: str):
        with st.spinner("Loading latest news..."):
            articles = fetch_news(category)

        if not articles:
            st.markdown('<div style="text-align:center;padding:40px;color:#64748b;">No articles found.</div>', unsafe_allow_html=True)
            return

        for article in articles:
            title = article.get("title", "")
            url = article.get("url", "#")
            source = article.get("source", "")
            published = article.get("published", "")[:16] if article.get("published") else ""
            target = 'target="_blank"' if url != "#" else ""
            st.markdown(f"""
            <a href="{url}" {target} class="news-card" style="display:block;text-decoration:none;">
              <div class="news-title">{title}</div>
              <div class="news-meta">
                <span class="news-source">📡 {source}</span>
                <span>🕐 {published}</span>
              </div>
            </a>
            """, unsafe_allow_html=True)

    with tab_tech:
        st.markdown("""
        <div style="padding:4px 0 16px;">
          <span style="font-size:13px;color:#64748b;">Latest in software engineering, developer tools, and platform news</span>
        </div>""", unsafe_allow_html=True)
        render_news_list("Tech")

    with tab_ai:
        st.markdown("""
        <div style="padding:4px 0 16px;">
          <span style="font-size:13px;color:#64748b;">Cutting-edge AI research, model releases, and machine learning breakthroughs</span>
        </div>""", unsafe_allow_html=True)
        render_news_list("AI")

    with tab_biz:
        st.markdown("""
        <div style="padding:4px 0 16px;">
          <span style="font-size:13px;color:#64748b;">Market moves, company earnings, and business strategy insights</span>
        </div>""", unsafe_allow_html=True)
        render_news_list("Business")

    with tab_startups:
        st.markdown("""
        <div style="padding:4px 0 16px;">
          <span style="font-size:13px;color:#64748b;">Startup funding rounds, founder stories, and venture capital news</span>
        </div>""", unsafe_allow_html=True)
        render_news_list("Startups")

    st.markdown('</div>', unsafe_allow_html=True)
