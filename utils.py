"""
RYNZ UI Utilities – Global CSS, Navbar, Footer, Components
"""
import streamlit as st


def inject_global_css():
    st.markdown("""
<style>
/* ─── FONTS & RESET ─────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { scroll-behavior: smooth; }

/* ─── STREAMLIT OVERRIDES ───────────────────────── */
.stApp { background: #020408 !important; color: #e2e8f0; font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.stButton > button { all: unset; cursor: pointer; }
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 10px !important;
  color: #e2e8f0 !important;
  padding: 12px 16px !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 14px !important;
  transition: border-color 0.2s ease !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: rgba(99,102,241,0.6) !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
  outline: none !important;
}
.stCheckbox label span { color: #94a3b8 !important; font-size: 13px; }
.stSelectbox > div > div { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; color: #e2e8f0 !important; }
.stFormSubmitButton > button {
  all: unset !important;
  display: block !important;
  width: 100% !important;
  text-align: center !important;
  background: linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4) !important;
  color: white !important;
  padding: 14px !important;
  border-radius: 12px !important;
  font-weight: 600 !important;
  font-size: 15px !important;
  cursor: pointer !important;
  transition: all 0.3s ease !important;
  margin-top: 8px !important;
}
.stFormSubmitButton > button:hover { opacity: 0.9; transform: translateY(-1px); }

/* ─── NAVBAR ────────────────────────────────────── */
.rynz-navbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 64px;
  background: rgba(2,4,8,0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255,255,255,0.06);
  position: sticky; top: 0; z-index: 999;
}
.nav-logo { font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; color: white; text-decoration: none; display: flex; align-items: center; gap: 8px; }
.nav-logo span { background: linear-gradient(135deg, #6366f1, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.nav-links { display: flex; align-items: center; gap: 32px; }
.nav-links a { color: #94a3b8; text-decoration: none; font-size: 14px; font-weight: 500; transition: color 0.2s; }
.nav-links a:hover { color: white; }
.nav-actions { display: flex; gap: 12px; align-items: center; }

/* ─── BUTTONS ───────────────────────────────────── */
.btn-primary {
  display: inline-flex; align-items: center; gap: 8px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white !important; text-decoration: none;
  padding: 12px 24px; border-radius: 10px;
  font-weight: 600; font-size: 14px;
  transition: all 0.3s ease;
  border: none; cursor: pointer;
  box-shadow: 0 0 20px rgba(99,102,241,0.3);
}
.btn-primary:hover { opacity: 0.9; transform: translateY(-2px); box-shadow: 0 0 30px rgba(99,102,241,0.5); }

.btn-secondary {
  display: inline-flex; align-items: center;
  background: rgba(255,255,255,0.08);
  color: white !important; text-decoration: none;
  padding: 12px 24px; border-radius: 10px;
  font-weight: 600; font-size: 14px;
  border: 1px solid rgba(255,255,255,0.12);
  transition: all 0.3s ease; cursor: pointer;
}
.btn-secondary:hover { background: rgba(255,255,255,0.12); }

.btn-outline {
  display: block; text-align: center;
  background: transparent;
  color: white !important; text-decoration: none;
  padding: 12px 24px; border-radius: 10px;
  font-weight: 600; font-size: 14px;
  border: 1px solid rgba(255,255,255,0.2);
  transition: all 0.3s ease; cursor: pointer;
}
.btn-outline:hover { border-color: rgba(99,102,241,0.6); color: #6366f1 !important; }

/* ─── HERO SECTION ──────────────────────────────── */
.hero-section {
  position: relative; overflow: hidden;
  padding: 120px 64px 100px;
  text-align: center;
  background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(99,102,241,0.15) 0%, transparent 60%),
              radial-gradient(ellipse 60% 50% at 80% 50%, rgba(6,182,212,0.08) 0%, transparent 50%);
}
.hero-badge {
  display: inline-flex; align-items: center;
  background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.25);
  color: #a5b4fc; padding: 8px 20px; border-radius: 100px;
  font-size: 13px; font-weight: 500; margin-bottom: 32px;
  animation: fadeInUp 0.6s ease;
}
.hero-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(48px, 7vw, 88px); font-weight: 800;
  line-height: 1.05; color: white; margin-bottom: 24px;
  animation: fadeInUp 0.7s ease 0.1s both;
}
.gradient-text {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 40%, #06b6d4 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-subtitle {
  font-size: 18px; color: #94a3b8; line-height: 1.7;
  max-width: 640px; margin: 0 auto 40px;
  animation: fadeInUp 0.7s ease 0.2s both;
}
.hero-cta-group {
  display: flex; gap: 16px; justify-content: center; align-items: center;
  margin-bottom: 64px; flex-wrap: wrap;
  animation: fadeInUp 0.7s ease 0.3s both;
}
.hero-stats {
  display: inline-flex; align-items: center; gap: 32px;
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
  padding: 20px 40px; border-radius: 16px;
  animation: fadeInUp 0.7s ease 0.4s both;
}
.stat-item { text-align: center; }
.stat-num { display: block; font-size: 22px; font-weight: 700; color: white; }
.stat-label { font-size: 12px; color: #64748b; }
.stat-divider { width: 1px; height: 32px; background: rgba(255,255,255,0.08); }
.hero-glow {
  position: absolute; top: -200px; left: 50%; transform: translateX(-50%);
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
  pointer-events: none; animation: pulse 4s ease-in-out infinite;
}

/* ─── SECTIONS ──────────────────────────────────── */
.section-spacer { height: 80px; }
.section-header { text-align: center; padding: 0 64px 48px; }
.section-tag {
  display: inline-block; background: rgba(99,102,241,0.12);
  border: 1px solid rgba(99,102,241,0.25); color: #a5b4fc;
  padding: 6px 16px; border-radius: 100px; font-size: 12px;
  font-weight: 600; text-transform: uppercase; letter-spacing: 1px;
  margin-bottom: 16px;
}
.section-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(32px, 4vw, 52px); font-weight: 700;
  color: white; line-height: 1.15;
}

/* ─── BENTO GRID ────────────────────────────────── */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px; padding: 0 64px;
}
.bento-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px; padding: 32px;
  cursor: pointer; transition: all 0.3s ease;
  position: relative; overflow: hidden;
}
.bento-wide { grid-column: span 2; }
.bento-card:hover { background: rgba(255,255,255,0.06); border-color: rgba(99,102,241,0.3); transform: translateY(-4px); box-shadow: 0 20px 40px rgba(0,0,0,0.3); }
.bento-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(99,102,241,0.4), transparent); opacity: 0; transition: opacity 0.3s; }
.bento-card:hover::before { opacity: 1; }
.bento-icon { font-size: 32px; margin-bottom: 12px; }
.bento-tag { display: inline-block; background: rgba(99,102,241,0.15); color: #a5b4fc; padding: 4px 12px; border-radius: 100px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; }
.bento-title { font-size: 20px; font-weight: 700; color: white; margin-bottom: 10px; }
.bento-desc { font-size: 14px; color: #64748b; line-height: 1.6; }
.bento-arrow { position: absolute; bottom: 24px; right: 24px; color: rgba(255,255,255,0.2); font-size: 18px; transition: all 0.3s; }
.bento-card:hover .bento-arrow { color: #6366f1; transform: translate(4px, -4px); }

/* ─── AI PREVIEW ────────────────────────────────── */
.ai-preview-section { padding: 0 64px; }
.chat-preview {
  max-width: 720px; margin: 0 auto;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 24px; overflow: hidden;
  box-shadow: 0 40px 80px rgba(0,0,0,0.4), 0 0 0 1px rgba(99,102,241,0.1);
}
.chat-header { display: flex; align-items: center; gap: 12px; padding: 20px 24px; background: rgba(255,255,255,0.03); border-bottom: 1px solid rgba(255,255,255,0.06); }
.chat-avatar { width: 36px; height: 36px; background: linear-gradient(135deg, #6366f1, #06b6d4); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; }
.chat-name { display: block; font-weight: 600; color: white; font-size: 14px; }
.chat-status { font-size: 12px; color: #22c55e; }
.chat-messages { padding: 24px; display: flex; flex-direction: column; gap: 16px; }
.chat-msg { display: flex; }
.chat-msg.user { justify-content: flex-end; }
.msg-bubble { max-width: 75%; padding: 14px 18px; border-radius: 16px; font-size: 14px; line-height: 1.6; }
.chat-msg.assistant .msg-bubble { background: rgba(255,255,255,0.06); color: #e2e8f0; border-bottom-left-radius: 4px; }
.chat-msg.user .msg-bubble { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; border-bottom-right-radius: 4px; }
.chat-typing { display: flex; align-items: center; gap: 6px; padding: 8px; }
.chat-typing span { width: 8px; height: 8px; background: #6366f1; border-radius: 50%; animation: typingDot 1.4s ease-in-out infinite; }
.chat-typing span:nth-child(2) { animation-delay: 0.2s; }
.chat-typing span:nth-child(3) { animation-delay: 0.4s; }
.chat-input-preview { display: flex; align-items: center; gap: 12px; padding: 16px 20px; background: rgba(255,255,255,0.03); border-top: 1px solid rgba(255,255,255,0.06); }
.chat-input-preview input { flex: 1; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; padding: 12px 16px; border-radius: 10px; font-size: 14px; cursor: not-allowed; }
.chat-send { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; border: none; width: 36px; height: 36px; border-radius: 8px; font-size: 16px; cursor: pointer; }

/* ─── TESTIMONIALS ──────────────────────────────── */
.testimonials-grid {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 20px; padding: 0 64px;
}
.testimonial-card {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px; padding: 28px;
  transition: all 0.3s ease;
}
.testimonial-card:hover { transform: translateY(-4px); border-color: rgba(99,102,241,0.3); }
.t-rating { color: #f59e0b; font-size: 14px; margin-bottom: 12px; }
.t-text { color: #94a3b8; font-size: 14px; line-height: 1.7; margin-bottom: 20px; font-style: italic; }
.t-author { display: flex; align-items: center; gap: 12px; }
.t-avatar { width: 40px; height: 40px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; color: white; }
.t-name { display: block; font-weight: 600; color: white; font-size: 14px; }
.t-role { font-size: 12px; color: #64748b; }

/* ─── PRICING ───────────────────────────────────── */
.pricing-grid {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 24px; padding: 0 64px; align-items: start;
}
.pricing-card, .pricing-card-highlight {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 24px; padding: 36px;
  position: relative; transition: all 0.3s ease;
}
.pricing-card-highlight {
  background: rgba(99,102,241,0.08);
  border-color: rgba(99,102,241,0.4);
  box-shadow: 0 0 40px rgba(99,102,241,0.15);
}
.pricing-badge {
  display: inline-block; background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white; padding: 6px 14px; border-radius: 100px;
  font-size: 12px; font-weight: 600; margin-bottom: 16px;
}
.pricing-name { font-size: 18px; font-weight: 700; color: white; margin-bottom: 8px; }
.pricing-price { font-size: 42px; font-weight: 800; color: white; margin-bottom: 24px; }
.pricing-period { font-size: 16px; color: #64748b; font-weight: 400; }
.pricing-features { list-style: none; margin-bottom: 32px; display: flex; flex-direction: column; gap: 12px; }
.pricing-feature { display: flex; align-items: center; gap: 10px; font-size: 14px; color: #94a3b8; }
.pf-check { color: #22c55e; font-weight: 700; }

/* ─── AUTH MODAL ────────────────────────────────── */
.auth-overlay {
  min-height: 100vh; display: flex; align-items: center; justify-content: center;
  padding: 40px 20px;
  background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(99,102,241,0.12) 0%, transparent 60%);
}
.auth-modal {
  background: rgba(255,255,255,0.04); backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.1); border-radius: 24px;
  padding: 48px 40px; width: 100%; max-width: 440px;
}
.auth-header { text-align: center; margin-bottom: 32px; }
.auth-logo { display: block; font-size: 24px; font-weight: 800; color: white; margin-bottom: 16px; }
.auth-header h2 { font-size: 26px; font-weight: 700; color: white; margin-bottom: 8px; }
.auth-header p { font-size: 14px; color: #64748b; }
.auth-footer { text-align: center; margin-top: 24px; }
.auth-footer p { font-size: 14px; color: #64748b; margin-bottom: 8px; }
.auth-footer a { color: #818cf8; text-decoration: none; font-weight: 500; }
.auth-footer a:hover { color: #6366f1; }

/* ─── SIDEBAR ───────────────────────────────────── */
[data-testid="stSidebar"] {
  background: rgba(2,4,8,0.95) !important;
  border-right: 1px solid rgba(255,255,255,0.06) !important;
  padding: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 4px; }
.sidebar-logo { font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 800; color: white; padding: 24px 20px 16px; }
.sidebar-user { display: flex; align-items: center; gap: 12px; padding: 12px 20px; background: rgba(255,255,255,0.04); border-radius: 12px; margin: 0 12px; }
.sidebar-avatar { width: 38px; height: 38px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; color: white; font-size: 14px; min-width: 38px; }
.sidebar-name { font-size: 14px; font-weight: 600; color: white; display: block; }
.sidebar-email { font-size: 11px; color: #64748b; display: block; }
[data-testid="stSidebar"] .stButton > button {
  all: unset !important; display: flex !important; align-items: center !important;
  width: 100% !important; padding: 10px 20px !important; border-radius: 10px !important;
  color: #94a3b8 !important; font-size: 14px !important; font-weight: 500 !important;
  cursor: pointer !important; transition: all 0.2s !important; gap: 8px !important;
}
[data-testid="stSidebar"] .stButton > button:hover { background: rgba(255,255,255,0.06) !important; color: white !important; }
.nav-active button { background: rgba(99,102,241,0.15) !important; color: #818cf8 !important; }

/* ─── INNER PAGE COMPONENTS ─────────────────────── */
.page-header { padding: 32px 40px 24px; border-bottom: 1px solid rgba(255,255,255,0.06); }
.page-title { font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 700; color: white; margin-bottom: 6px; }
.page-subtitle { font-size: 14px; color: #64748b; }
.page-content { padding: 32px 40px; }

.metric-card {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px; padding: 24px; text-align: center; transition: all 0.3s ease;
}
.metric-card:hover { border-color: rgba(99,102,241,0.3); transform: translateY(-2px); }
.metric-icon { font-size: 28px; margin-bottom: 12px; }
.metric-value { font-size: 32px; font-weight: 800; color: white; margin-bottom: 4px; }
.metric-label { font-size: 13px; color: #64748b; }
.metric-change { font-size: 12px; margin-top: 6px; }
.metric-change.up { color: #22c55e; }
.metric-change.down { color: #ef4444; }

.job-card {
  background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px; padding: 24px; margin-bottom: 16px;
  transition: all 0.3s ease; cursor: pointer;
}
.job-card:hover { border-color: rgba(99,102,241,0.3); transform: translateX(4px); }
.job-title { font-size: 16px; font-weight: 700; color: white; margin-bottom: 4px; }
.job-company { font-size: 14px; color: #94a3b8; margin-bottom: 12px; }
.job-tags { display: flex; flex-wrap: wrap; gap: 8px; }
.job-tag { background: rgba(99,102,241,0.12); color: #a5b4fc; padding: 4px 12px; border-radius: 100px; font-size: 12px; font-weight: 500; }
.job-tag-green { background: rgba(34,197,94,0.1); color: #86efac; }
.job-tag-blue { background: rgba(6,182,212,0.1); color: #67e8f9; }
.job-tag-orange { background: rgba(249,115,22,0.1); color: #fdba74; }
.job-salary { font-size: 14px; color: #22c55e; font-weight: 600; }
.job-time { font-size: 12px; color: #475569; }

.chat-container { height: 500px; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 16px; scroll-behavior: smooth; }
.chat-container::-webkit-scrollbar { width: 4px; }
.chat-container::-webkit-scrollbar-track { background: transparent; }
.chat-container::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 2px; }
.ai-msg-bubble { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; border-bottom-left-radius: 4px; padding: 16px 20px; color: #e2e8f0; font-size: 14px; line-height: 1.7; max-width: 85%; }
.user-msg-bubble { background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 16px; border-bottom-right-radius: 4px; padding: 14px 18px; color: white; font-size: 14px; max-width: 75%; align-self: flex-end; }
.msg-wrapper { display: flex; align-items: flex-start; gap: 12px; }
.msg-wrapper.user { justify-content: flex-end; }
.ai-avatar { width: 32px; height: 32px; background: linear-gradient(135deg, #6366f1, #06b6d4); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; min-width: 32px; }

.upload-zone {
  border: 2px dashed rgba(99,102,241,0.3);
  border-radius: 16px; padding: 48px; text-align: center;
  transition: all 0.3s ease; cursor: pointer;
  background: rgba(99,102,241,0.04);
}
.upload-zone:hover { border-color: rgba(99,102,241,0.6); background: rgba(99,102,241,0.08); }
.upload-icon { font-size: 48px; margin-bottom: 16px; }
.upload-text { font-size: 16px; color: #94a3b8; }

.score-ring {
  width: 120px; height: 120px; border-radius: 50%;
  background: conic-gradient(#6366f1 var(--score), rgba(255,255,255,0.05) 0);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 16px;
}
.score-inner { width: 90px; height: 90px; background: #020408; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-direction: column; }
.score-num { font-size: 24px; font-weight: 800; color: white; }
.score-text { font-size: 10px; color: #64748b; }

.news-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 20px; margin-bottom: 12px; transition: all 0.3s ease; text-decoration: none; display: block; }
.news-card:hover { border-color: rgba(99,102,241,0.3); transform: translateY(-2px); }
.news-title { font-size: 15px; font-weight: 600; color: white; margin-bottom: 8px; line-height: 1.4; }
.news-meta { font-size: 12px; color: #64748b; display: flex; gap: 12px; }
.news-source { color: #818cf8; }

.scholarship-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 24px; margin-bottom: 16px; transition: all 0.3s ease; }
.scholarship-card:hover { border-color: rgba(99,102,241,0.3); transform: translateY(-2px); }
.sch-title { font-size: 16px; font-weight: 700; color: white; margin-bottom: 6px; }
.sch-org { font-size: 13px; color: #94a3b8; margin-bottom: 12px; }
.sch-amount { font-size: 18px; font-weight: 700; color: #22c55e; }
.sch-deadline { font-size: 12px; color: #ef4444; }

/* ─── FOOTER ────────────────────────────────────── */
.rynz-footer {
  border-top: 1px solid rgba(255,255,255,0.06);
  padding: 60px 64px 40px; margin-top: 80px;
}
.footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 40px; margin-bottom: 40px; }
.footer-brand p { color: #475569; font-size: 14px; line-height: 1.7; margin-top: 12px; max-width: 280px; }
.footer-col h4 { font-weight: 600; color: white; margin-bottom: 16px; font-size: 14px; }
.footer-col a { display: block; color: #475569; text-decoration: none; font-size: 13px; margin-bottom: 10px; transition: color 0.2s; }
.footer-col a:hover { color: #94a3b8; }
.footer-bottom { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 28px; }
.footer-copy { color: #374151; font-size: 13px; }
.footer-links { display: flex; gap: 24px; }
.footer-links a { color: #374151; text-decoration: none; font-size: 13px; }

/* ─── ANIMATIONS ────────────────────────────────── */
@keyframes fadeInUp { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse { 0%, 100% { opacity: 0.6; transform: translateX(-50%) scale(1); } 50% { opacity: 0.9; transform: translateX(-50%) scale(1.08); } }
@keyframes typingDot { 0%, 60%, 100% { transform: translateY(0); opacity: 0.4; } 30% { transform: translateY(-6px); opacity: 1; } }
@keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
.skeleton { background: linear-gradient(90deg, rgba(255,255,255,0.03) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.03) 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 8px; }

/* ─── RESPONSIVE ────────────────────────────────── */
@media (max-width: 1024px) {
  .hero-section, .rynz-navbar, .ai-preview-section,
  .section-header, .bento-grid, .testimonials-grid,
  .pricing-grid, .rynz-footer, .footer-grid { padding-left: 24px !important; padding-right: 24px !important; }
  .bento-grid { grid-template-columns: repeat(2, 1fr) !important; }
  .bento-wide { grid-column: span 2; }
  .testimonials-grid { grid-template-columns: repeat(2, 1fr) !important; }
  .pricing-grid { grid-template-columns: 1fr !important; }
  .footer-grid { grid-template-columns: 1fr 1fr !important; }
}
@media (max-width: 640px) {
  .bento-grid { grid-template-columns: 1fr !important; }
  .bento-wide { grid-column: span 1 !important; }
  .testimonials-grid { grid-template-columns: 1fr !important; }
  .hero-stats { flex-wrap: wrap; gap: 16px; }
  .stat-divider { display: none; }
  .nav-links { display: none; }
  .rynz-navbar { padding: 16px 20px !important; }
  .hero-section { padding: 80px 20px 60px !important; }
}
</style>
""", unsafe_allow_html=True)


def render_navbar(authenticated=False):
    if authenticated:
        user = st.session_state.get("user", {})
        name = user.get("full_name", "User")
        st.markdown(f"""
        <div class="rynz-navbar">
          <a class="nav-logo" href="?page=dashboard">⚡ <span>RYNZ</span></a>
          <div class="nav-links">
            <a href="?page=jobs">Jobs</a>
            <a href="?page=internships">Internships</a>
            <a href="?page=scholarships">Scholarships</a>
            <a href="?page=ai_assistant">AI Assistant</a>
            <a href="?page=news">News</a>
          </div>
          <div class="nav-actions">
            <span style="color:#94a3b8;font-size:14px">Hello, {name.split()[0]}</span>
            <a href="?page=logout" class="btn-secondary" style="padding:8px 16px;font-size:13px">Sign Out</a>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="rynz-navbar">
          <a class="nav-logo" href="?page=home">⚡ <span>RYNZ</span></a>
          <div class="nav-links">
            <a href="#features">Features</a>
            <a href="#pricing">Pricing</a>
            <a href="?page=jobs">Jobs</a>
            <a href="?page=scholarships">Scholarships</a>
          </div>
          <div class="nav-actions">
            <a href="?page=login" class="btn-secondary" style="padding:10px 20px;font-size:14px">Sign In</a>
            <a href="?page=signup" class="btn-primary" style="padding:10px 20px;font-size:14px">Get Started</a>
          </div>
        </div>
        """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="rynz-footer">
      <div class="footer-grid">
        <div class="footer-brand">
          <span style="font-family:'Space Grotesk',sans-serif;font-size:22px;font-weight:800;color:white">⚡ RYNZ</span>
          <p>The world's most advanced AI-powered career ecosystem. Helping 50,000+ professionals land their dream roles.</p>
        </div>
        <div class="footer-col">
          <h4>Platform</h4>
          <a href="?page=jobs">Jobs</a>
          <a href="?page=internships">Internships</a>
          <a href="?page=scholarships">Scholarships</a>
          <a href="?page=ai_assistant">AI Assistant</a>
          <a href="?page=resume_analyzer">Resume Analyzer</a>
        </div>
        <div class="footer-col">
          <h4>Resources</h4>
          <a href="#">Blog</a>
          <a href="#">Career Guide</a>
          <a href="#">Interview Prep</a>
          <a href="#">Salary Guide</a>
          <a href="#">API Docs</a>
        </div>
        <div class="footer-col">
          <h4>Company</h4>
          <a href="#">About</a>
          <a href="#">Careers</a>
          <a href="#">Press</a>
          <a href="#">Contact</a>
          <a href="#">Status</a>
        </div>
      </div>
      <div class="footer-bottom">
        <span class="footer-copy">© 2025 RYNZ. All rights reserved.</span>
        <div class="footer-links">
          <a href="#">Privacy</a>
          <a href="#">Terms</a>
          <a href="#">Cookies</a>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str = "", icon: str = ""):
    st.markdown(f"""
    <div class="page-header">
      <div class="page-title">{icon} {title}</div>
      {f'<div class="page-subtitle">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def render_metric_cards(metrics: list):
    cols = st.columns(len(metrics))
    for i, m in enumerate(metrics):
        with cols[i]:
            change_class = "up" if m.get("change_dir") == "up" else "down"
            change_html = f'<div class="metric-change {change_class}">{m.get("change","")}</div>' if m.get("change") else ""
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-icon">{m.get('icon','📊')}</div>
              <div class="metric-value">{m['value']}</div>
              <div class="metric-label">{m['label']}</div>
              {change_html}
            </div>
            """, unsafe_allow_html=True)


def render_loading():
    st.markdown("""
    <div style="display:flex;flex-direction:column;gap:12px;padding:24px 0;">
      <div class="skeleton" style="height:60px;border-radius:16px;"></div>
      <div class="skeleton" style="height:100px;border-radius:16px;"></div>
      <div class="skeleton" style="height:80px;border-radius:16px;"></div>
    </div>
    """, unsafe_allow_html=True)


def render_empty_state(icon: str, title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="text-align:center;padding:80px 40px;">
      <div style="font-size:48px;margin-bottom:16px;">{icon}</div>
      <h3 style="font-size:20px;font-weight:700;color:white;margin-bottom:8px;">{title}</h3>
      <p style="font-size:14px;color:#64748b;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
