"""
SummarizeAI — Premium AI Text Summarizer + OCR
================================================
Multi-page application with nav-pill routing.
Pages: HOME · ABOUT · CONTENT · OTHERS

Palette:  Navy #0B1B3A · Page #F4F7FB · Card #FFFFFF · Accent #8FB2FF
"""

# ╔══════════════════════════════════════════════════════════════╗
# ║  1. IMPORTS & CONSTANTS                                     ║
# ╚══════════════════════════════════════════════════════════════╝

import streamlit as st
import requests
import time
import html as html_lib

from services.ocr_service import extract_text_from_image, OCRError

API_URL = "http://127.0.0.1:8080/v1/chat/completions"
MODEL   = "local-model"

# ╔══════════════════════════════════════════════════════════════╗
# ║  2. PAGE CONFIG                                             ║
# ╚══════════════════════════════════════════════════════════════╝

st.set_page_config(
    page_title="SummarizeAI — Intelligent Summarizer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ╔══════════════════════════════════════════════════════════════╗
# ║  3. DESIGN SYSTEM — Full CSS                                ║
# ╚══════════════════════════════════════════════════════════════╝

st.markdown("""
<style>
/* ═══════════════════════════════════════════
   3.1 — Design Tokens
   ═══════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --navy:          #0B1B3A;
    --navy-light:    #132B55;
    --accent:        #8FB2FF;
    --accent-hover:  #7BA3F7;
    --accent-light:  #E8F0FF;
    --accent-muted:  rgba(143,178,255,0.10);
    --accent-border: rgba(143,178,255,0.22);
    --accent-ring:   rgba(143,178,255,0.25);

    --bg-page:   #F4F7FB;
    --bg-card:   #FFFFFF;
    --bg-subtle: #EDF1F7;
    --bg-input:  #F4F7FB;

    --border:       #DFE4ED;
    --border-hover: #C8CFD8;
    --border-focus: var(--accent);

    --text-1: #0F172A;
    --text-2: #475569;
    --text-3: #94A3B8;
    --text-on-navy:   #FFFFFF;
    --text-on-accent: #0B1B3A;

    --success:    #059669;
    --success-bg: #ECFDF5;
    --error:      #DC2626;
    --error-bg:   #FEF2F2;
    --warning:    #D97706;
    --info:       #2563EB;

    --sp-1: 4px;  --sp-2: 8px;  --sp-3: 12px;
    --sp-4: 16px; --sp-5: 20px; --sp-6: 24px;
    --sp-8: 32px; --sp-10: 40px; --sp-12: 48px;
    --sp-16: 64px;

    --r-sm:   8px;
    --r-md:   12px;
    --r-lg:   16px;
    --r-xl:   20px;
    --r-2xl:  24px;
    --r-full: 9999px;

    --shadow-xs:  0 1px 2px rgba(11,27,58,0.04);
    --shadow-sm:  0 1px 3px rgba(11,27,58,0.06), 0 1px 2px rgba(11,27,58,0.04);
    --shadow-md:  0 4px 6px -1px rgba(11,27,58,0.07), 0 2px 4px -1px rgba(11,27,58,0.04);
    --shadow-lg:  0 10px 15px -3px rgba(11,27,58,0.08), 0 4px 6px -2px rgba(11,27,58,0.03);
    --shadow-xl:  0 20px 25px -5px rgba(11,27,58,0.10), 0 10px 10px -5px rgba(11,27,58,0.03);

    --ease-fast:   150ms ease;
    --ease-base:   250ms cubic-bezier(.4,0,.2,1);
    --ease-spring: 400ms cubic-bezier(.175,.885,.32,1.275);
}

/* ═══════════════════════════════════════════
   3.2 — Global
   ═══════════════════════════════════════════ */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] * {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont,
                 'Segoe UI', Roboto, sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background: var(--bg-page) !important;
    -webkit-font-smoothing: antialiased;
}
[data-testid="stHeader"] { background: transparent !important; }
.main .block-container {
    padding: 0 var(--sp-8) var(--sp-16) var(--sp-8);
    max-width: 1140px;
}

/* ═══════════════════════════════════════════
   3.3 — Animations
   ═══════════════════════════════════════════ */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}
@keyframes modalFadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes modalSlideUp {
    from { opacity: 0; transform: translateY(30px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* ═══════════════════════════════════════════
   3.4 — Navbar
   ═══════════════════════════════════════════ */
.navbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: var(--sp-3) var(--sp-6);
    background: var(--navy);
    margin: 0 calc(-1 * var(--sp-8)) var(--sp-2) calc(-1 * var(--sp-8));
    animation: fadeIn 0.35s ease-out;
}
.nav-left { display: flex; align-items: center; gap: var(--sp-3); }
.nav-logo {
    width: 34px; height: 34px; background: var(--accent);
    border-radius: var(--r-sm); display: grid; place-items: center;
    color: var(--navy); font-weight: 700; font-size: 1rem; flex-shrink: 0;
}
.nav-brand {
    font-size: 0.95rem; font-weight: 700;
    color: var(--text-on-navy); letter-spacing: -0.3px;
}
.nav-center {
    display: flex; align-items: center;
    background: rgba(255,255,255,0.08);
    border-radius: var(--r-full); padding: 3px 4px; gap: 2px;
}
.nav-pill {
    padding: 7px 18px; font-size: 0.78rem; font-weight: 500;
    color: rgba(255,255,255,0.6); text-decoration: none;
    border-radius: var(--r-full); transition: var(--ease-fast); cursor: pointer;
}
.nav-pill:hover { color: rgba(255,255,255,0.9); background: rgba(255,255,255,0.06); }
.nav-pill.active { background: var(--accent); color: var(--navy); font-weight: 600; }
.nav-right { display: flex; align-items: center; gap: var(--sp-3); }
.nav-upgrade {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 8px 20px; background: var(--accent);
    color: var(--navy); font-size: 0.78rem; font-weight: 700;
    border-radius: var(--r-full); text-decoration: none;
    transition: var(--ease-base); cursor: pointer; border: none;
}
.nav-upgrade:hover {
    background: var(--accent-hover); transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(143,178,255,0.35);
}
.nav-hamburger {
    width: 34px; height: 34px; background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12); border-radius: var(--r-sm);
    display: grid; place-items: center; cursor: pointer; transition: var(--ease-fast);
}
.nav-hamburger:hover { background: rgba(255,255,255,0.14); }
.nav-hamburger svg {
    width: 18px; height: 18px; stroke: rgba(255,255,255,0.7);
    fill: none; stroke-width: 2; stroke-linecap: round;
}

/* ═══════════════════════════════════════════
   3.5 — Hero
   ═══════════════════════════════════════════ */
.hero {
    text-align: center; padding: var(--sp-10) 0 var(--sp-8) 0;
    animation: fadeInUp 0.5s ease-out;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 5px 14px; background: var(--accent-light);
    color: var(--navy); font-size: 0.72rem; font-weight: 600;
    border-radius: var(--r-full); letter-spacing: 0.3px; margin-bottom: var(--sp-4);
}
.hero h1 {
    font-size: 2.2rem; font-weight: 700; color: var(--text-1);
    margin: 0 0 var(--sp-3) 0; letter-spacing: -0.8px; line-height: 1.2;
}
.hero p {
    font-size: 1.05rem; color: var(--text-2);
    margin: 0 auto; max-width: 520px; line-height: 1.6;
}
.trust-row {
    display: flex; align-items: center; justify-content: center;
    gap: var(--sp-6); margin-top: var(--sp-6); flex-wrap: wrap;
}
.trust-item {
    display: flex; align-items: center; gap: 6px;
    font-size: 0.78rem; color: var(--text-3); font-weight: 500;
}

/* ═══════════════════════════════════════════
   3.6 — Cards  (main-card, inner-card)
   ═══════════════════════════════════════════ */
.main-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--r-xl); padding: var(--sp-6);
    box-shadow: var(--shadow-lg);
    animation: fadeInUp 0.5s ease-out both; animation-delay: 0.1s;
}
.main-card:hover { box-shadow: var(--shadow-xl); }
.inner-card {
    background: var(--bg-subtle); border: 1px solid var(--border);
    border-radius: var(--r-md); padding: var(--sp-4);
    margin-bottom: var(--sp-4); transition: var(--ease-fast);
}
.inner-card:hover { border-color: var(--border-hover); }
.ic-header { display: flex; align-items: center; gap: var(--sp-3); margin-bottom: var(--sp-2); }
.ic-icon {
    width: 32px; height: 32px; background: var(--accent-light);
    border-radius: var(--r-sm); display: grid; place-items: center;
    font-size: 0.9rem; flex-shrink: 0;
}
.ic-title { font-size: 0.88rem; font-weight: 600; color: var(--text-1); margin: 0; }
.ic-desc  { font-size: 0.76rem; color: var(--text-3); margin: 0; }

/* ═══════════════════════════════════════════
   3.7 — Result card
   ═══════════════════════════════════════════ */
.result-card {
    background: var(--bg-card); border: 1px solid var(--accent-border);
    border-radius: var(--r-lg); padding: var(--sp-6);
    position: relative; overflow: hidden;
    animation: fadeInUp 0.5s ease-out both; box-shadow: var(--shadow-sm);
}
.result-card::before {
    content: ''; position: absolute; left: 0; top: 0; bottom: 0;
    width: 3px; background: var(--accent); border-radius: 3px 0 0 3px;
}
.result-label {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 0.7rem; font-weight: 600; color: var(--navy);
    text-transform: uppercase; letter-spacing: 0.8px;
    margin-bottom: var(--sp-4); padding-left: var(--sp-3);
}
.result-body {
    color: var(--text-1); font-size: 0.92rem;
    line-height: 1.85; padding-left: var(--sp-3);
}

/* ═══════════════════════════════════════════
   3.8 — Metrics
   ═══════════════════════════════════════════ */
.metrics-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: var(--sp-3); margin-bottom: var(--sp-5);
    animation: fadeInUp 0.4s ease-out both;
}
.m-card {
    background: var(--bg-subtle); border: 1px solid var(--border);
    border-radius: var(--r-md); padding: var(--sp-3) var(--sp-4);
    text-align: center; transition: var(--ease-fast);
}
.m-card:hover { border-color: var(--accent-border); background: var(--accent-light); }
.m-val { font-size: 1.15rem; font-weight: 700; color: var(--navy); margin: 0; }
.m-lbl {
    font-size: 0.64rem; color: var(--text-3);
    text-transform: uppercase; letter-spacing: 0.5px;
    margin: 2px 0 0 0; font-weight: 500;
}

/* ═══════════════════════════════════════════
   3.9 — Empty / Loading
   ═══════════════════════════════════════════ */
.empty-state {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; padding: var(--sp-16) var(--sp-6);
    text-align: center; animation: fadeIn 0.5s ease-out;
}
.empty-icon {
    width: 56px; height: 56px; background: var(--bg-subtle);
    border: 1px solid var(--border); border-radius: var(--r-lg);
    display: grid; place-items: center; margin-bottom: var(--sp-5); color: var(--text-3);
}
.empty-title { font-size: 0.95rem; font-weight: 600; color: var(--text-2); margin: 0 0 var(--sp-2) 0; }
.empty-desc { font-size: 0.82rem; color: var(--text-3); max-width: 280px; margin: 0; line-height: 1.6; }

/* ═══════════════════════════════════════════
   3.10 — Form Elements
   ═══════════════════════════════════════════ */
.counter-row { display: flex; align-items: center; gap: var(--sp-2); margin: var(--sp-2) 0 var(--sp-3) 0; }
.ctr-pill {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 2px 10px; background: var(--bg-subtle);
    border: 1px solid var(--border); border-radius: var(--r-full);
    font-size: 0.68rem; color: var(--text-3); font-weight: 500;
}
.ctr-val { color: var(--text-2); font-weight: 600; }

.stButton > button {
    background: var(--navy) !important; color: var(--text-on-navy) !important;
    border: none !important; border-radius: var(--r-sm) !important;
    padding: 10px 24px !important; font-size: 0.88rem !important;
    font-weight: 600 !important; width: 100%;
    transition: var(--ease-base) !important; box-shadow: var(--shadow-xs) !important;
}
.stButton > button:hover {
    background: var(--navy-light) !important; transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(11,27,58,0.25) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button:disabled {
    background: var(--bg-subtle) !important; color: var(--text-3) !important;
    box-shadow: none !important; transform: none !important;
}

.stTextArea textarea {
    background: var(--bg-card) !important; border: 1px solid var(--border) !important;
    border-radius: var(--r-md) !important; color: var(--text-1) !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.88rem !important;
    line-height: 1.7 !important; transition: var(--ease-fast) !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-ring) !important; outline: none !important;
}
.stTextArea textarea::placeholder { color: var(--text-3) !important; }

[data-testid="stFileUploader"] {
    background: var(--bg-card); border: 2px dashed var(--border);
    border-radius: var(--r-md); padding: var(--sp-5); transition: var(--ease-base);
}
[data-testid="stFileUploader"]:hover { border-color: var(--accent); background: var(--accent-light); }

.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border-color: var(--border) !important; border-radius: var(--r-sm) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 2px; background: var(--bg-subtle); border-radius: var(--r-md);
    padding: 4px; border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: var(--r-sm); padding: 8px 18px;
    font-weight: 500; font-size: 0.84rem; color: var(--text-3);
    transition: var(--ease-fast);
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text-1); }
.stTabs [aria-selected="true"] {
    background: var(--bg-card) !important; color: var(--text-1) !important;
    font-weight: 600; box-shadow: var(--shadow-sm);
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none; }

.streamlit-expanderHeader {
    background: var(--bg-subtle) !important; border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important; font-size: 0.84rem !important;
    font-weight: 500 !important; color: var(--text-2) !important;
}

.stProgress > div > div {
    background: linear-gradient(90deg, var(--navy), var(--accent)) !important;
    background-size: 200% auto; animation: shimmer 2s linear infinite;
    border-radius: var(--r-full);
}
.stProgress > div { background: var(--bg-subtle) !important; border-radius: var(--r-full); }

hr { border-color: var(--border) !important; }

.sec-head {
    display: flex; align-items: center; gap: var(--sp-3);
    margin: var(--sp-6) 0 var(--sp-4) 0; animation: fadeIn 0.4s ease-out;
}
.sec-head h3 {
    font-size: 0.88rem; font-weight: 600; color: var(--text-1);
    margin: 0; white-space: nowrap;
}
.sec-head-line { flex: 1; height: 1px; background: var(--border); }

/* ═══════════════════════════════════════════
   3.11 — Sidebar
   ═══════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { color: var(--text-1); }

.status-chip {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 8px 14px; border-radius: var(--r-sm);
    font-size: 0.8rem; font-weight: 600; width: 100%; box-sizing: border-box;
}
.status-on { background: var(--success-bg); border: 1px solid rgba(5,150,105,0.2); color: var(--success); }
.status-off { background: var(--error-bg); border: 1px solid rgba(220,38,38,0.2); color: var(--error); }
.status-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.status-on .status-dot { background: var(--success); box-shadow: 0 0 6px rgba(5,150,105,0.5); }
.status-off .status-dot { background: var(--error); }
.sidebar-foot {
    background: var(--bg-subtle); border: 1px solid var(--border);
    border-radius: var(--r-md); padding: var(--sp-4); margin-top: var(--sp-4); text-align: center;
}
.sidebar-foot p { font-size: 0.72rem; color: var(--text-3); margin: 2px 0; }

/* ═══════════════════════════════════════════
   3.12 — Footer
   ═══════════════════════════════════════════ */
.app-footer {
    text-align: center; padding: var(--sp-8) 0 var(--sp-4) 0;
    border-top: 1px solid var(--border); margin-top: var(--sp-12);
    animation: fadeIn 0.5s ease-out;
}
.app-footer p { font-size: 0.75rem; color: var(--text-3); margin: 2px 0; }

/* ═══════════════════════════════════════════
   3.13 — Pricing Modal
   ═══════════════════════════════════════════ */
.modal-overlay {
    position: fixed; inset: 0; background: rgba(11,27,58,0.55);
    backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px);
    z-index: 99999; display: flex; align-items: center; justify-content: center;
    animation: modalFadeIn 0.25s ease-out;
}
.modal-box {
    background: var(--bg-card); border-radius: var(--r-2xl); padding: var(--sp-8);
    max-width: 840px; width: 92vw; max-height: 90vh; overflow-y: auto;
    box-shadow: var(--shadow-xl); position: relative; animation: modalSlideUp 0.35s ease-out;
}
.modal-close {
    position: absolute; top: var(--sp-4); right: var(--sp-4);
    width: 32px; height: 32px; background: var(--bg-subtle);
    border: 1px solid var(--border); border-radius: 50%;
    display: grid; place-items: center; cursor: pointer;
    font-size: 0.9rem; color: var(--text-2); transition: var(--ease-fast); line-height: 1;
}
.modal-close:hover { background: var(--error-bg); color: var(--error); border-color: rgba(220,38,38,0.2); }
.modal-title {
    font-size: 1.4rem; font-weight: 700; color: var(--text-1);
    margin: 0 0 4px 0; letter-spacing: -0.5px; text-align: center;
}
.modal-subtitle { font-size: 0.88rem; color: var(--text-3); text-align: center; margin: 0 0 var(--sp-6) 0; }

.pricing-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--sp-4); }
.pricing-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--r-lg); padding: var(--sp-6) var(--sp-5);
    text-align: center; position: relative; transition: var(--ease-base);
}
.pricing-card:hover { border-color: var(--border-hover); box-shadow: var(--shadow-md); transform: translateY(-2px); }
.pricing-card.popular { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent), var(--shadow-lg); }
.popular-badge {
    position: absolute; top: -11px; left: 50%; transform: translateX(-50%);
    background: var(--accent); color: var(--navy);
    font-size: 0.64rem; font-weight: 700; padding: 3px 14px;
    border-radius: var(--r-full); text-transform: uppercase;
    letter-spacing: 0.6px; white-space: nowrap;
}
.plan-name { font-size: 1rem; font-weight: 600; color: var(--text-1); margin: 0 0 var(--sp-2) 0; }
.plan-price { font-size: 1.8rem; font-weight: 700; color: var(--navy); margin: 0; line-height: 1.2; }
.plan-price span { font-size: 0.82rem; font-weight: 400; color: var(--text-3); }
.plan-features { list-style: none; padding: 0; margin: var(--sp-4) 0 var(--sp-5) 0; text-align: left; }
.plan-features li {
    font-size: 0.8rem; color: var(--text-2); padding: 5px 0;
    display: flex; align-items: flex-start; gap: 8px; line-height: 1.4;
}
.plan-features li::before {
    content: '✓'; color: var(--success); font-weight: 700;
    font-size: 0.78rem; flex-shrink: 0; margin-top: 1px;
}

/* ═══════════════════════════════════════════
   3.14 — FAB
   ═══════════════════════════════════════════ */
.fab-next {
    position: fixed; right: 28px; bottom: 32px;
    width: 52px; height: 52px; background: var(--navy);
    border-radius: 50%; display: grid; place-items: center;
    box-shadow: var(--shadow-lg); cursor: pointer;
    transition: var(--ease-base); z-index: 9990;
    border: 2px solid rgba(143,178,255,0.2);
}
.fab-next:hover {
    background: var(--navy-light); transform: translateY(-2px) scale(1.05);
    box-shadow: 0 8px 24px rgba(11,27,58,0.3);
}
.fab-next svg {
    width: 22px; height: 22px; stroke: var(--accent); fill: none;
    stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round;
}

/* ═══════════════════════════════════════════
   3.15 — Page-specific: Feature cards
   ═══════════════════════════════════════════ */
.feature-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: var(--sp-5); margin: var(--sp-6) 0;
}
.feature-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--r-xl); padding: var(--sp-6);
    text-align: center; transition: var(--ease-base);
    animation: fadeInUp 0.5s ease-out both;
}
.feature-card:nth-child(1) { animation-delay: 0.05s; }
.feature-card:nth-child(2) { animation-delay: 0.15s; }
.feature-card:nth-child(3) { animation-delay: 0.25s; }
.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-color: var(--accent-border);
}
.fc-icon {
    width: 52px; height: 52px; border-radius: var(--r-lg);
    display: inline-grid; place-items: center;
    font-size: 1.4rem; margin-bottom: var(--sp-4);
}
.fc-icon-blue  { background: var(--accent-light); color: var(--accent); }
.fc-icon-green { background: var(--success-bg);   color: var(--success); }
.fc-icon-navy  { background: #E8EDF5;             color: var(--navy); }
.fc-title {
    font-size: 1rem; font-weight: 700; color: var(--text-1);
    margin: 0 0 var(--sp-2) 0;
}
.fc-desc {
    font-size: 0.84rem; color: var(--text-2);
    line-height: 1.6; margin: 0;
}

/* ═══════════════════════════════════════════
   3.16 — Steps (How it works)
   ═══════════════════════════════════════════ */
.steps-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: var(--sp-5); margin: var(--sp-5) 0;
    counter-reset: step-counter;
}
.step-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--r-lg); padding: var(--sp-6) var(--sp-5);
    position: relative; text-align: center;
    transition: var(--ease-base); animation: fadeInUp 0.5s ease-out both;
}
.step-card:nth-child(1) { animation-delay: 0.1s; }
.step-card:nth-child(2) { animation-delay: 0.2s; }
.step-card:nth-child(3) { animation-delay: 0.3s; }
.step-card:hover {
    border-color: var(--accent-border);
    box-shadow: var(--shadow-md);
}
.step-num {
    width: 36px; height: 36px; border-radius: 50%;
    background: var(--navy); color: var(--text-on-navy);
    display: inline-grid; place-items: center;
    font-size: 0.88rem; font-weight: 700;
    margin-bottom: var(--sp-3);
}
.step-title {
    font-size: 0.95rem; font-weight: 600; color: var(--text-1);
    margin: 0 0 var(--sp-2) 0;
}
.step-desc { font-size: 0.82rem; color: var(--text-2); margin: 0; line-height: 1.55; }

/* ═══════════════════════════════════════════
   3.17 — CTA section
   ═══════════════════════════════════════════ */
.cta-section {
    text-align: center; padding: var(--sp-10) var(--sp-6);
    background: var(--navy); border-radius: var(--r-xl);
    margin: var(--sp-8) 0; animation: fadeInUp 0.5s ease-out both;
}
.cta-section h2 {
    font-size: 1.5rem; font-weight: 700; color: var(--text-on-navy);
    margin: 0 0 var(--sp-3) 0;
}
.cta-section p {
    font-size: 0.92rem; color: rgba(255,255,255,0.65);
    margin: 0 0 var(--sp-6) 0; line-height: 1.6;
}

/* ═══════════════════════════════════════════
   3.18 — Stats grid (About page)
   ═══════════════════════════════════════════ */
.stat-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: var(--sp-4); margin: var(--sp-6) 0;
}
.stat-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--r-lg); padding: var(--sp-6);
    text-align: center; transition: var(--ease-base);
    animation: fadeInUp 0.5s ease-out both;
}
.stat-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); border-color: var(--accent-border); }
.stat-num {
    font-size: 2rem; font-weight: 700; color: var(--navy);
    margin: 0 0 4px 0; line-height: 1;
}
.stat-label {
    font-size: 0.8rem; color: var(--text-2); margin: 0;
    font-weight: 500;
}

/* ═══════════════════════════════════════════
   3.19 — Timeline (About page)
   ═══════════════════════════════════════════ */
.timeline {
    position: relative; padding-left: 28px;
    margin: var(--sp-6) 0;
}
.timeline::before {
    content: ''; position: absolute; left: 8px; top: 4px; bottom: 4px;
    width: 2px; background: var(--border); border-radius: var(--r-full);
}
.tl-item {
    position: relative; padding: 0 0 var(--sp-6) var(--sp-5);
    animation: fadeInUp 0.4s ease-out both;
}
.tl-item:last-child { padding-bottom: 0; }
.tl-dot {
    position: absolute; left: -24px; top: 4px;
    width: 12px; height: 12px; border-radius: 50%;
    background: var(--accent); border: 2px solid var(--bg-page);
    box-shadow: 0 0 0 3px var(--accent-ring);
}
.tl-date {
    font-size: 0.72rem; font-weight: 600; color: var(--accent);
    text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 2px 0;
}
.tl-title { font-size: 0.9rem; font-weight: 600; color: var(--text-1); margin: 0 0 2px 0; }
.tl-desc { font-size: 0.8rem; color: var(--text-2); margin: 0; line-height: 1.5; }

/* ═══════════════════════════════════════════
   3.20 — Why card
   ═══════════════════════════════════════════ */
.why-card {
    background: linear-gradient(135deg, var(--navy), var(--navy-light));
    border-radius: var(--r-xl); padding: var(--sp-8);
    margin: var(--sp-6) 0;
    animation: fadeInUp 0.5s ease-out both;
}
.why-card h3 { font-size: 1.15rem; font-weight: 700; color: var(--text-on-navy); margin: 0 0 var(--sp-4) 0; }
.why-list { list-style: none; padding: 0; margin: 0; }
.why-list li {
    font-size: 0.86rem; color: rgba(255,255,255,0.8);
    padding: 8px 0; display: flex; align-items: center; gap: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.why-list li:last-child { border-bottom: none; }
.why-list li::before {
    content: '✦'; color: var(--accent); font-size: 0.75rem; flex-shrink: 0;
}

/* ═══════════════════════════════════════════
   3.21 — Format cards (Content page)
   ═══════════════════════════════════════════ */
.format-grid {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: var(--sp-4); margin: var(--sp-5) 0;
}
.format-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--r-lg); padding: var(--sp-5);
    transition: var(--ease-base); animation: fadeInUp 0.45s ease-out both;
}
.format-card:nth-child(1) { animation-delay: 0.05s; }
.format-card:nth-child(2) { animation-delay: 0.1s; }
.format-card:nth-child(3) { animation-delay: 0.15s; }
.format-card:nth-child(4) { animation-delay: 0.2s; }
.format-card:hover {
    border-color: var(--accent-border);
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}
.fmt-header { display: flex; align-items: center; gap: var(--sp-3); margin-bottom: var(--sp-2); }
.fmt-icon {
    width: 38px; height: 38px; border-radius: var(--r-md);
    background: var(--accent-light); display: grid; place-items: center;
    font-size: 1.05rem; flex-shrink: 0;
}
.fmt-title { font-size: 0.92rem; font-weight: 700; color: var(--text-1); margin: 0; }
.fmt-badge {
    font-size: 0.6rem; font-weight: 600; color: var(--accent);
    background: var(--accent-light); padding: 2px 8px;
    border-radius: var(--r-full); margin-left: 6px; text-transform: uppercase;
}
.fmt-desc { font-size: 0.82rem; color: var(--text-2); margin: 0; line-height: 1.55; }

/* Demo block */
.demo-block {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--r-xl); overflow: hidden;
    margin: var(--sp-6) 0; animation: fadeInUp 0.5s ease-out both;
}
.demo-header {
    background: var(--navy); padding: var(--sp-4) var(--sp-5);
    display: flex; align-items: center; gap: 8px;
}
.demo-dot { width: 8px; height: 8px; border-radius: 50%; }
.demo-dot-r { background: #ef4444; }
.demo-dot-y { background: #eab308; }
.demo-dot-g { background: #22c55e; }
.demo-body { padding: var(--sp-5); }
.demo-label {
    font-size: 0.7rem; font-weight: 600; color: var(--text-3);
    text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 var(--sp-2) 0;
}
.demo-text {
    font-size: 0.84rem; color: var(--text-1); line-height: 1.7;
    margin: 0; padding: var(--sp-3); background: var(--bg-subtle);
    border-radius: var(--r-sm); border: 1px solid var(--border);
}

/* Use-case cards */
.usecase-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: var(--sp-4); margin: var(--sp-5) 0;
}
.usecase-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--r-lg); padding: var(--sp-5);
    text-align: center; transition: var(--ease-base);
    animation: fadeInUp 0.5s ease-out both;
}
.usecase-card:hover {
    transform: translateY(-3px); box-shadow: var(--shadow-md);
    border-color: var(--accent-border);
}
.uc-icon {
    font-size: 1.8rem; margin-bottom: var(--sp-3);
}
.uc-title { font-size: 0.95rem; font-weight: 700; color: var(--text-1); margin: 0 0 var(--sp-2) 0; }
.uc-desc { font-size: 0.8rem; color: var(--text-2); margin: 0; line-height: 1.55; }

/* ═══════════════════════════════════════════
   3.22 — Others page: FAQ, Roadmap, Contact, Legal
   ═══════════════════════════════════════════ */
.roadmap-grid {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: var(--sp-4); margin: var(--sp-5) 0;
}
.roadmap-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--r-lg); padding: var(--sp-5);
    transition: var(--ease-base); animation: fadeInUp 0.45s ease-out both;
}
.roadmap-card:hover { border-color: var(--accent-border); box-shadow: var(--shadow-sm); }
.rm-header { display: flex; align-items: center; gap: var(--sp-2); margin-bottom: var(--sp-2); }
.rm-badge {
    font-size: 0.6rem; font-weight: 700; padding: 2px 10px;
    border-radius: var(--r-full); text-transform: uppercase; letter-spacing: 0.4px;
}
.rm-soon { background: #FEF3C7; color: #92400E; }
.rm-planned { background: var(--accent-light); color: var(--navy); }
.rm-title { font-size: 0.9rem; font-weight: 600; color: var(--text-1); margin: 0; }
.rm-desc { font-size: 0.8rem; color: var(--text-2); margin: var(--sp-1) 0 0 0; line-height: 1.5; }

.contact-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--r-xl); padding: var(--sp-8);
    text-align: center; animation: fadeInUp 0.5s ease-out both;
}
.contact-card h3 { font-size: 1.1rem; font-weight: 700; color: var(--text-1); margin: 0 0 var(--sp-2) 0; }
.contact-card p { font-size: 0.86rem; color: var(--text-2); margin: 0 0 var(--sp-4) 0; line-height: 1.6; }
.contact-email {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 10px 24px; background: var(--accent-light);
    border-radius: var(--r-full); font-size: 0.88rem;
    font-weight: 600; color: var(--navy);
}

.legal-grid {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: var(--sp-4); margin: var(--sp-5) 0;
}
.legal-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--r-lg); padding: var(--sp-5);
    animation: fadeInUp 0.45s ease-out both;
}
.legal-card h4 { font-size: 0.92rem; font-weight: 700; color: var(--text-1); margin: 0 0 var(--sp-2) 0; }
.legal-card p { font-size: 0.8rem; color: var(--text-2); margin: 0; line-height: 1.6; }

/* ═══════════════════════════════════════════
   3.23 — Page titles
   ═══════════════════════════════════════════ */
.page-header {
    text-align: center; padding: var(--sp-8) 0 var(--sp-6) 0;
    animation: fadeInUp 0.45s ease-out;
}
.page-header h1 {
    font-size: 1.8rem; font-weight: 700; color: var(--text-1);
    margin: 0 0 var(--sp-2) 0; letter-spacing: -0.6px;
}
.page-header p {
    font-size: 0.95rem; color: var(--text-2); margin: 0 auto;
    max-width: 500px; line-height: 1.6;
}

/* ═══════════════════════════════════════════
   3.24 — Nav button row  (hidden — functional only)
   ═══════════════════════════════════════════ */
/* Primary hide rule: targets the stHorizontalBlock right after #nav-btn-marker */
div.stMarkdown:has(#nav-btn-marker) + div[data-testid="stHorizontalBlock"] {
    display: none !important;
    height: 0 !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* ═══════════════════════════════════════════
   3.25 — Responsive
   ═══════════════════════════════════════════ */
@media (max-width: 768px) {
    .navbar { flex-wrap: wrap; gap: var(--sp-3); justify-content: center; padding: var(--sp-3) var(--sp-4); }
    .nav-center { display: none; }
    .hero h1 { font-size: 1.6rem; }
    .metrics-grid { grid-template-columns: repeat(2, 1fr); }
    .trust-row { flex-direction: column; gap: var(--sp-3); }
    .pricing-grid { grid-template-columns: 1fr; }
    .fab-next { right: 16px; bottom: 20px; width: 46px; height: 46px; }
    .feature-grid { grid-template-columns: 1fr; }
    .steps-grid { grid-template-columns: 1fr; }
    .stat-grid { grid-template-columns: 1fr; }
    .format-grid { grid-template-columns: 1fr; }
    .usecase-grid { grid-template-columns: 1fr; }
    .roadmap-grid { grid-template-columns: 1fr; }
    .legal-grid { grid-template-columns: 1fr; }
    .page-header h1 { font-size: 1.4rem; }
}
</style>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════╗
# ║  4. SESSION STATE                                           ║
# ╚══════════════════════════════════════════════════════════════╝

_DEFAULTS = {
    "summary_result":     None,
    "summary_input":      "",
    "summary_style_used": "",
    "ocr_text":           "",
    "history":            [],
    "show_pricing":       False,
    "active_page":        "HOME",
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ╔══════════════════════════════════════════════════════════════╗
# ║  5. UTILITY / LLM FUNCTIONS                                 ║
# ╚══════════════════════════════════════════════════════════════╝

def check_server() -> bool:
    try:
        return requests.get("http://127.0.0.1:8080/", timeout=3).status_code == 200
    except Exception:
        return False

def count_words(t: str) -> int:
    return len(t.split()) if t else 0

def count_chars(t: str) -> int:
    return len(t) if t else 0

def estimate_tokens(t: str) -> int:
    return int(count_words(t) * 1.33)

def build_system_prompt(style: str, language: str, extra: str) -> str:
    if style == "OCR Clean + Summarize":
        prompt = (
            "You are an expert AI assistant.\n\n"
            "The following text was extracted via OCR from an image. "
            "It may contain spelling errors, broken words, or formatting issues.\n\n"
            "Your tasks:\n"
            "1. Correct obvious OCR errors.\n"
            "2. Remove noise and duplicated fragments.\n"
            "3. Preserve important names, numbers, and dates.\n"
            "4. Provide a clear, structured summary.\n\n"
            "Base your summary strictly on the cleaned text."
        )
    else:
        styles = {
            "Concise":       "Produce a short, concise summary capturing only the key points.",
            "Detailed":      "Produce a thorough summary preserving important nuances.",
            "Bullet Points": "Produce a clear, well-organized bullet-point summary.",
            "Academic":      "Produce a formal, academic-style summary suitable for scholarly work.",
            "ELI5":          "Explain the text simply, as if for a five-year-old.",
        }
        prompt = f"You are an expert text summarizer.\n{styles.get(style, styles['Concise'])}"
    if language != "Auto (same as input)":
        prompt += f"\nWrite the summary in {language}."
    if extra and extra.strip():
        prompt += f"\nAdditional instructions: {extra.strip()}"
    return prompt

def call_llm(text, system_prompt, temperature, max_tokens):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": f"Summarize the following text:\n\n{text}"},
        ],
        "temperature": temperature,
        "max_tokens":  max_tokens,
        "stream":      False,
    }
    t0 = time.time()
    resp = requests.post(API_URL, json=payload, timeout=600)
    elapsed = time.time() - t0
    resp.raise_for_status()
    data = resp.json()
    usage = data.get("usage", {})
    return {
        "summary":           data["choices"][0]["message"]["content"],
        "elapsed":           elapsed,
        "prompt_tokens":     usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
        "total_tokens":      usage.get("total_tokens", 0),
    }


# ╔══════════════════════════════════════════════════════════════╗
# ║  6. UI COMPONENTS (shared)                                  ║
# ╚══════════════════════════════════════════════════════════════╝

def render_counters(text: str):
    w, c, t = count_words(text), count_chars(text), estimate_tokens(text)
    st.markdown(f"""
    <div class="counter-row">
        <span class="ctr-pill"><span class="ctr-val">{w:,}</span> words</span>
        <span class="ctr-pill"><span class="ctr-val">{c:,}</span> chars</span>
        <span class="ctr-pill">≈ <span class="ctr-val">{t:,}</span> tokens</span>
    </div>""", unsafe_allow_html=True)

def render_empty():
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="1.5"
                 stroke-linecap="round" stroke-linejoin="round">
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12
                         a2 2 0 0 0 2-2V7.5L14.5 2z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <line x1="10" y1="9" x2="8" y2="9"/>
            </svg>
        </div>
        <p class="empty-title">No summary yet</p>
        <p class="empty-desc">
            Paste text, upload a file, or extract from an image
            — then click <strong>Summarize</strong>.
        </p>
    </div>""", unsafe_allow_html=True)

def render_metrics(result, input_text):
    orig = count_words(input_text)
    summ = count_words(result["summary"])
    comp = round(summ / orig * 100, 1) if orig else 0
    st.markdown(f"""
    <div class="metrics-grid">
        <div class="m-card"><p class="m-val">{result['elapsed']:.1f}s</p><p class="m-lbl">Latency</p></div>
        <div class="m-card"><p class="m-val">{result['prompt_tokens']:,}</p><p class="m-lbl">Input Tokens</p></div>
        <div class="m-card"><p class="m-val">{result['completion_tokens']:,}</p><p class="m-lbl">Output Tokens</p></div>
        <div class="m-card"><p class="m-val">{comp}%</p><p class="m-lbl">Compression</p></div>
    </div>""", unsafe_allow_html=True)

def render_output(result, input_text):
    render_metrics(result, input_text)
    safe = html_lib.escape(result["summary"]).replace("\n", "<br>")
    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">✦ AI-Generated Summary</div>
        <div class="result-body">{safe}</div>
    </div>""", unsafe_allow_html=True)
    with st.expander("📋  Copy summary"):
        st.code(result["summary"], language=None)
    with st.expander("🔍  Compare original vs summary"):
        c1, c2 = st.columns(2)
        with c1:
            st.caption(f"Original — {count_words(input_text):,} words")
            st.text_area("_o", input_text[:5000], height=180,
                         disabled=True, label_visibility="collapsed")
        with c2:
            st.caption(f"Summary — {count_words(result['summary']):,} words")
            st.text_area("_s", result["summary"], height=180,
                         disabled=True, label_visibility="collapsed")

def do_summarize(text, server_ok, style, lang, extra, temp, max_tok):
    if not text or not text.strip():
        st.warning("Please enter some text to summarize.")
        return
    if not server_ok:
        st.error("Server offline — start llama.cpp at 127.0.0.1:8080.")
        return
    system = build_system_prompt(style, lang, extra)
    bar = st.progress(0, text="Preparing request…")
    for p in range(0, 25, 5):
        time.sleep(0.02); bar.progress(p, text="Preparing request…")
    bar.progress(25, text="Generating summary…")
    try:
        result = call_llm(text, system, temp, max_tok)
    except requests.exceptions.Timeout:
        bar.empty(); st.error("Timed out — try shorter text or check the server."); return
    except requests.exceptions.ConnectionError:
        bar.empty(); st.error("Cannot connect — make sure llama.cpp is running."); return
    except Exception as e:
        bar.empty(); st.error(f"Error: {e}"); return
    for p in range(25, 101, 10):
        time.sleep(0.012); bar.progress(min(p, 100), text="Finalizing…")
    bar.empty()
    st.session_state.summary_result     = result
    st.session_state.summary_input      = text
    st.session_state.summary_style_used = style
    st.session_state.history.append({
        "style": style,
        "preview": (text[:80] + "…") if len(text) > 80 else text,
        "summary": result["summary"],
        "time": result["elapsed"],
        "tokens": result["total_tokens"],
    })
    st.rerun()


# ╔══════════════════════════════════════════════════════════════╗
# ║  7. PAGE RENDERERS                                          ║
# ╚══════════════════════════════════════════════════════════════╝

# ────────────────────────── HOME ──────────────────────────────

def render_home(server_ok, summary_style, language, extra_instructions,
                temperature, max_tokens):
    """HOME page: Hero + Features + How-it-works + CTA + Summarizer + History."""

    # ── Hero ──
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">✦ AI-Powered Summarization</div>
        <h1>Summarize any text in seconds</h1>
        <p>
            Paste an article, upload a document, or extract text from an image
            — get a clean, intelligent summary powered by your local LLM.
        </p>
        <div class="trust-row">
            <span class="trust-item">🔒 100% Private</span>
            <span class="trust-item">⚡ Runs Locally</span>
            <span class="trust-item">🌐 Offline-Ready</span>
            <span class="trust-item">📷 OCR Built-in</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Feature cards ──
    st.markdown("""
    <div class="sec-head"><h3>Why SummarizeAI?</h3><div class="sec-head-line"></div></div>
    <div class="feature-grid">
        <div class="feature-card">
            <div class="fc-icon fc-icon-blue">⚡</div>
            <p class="fc-title">Fast Summary</p>
            <p class="fc-desc">
                Get concise, accurate summaries in seconds.
                Multiple styles — bullet points, executive, academic, ELI5.
            </p>
        </div>
        <div class="feature-card">
            <div class="fc-icon fc-icon-green">📷</div>
            <p class="fc-title">Smart OCR</p>
            <p class="fc-desc">
                Upload an image and extract text automatically with EasyOCR.
                Clean, correct, and summarize — all in one step.
            </p>
        </div>
        <div class="feature-card">
            <div class="fc-icon fc-icon-navy">🔒</div>
            <p class="fc-title">Secure & Private</p>
            <p class="fc-desc">
                Everything runs on your machine. No data leaves your network.
                No cloud dependency — full offline capable.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── How it works ──
    st.markdown("""
    <div class="sec-head"><h3>How It Works</h3><div class="sec-head-line"></div></div>
    <div class="steps-grid">
        <div class="step-card">
            <div class="step-num">1</div>
            <p class="step-title">Input Your Text</p>
            <p class="step-desc">Paste text, upload a .txt / .md file, or capture text from an image using OCR.</p>
        </div>
        <div class="step-card">
            <div class="step-num">2</div>
            <p class="step-title">Choose Your Style</p>
            <p class="step-desc">Select concise, detailed, bullets, academic, or ELI5 — then fine-tune temperature and tokens.</p>
        </div>
        <div class="step-card">
            <div class="step-num">3</div>
            <p class="step-title">Get Your Summary</p>
            <p class="step-desc">The AI processes your text locally and delivers a clean summary with performance metrics.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA ──
    st.markdown("""
    <div class="cta-section">
        <h2>Ready to summarize?</h2>
        <p>Scroll down to the editor, paste your content, and let the AI do the rest.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Summarizer: Two-Column Layout ──
    st.markdown("""
    <div class="sec-head"><h3>Summarizer</h3><div class="sec-head-line"></div></div>
    """, unsafe_allow_html=True)

    col_in, col_out = st.columns([11, 9], gap="large")

    with col_in:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)

        tab_paste, tab_file, tab_image = st.tabs([
            "Paste Text", "Upload File", "Image OCR",
        ])

        with tab_paste:
            st.markdown("""
            <div class="inner-card"><div class="ic-header">
                <div class="ic-icon">📋</div>
                <div><p class="ic-title">Paste Your Text</p>
                <p class="ic-desc">Article, report, or document — the AI will summarize it.</p></div>
            </div></div>""", unsafe_allow_html=True)
            paste_text = st.text_area(
                "Text input", height=280,
                placeholder="Paste the text you want to summarize…",
                key="paste_input", label_visibility="collapsed",
            )
            if paste_text:
                render_counters(paste_text)
            if st.button("Summarize", key="btn_paste", use_container_width=True):
                do_summarize(paste_text, server_ok, summary_style,
                             language, extra_instructions, temperature, max_tokens)

        with tab_file:
            st.markdown("""
            <div class="inner-card"><div class="ic-header">
                <div class="ic-icon">📄</div>
                <div><p class="ic-title">Upload a Text File</p>
                <p class="ic-desc">Supports .txt and .md files.</p></div>
            </div></div>""", unsafe_allow_html=True)
            uploaded = st.file_uploader(
                "Upload file", type=["txt", "md"],
                key="file_upload", label_visibility="collapsed",
            )
            file_text = ""
            if uploaded is not None:
                file_text = uploaded.read().decode("utf-8", errors="replace")
                st.text_area("Preview", file_text[:3000], height=180,
                             disabled=True, label_visibility="collapsed")
                render_counters(file_text)
            if st.button("Summarize", key="btn_file", use_container_width=True):
                do_summarize(file_text, server_ok, summary_style,
                             language, extra_instructions, temperature, max_tokens)

        with tab_image:
            st.markdown("""
            <div class="inner-card"><div class="ic-header">
                <div class="ic-icon">📷</div>
                <div><p class="ic-title">Image to Text (OCR)</p>
                <p class="ic-desc">Upload a photo → extract → edit → summarize.</p></div>
            </div></div>""", unsafe_allow_html=True)
            image_file = st.file_uploader(
                "Upload image",
                type=["jpg", "jpeg", "png", "webp", "bmp", "tiff"],
                key="img_upload", label_visibility="collapsed",
            )
            if image_file is not None:
                st.image(image_file, caption="Uploaded image", use_container_width=True)
                if st.button("Extract Text (OCR)", key="btn_ocr", use_container_width=True):
                    bar = st.progress(0, text="Starting OCR engine…")
                    for p in range(0, 30, 5):
                        time.sleep(0.03); bar.progress(p, text="Starting OCR engine…")
                    bar.progress(30, text="Extracting text…")
                    try:
                        extracted = extract_text_from_image(image_file.getvalue())
                    except OCRError as e:
                        bar.empty(); st.error(f"OCR Error: {e}"); extracted = ""
                    except Exception as e:
                        bar.empty(); st.error(f"Error: {e}"); extracted = ""
                    for p in range(30, 101, 10):
                        time.sleep(0.012); bar.progress(min(p, 100), text="Complete!")
                    bar.empty()
                    if extracted and extracted.strip():
                        st.session_state.ocr_text = extracted
                        st.success(f"Extracted {count_words(extracted):,} words")
                    else:
                        st.session_state.ocr_text = ""
                        st.warning("No text detected — image may be blurry or empty.")

            if st.session_state.ocr_text:
                st.markdown("""
                <div class="sec-head"><h3>Extracted Text</h3>
                <div class="sec-head-line"></div></div>""", unsafe_allow_html=True)
                ocr_edit = st.text_area(
                    "Extracted text (editable)",
                    value=st.session_state.ocr_text, height=220,
                    key="ocr_editor", label_visibility="collapsed",
                )
                render_counters(ocr_edit)
                if summary_style != "OCR Clean + Summarize":
                    st.info("**Tip:** Select *OCR Clean + Summarize* in the sidebar for best results with OCR text.")
                if st.button("Summarize", key="btn_ocr_sum", use_container_width=True):
                    do_summarize(ocr_edit, server_ok, summary_style,
                                 language, extra_instructions, temperature, max_tokens)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Right column — Output ──
    with col_out:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<div class="sec-head"><h3>Output</h3><div class="sec-head-line"></div></div>',
                    unsafe_allow_html=True)
        if st.session_state.summary_result is not None:
            render_output(st.session_state.summary_result, st.session_state.summary_input)
        else:
            render_empty()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Session History ──
    if st.session_state.history:
        st.markdown("""
        <div class="sec-head" style="margin-top:48px">
            <h3>Session History</h3><div class="sec-head-line"></div>
        </div>""", unsafe_allow_html=True)
        for i, h in enumerate(reversed(st.session_state.history), 1):
            with st.expander(f"#{i}  ·  {h['style']}  ·  {h['time']:.1f}s  ·  {h['tokens']:,} tokens"):
                st.caption(f"Input: {h['preview']}")
                st.markdown(h["summary"])
                st.code(h["summary"], language=None)


# ────────────────────────── ABOUT ─────────────────────────────

def render_about():
    """ABOUT page: Platform overview, mission, stats, timeline, why choose us."""

    st.markdown("""
    <div class="page-header">
        <h1>About SummarizeAI</h1>
        <p>An intelligent, privacy-first text summarization platform built for professionals, students, and researchers.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Mission / Vision ──
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("""
        <div class="ic-header">
            <div class="ic-icon">🎯</div>
            <div><p class="ic-title">Our Mission</p></div>
        </div>""", unsafe_allow_html=True)
        st.markdown(
            "We believe everyone deserves access to powerful AI tools "
            "**without sacrificing privacy**. SummarizeAI runs entirely on your machine "
            "— no data ever leaves your network. Our mission is to make text comprehension "
            "faster, smarter, and more accessible."
        )
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("""
        <div class="ic-header">
            <div class="ic-icon">🔭</div>
            <div><p class="ic-title">Our Vision</p></div>
        </div>""", unsafe_allow_html=True)
        st.markdown(
            "A world where **AI augments human understanding** rather than replacing it. "
            "We envision a suite of local-first AI tools that professionals trust "
            "for daily workflows — from document analysis to knowledge management "
            "and beyond."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Stats ──
    st.markdown("""
    <div class="sec-head"><h3>By the Numbers</h3><div class="sec-head-line"></div></div>
    <div class="stat-grid">
        <div class="stat-card">
            <p class="stat-num">10K+</p>
            <p class="stat-label">Summaries Generated</p>
        </div>
        <div class="stat-card">
            <p class="stat-num">99%</p>
            <p class="stat-label">Accuracy Rate</p>
        </div>
        <div class="stat-card">
            <p class="stat-num">100%</p>
            <p class="stat-label">Offline Ready</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Timeline ──
    st.markdown("""
    <div class="sec-head"><h3>Development Timeline</h3><div class="sec-head-line"></div></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="timeline">
        <div class="tl-item">
            <div class="tl-dot"></div>
            <p class="tl-date">Jan 2026</p>
            <p class="tl-title">Project Inception</p>
            <p class="tl-desc">Initial idea — build a 100% local AI summarizer using llama.cpp and Streamlit.</p>
        </div>
        <div class="tl-item">
            <div class="tl-dot"></div>
            <p class="tl-date">Jan 2026</p>
            <p class="tl-title">Core Engine</p>
            <p class="tl-desc">LLM integration, multi-style summarization, and sidebar settings panel.</p>
        </div>
        <div class="tl-item">
            <div class="tl-dot"></div>
            <p class="tl-date">Feb 2026</p>
            <p class="tl-title">OCR Module</p>
            <p class="tl-desc">EasyOCR-based image-to-text extraction with automatic noise correction.</p>
        </div>
        <div class="tl-item">
            <div class="tl-dot"></div>
            <p class="tl-date">Feb 2026</p>
            <p class="tl-title">Premium Redesign</p>
            <p class="tl-desc">Navy palette, multi-page navigation, pricing modal, and responsive design.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Why choose us ──
    st.markdown("""
    <div class="why-card">
        <h3>Why Choose SummarizeAI?</h3>
        <ul class="why-list">
            <li>Zero cloud dependency — your data stays on your machine</li>
            <li>Multiple summary styles for every use-case</li>
            <li>Built-in OCR that cleans and corrects noisy text</li>
            <li>Lightning-fast local inference with llama.cpp</li>
            <li>Open architecture — easy to extend and customize</li>
            <li>Beautiful, responsive UI built with Streamlit</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ────────────────────────── CONTENT ───────────────────────────

def render_content():
    """CONTENT page: Formats, demo, use-cases."""

    st.markdown("""
    <div class="page-header">
        <h1>Content & Formats</h1>
        <p>Discover all the summary formats and features available in SummarizeAI.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Available formats ──
    st.markdown("""
    <div class="sec-head"><h3>Output Formats</h3><div class="sec-head-line"></div></div>
    <div class="format-grid">
        <div class="format-card">
            <div class="fmt-header">
                <div class="fmt-icon">📝</div>
                <p class="fmt-title">Bullet Summary</p>
            </div>
            <p class="fmt-desc">Clean, organized bullet points highlighting the key ideas. Perfect for quick review and note-taking.</p>
        </div>
        <div class="format-card">
            <div class="fmt-header">
                <div class="fmt-icon">📊</div>
                <p class="fmt-title">Executive Summary<span class="fmt-badge">Popular</span></p>
            </div>
            <p class="fmt-desc">A concise, professional summary suitable for decision-makers. Captures main conclusions and recommendations.</p>
        </div>
        <div class="format-card">
            <div class="fmt-header">
                <div class="fmt-icon">🗂️</div>
                <p class="fmt-title">Flashcards</p>
                <span class="fmt-badge">Coming Soon</span>
            </div>
            <p class="fmt-desc">Automatically generate question/answer flashcards from any text — ideal for studying and knowledge retention.</p>
        </div>
        <div class="format-card">
            <div class="fmt-header">
                <div class="fmt-icon">❓</div>
                <p class="fmt-title">Quiz Generator</p>
                <span class="fmt-badge">Coming Soon</span>
            </div>
            <p class="fmt-desc">Create multiple-choice quizzes based on your content. Great for teachers, trainers, and self-assessment.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Demo section ──
    st.markdown("""
    <div class="sec-head"><h3>Live Demo</h3><div class="sec-head-line"></div></div>
    <div class="demo-block">
        <div class="demo-header">
            <span class="demo-dot demo-dot-r"></span>
            <span class="demo-dot demo-dot-y"></span>
            <span class="demo-dot demo-dot-g"></span>
        </div>
        <div class="demo-body">
            <p class="demo-label">📥 Original Text</p>
            <p class="demo-text">
                Artificial intelligence (AI) has rapidly transformed industries worldwide.
                From healthcare diagnostics to autonomous vehicles, AI systems are becoming
                integral to everyday operations. Machine learning models now process vast
                datasets, enabling breakthroughs in drug discovery, climate modeling, and
                natural language understanding. However, concerns about data privacy, bias
                in algorithms, and the environmental cost of training large models continue
                to shape the public debate around AI adoption.
            </p>
            <br>
            <p class="demo-label">📤 AI Summary (Concise)</p>
            <p class="demo-text" style="border-left: 3px solid var(--accent);">
                AI is transforming industries like healthcare and transportation through
                machine learning breakthroughs. While enabling advances in drug discovery
                and climate science, it raises ongoing concerns about privacy, algorithmic
                bias, and environmental impact.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Interactive placeholder buttons ──
    st.markdown("""
    <div class="sec-head"><h3>Try a Format</h3><div class="sec-head-line"></div></div>
    """, unsafe_allow_html=True)
    bc1, bc2, bc3, bc4 = st.columns(4)
    with bc1:
        if st.button("📝 Bullet Points", key="try_bullet", use_container_width=True):
            st.toast("Switch to HOME tab, select 'Bullet Points' style, and paste your text!", icon="💡")
    with bc2:
        if st.button("📊 Executive", key="try_exec", use_container_width=True):
            st.toast("Switch to HOME tab, select 'Detailed' for an executive summary!", icon="💡")
    with bc3:
        if st.button("🗂️ Flashcards", key="try_flash", use_container_width=True):
            st.toast("Flashcards feature coming soon — stay tuned!", icon="🔜")
    with bc4:
        if st.button("❓ Quiz", key="try_quiz", use_container_width=True):
            st.toast("Quiz generator feature coming soon — stay tuned!", icon="🔜")

    # ── Use-cases ──
    st.markdown("""
    <div class="sec-head"><h3>Use Cases</h3><div class="sec-head-line"></div></div>
    <div class="usecase-grid">
        <div class="usecase-card">
            <div class="uc-icon">🎓</div>
            <p class="uc-title">Students</p>
            <p class="uc-desc">Summarize lectures, research papers, and textbooks. Generate study notes in seconds instead of hours.</p>
        </div>
        <div class="usecase-card">
            <div class="uc-icon">💼</div>
            <p class="uc-title">Business</p>
            <p class="uc-desc">Condense reports, meeting notes, and market research. Share concise briefs with your team.</p>
        </div>
        <div class="usecase-card">
            <div class="uc-icon">🔬</div>
            <p class="uc-title">Researchers</p>
            <p class="uc-desc">Quickly digest academic papers, extract key findings, and build literature reviews faster.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ────────────────────────── OTHERS ────────────────────────────

def render_others():
    """OTHERS page: FAQ, Roadmap, Support, Legal."""

    st.markdown("""
    <div class="page-header">
        <h1>More Information</h1>
        <p>Frequently asked questions, upcoming features, support, and legal notices.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── FAQ ──
    st.markdown("""
    <div class="sec-head"><h3>Frequently Asked Questions</h3><div class="sec-head-line"></div></div>
    """, unsafe_allow_html=True)

    with st.expander("What AI model does SummarizeAI use?"):
        st.markdown(
            "SummarizeAI uses a **local Mistral model** served through **llama.cpp**. "
            "The model runs entirely on your machine — no cloud API calls, no data sent externally. "
            "You can swap the model for any GGUF-format model compatible with llama.cpp."
        )
    with st.expander("Is my data sent to any server?"):
        st.markdown(
            "**No.** All processing happens locally at `127.0.0.1:8080`. "
            "Your text never leaves your computer. This makes SummarizeAI ideal for "
            "sensitive documents, legal texts, and confidential business data."
        )
    with st.expander("What file formats are supported?"):
        st.markdown(
            "Currently: **plain text** (.txt), **Markdown** (.md), and **images** "
            "(JPG, PNG, WebP, BMP, TIFF) via OCR. PDF and DOCX support are on the roadmap."
        )
    with st.expander("How does OCR work?"):
        st.markdown(
            "We use **EasyOCR** — an open-source, pure-Python OCR engine. "
            "It supports English and French out of the box. Images are automatically "
            "preprocessed (resized, converted to grayscale, sharpened) for optimal accuracy."
        )
    with st.expander("Can I change the summary language?"):
        st.markdown(
            "Yes! Use the **Output Language** selector in the sidebar to get summaries in "
            "English, French, Spanish, German, Arabic, Chinese, or Japanese — "
            "regardless of the input language."
        )
    with st.expander("What are the system requirements?"):
        st.markdown(
            "- **Python 3.10+** with Streamlit, requests, easyocr, Pillow\n"
            "- **llama.cpp** compiled and running with a GGUF model\n"
            "- Minimum **8 GB RAM** recommended (16 GB for larger models)\n"
            "- Works on Windows, macOS, and Linux"
        )

    # ── Roadmap ──
    st.markdown("""
    <div class="sec-head"><h3>Roadmap</h3><div class="sec-head-line"></div></div>
    <div class="roadmap-grid">
        <div class="roadmap-card">
            <div class="rm-header">
                <span class="rm-badge rm-soon">Coming Soon</span>
            </div>
            <p class="rm-title">PDF & DOCX Support</p>
            <p class="rm-desc">Upload PDF and Word documents directly — automatic text extraction and summarization.</p>
        </div>
        <div class="roadmap-card">
            <div class="rm-header">
                <span class="rm-badge rm-soon">Coming Soon</span>
            </div>
            <p class="rm-title">Export to PDF / DOCX</p>
            <p class="rm-desc">Download your summaries as beautifully formatted PDF or Word documents.</p>
        </div>
        <div class="roadmap-card">
            <div class="rm-header">
                <span class="rm-badge rm-planned">Planned</span>
            </div>
            <p class="rm-title">Flashcard Generator</p>
            <p class="rm-desc">Automatically create Q&A flashcards from any summarized text for efficient studying.</p>
        </div>
        <div class="roadmap-card">
            <div class="rm-header">
                <span class="rm-badge rm-planned">Planned</span>
            </div>
            <p class="rm-title">Multi-Document Analysis</p>
            <p class="rm-desc">Compare and cross-reference multiple documents with a unified summary view.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Support / Contact ──
    st.markdown("""
    <div class="sec-head"><h3>Support & Contact</h3><div class="sec-head-line"></div></div>
    <div class="contact-card">
        <h3>Need Help?</h3>
        <p>Whether you have a question, found a bug, or want to suggest a feature — we'd love to hear from you.</p>
        <div class="contact-email">📧 support@summarizeai.local</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Legal ──
    st.markdown("""
    <div class="sec-head"><h3>Legal</h3><div class="sec-head-line"></div></div>
    <div class="legal-grid">
        <div class="legal-card">
            <h4>🔒 Privacy Policy</h4>
            <p>
                SummarizeAI processes all data locally on your machine. We do not collect,
                store, or transmit any user data. No analytics, no tracking cookies,
                no third-party services. Your content remains entirely private.
            </p>
        </div>
        <div class="legal-card">
            <h4>📜 Terms of Service</h4>
            <p>
                SummarizeAI is provided "as-is" for personal and professional use.
                AI-generated summaries should be reviewed for accuracy before use in
                critical applications. The software is open for modification under
                applicable licenses.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════╗
# ║  8. NAVBAR (dynamic pills)                                  ║
# ╚══════════════════════════════════════════════════════════════╝

_page = st.session_state.active_page
_pill = lambda name: "nav-pill active" if _page == name else "nav-pill"

st.markdown(f"""
<div class="navbar">
    <div class="nav-left">
        <div class="nav-logo">✦</div>
        <span class="nav-brand">SummarizeAI</span>
    </div>
    <div class="nav-center">
        <span class="{_pill('HOME')}">HOME</span>
        <span class="{_pill('ABOUT')}">ABOUT</span>
        <span class="{_pill('CONTENT')}">CONTENT</span>
        <span class="{_pill('OTHERS')}">OTHERS</span>
    </div>
    <div class="nav-right">
        <span class="nav-upgrade">✦ Upgrade Pro</span>
        <div class="nav-hamburger">
            <svg viewBox="0 0 24 24">
                <line x1="4" y1="6" x2="20" y2="6"/>
                <line x1="4" y1="12" x2="20" y2="12"/>
                <line x1="4" y1="18" x2="20" y2="18"/>
            </svg>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════╗
# ║  9. NAV BUTTONS (functional — visually hidden via CSS)      ║
# ╚══════════════════════════════════════════════════════════════╝

def _go(page):
    st.session_state.active_page = page

# Unique marker element — CSS uses :has() to find the NEXT sibling HorizontalBlock
st.markdown('<span id="nav-btn-marker" style="display:none"></span>', unsafe_allow_html=True)
_nav_cols = st.columns([1, 1, 1, 1, 2])
with _nav_cols[0]:
    if st.button("HOME", key="nav_home", use_container_width=True):
        _go("HOME"); st.rerun()
with _nav_cols[1]:
    if st.button("ABOUT", key="nav_about", use_container_width=True):
        _go("ABOUT"); st.rerun()
with _nav_cols[2]:
    if st.button("CONTENT", key="nav_content", use_container_width=True):
        _go("CONTENT"); st.rerun()
with _nav_cols[3]:
    if st.button("OTHERS", key="nav_others", use_container_width=True):
        _go("OTHERS"); st.rerun()
with _nav_cols[4]:
    if st.button("✦ Upgrade Pro", key="btn_open_pricing", use_container_width=True):
        st.session_state.show_pricing = True; st.rerun()

# CSS: hide the button row — targets the stHorizontalBlock right after our marker
st.markdown("""
<style>
/* Hide nav routing buttons — sibling HorizontalBlock immediately after the marker */
div.stMarkdown:has(#nav-btn-marker) + div[data-testid="stHorizontalBlock"] {
    display: none !important;
    height: 0 !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════╗
# ║  10. PRICING MODAL                                          ║
# ╚══════════════════════════════════════════════════════════════╝

if st.session_state.show_pricing:
    st.markdown("""
    <div class="modal-overlay">
        <div class="modal-box">
            <div class="modal-close" title="Close">✕</div>
            <p class="modal-title">Upgrade to Pro</p>
            <p class="modal-subtitle">Choose the plan that fits your workflow</p>
            <div class="pricing-grid">
                <div class="pricing-card">
                    <p class="plan-name">Free</p>
                    <p class="plan-price">$0 <span>/ month</span></p>
                    <ul class="plan-features">
                        <li>Basic summaries</li>
                        <li>1,024 max tokens</li>
                        <li>OCR (limited)</li>
                        <li>Local mode</li>
                    </ul>
                </div>
                <div class="pricing-card popular">
                    <div class="popular-badge">Most Popular</div>
                    <p class="plan-name">Pro</p>
                    <p class="plan-price">$9 <span>/ month</span></p>
                    <ul class="plan-features">
                        <li>Up to 4,096 tokens</li>
                        <li>Priority speed</li>
                        <li>Advanced formats</li>
                        <li>Export PDF / DOCX</li>
                        <li>Custom presets</li>
                    </ul>
                </div>
                <div class="pricing-card">
                    <p class="plan-name">Team</p>
                    <p class="plan-price">$29 <span>/ month</span></p>
                    <ul class="plan-features">
                        <li>Multi-user workspace</li>
                        <li>Shared history</li>
                        <li>Admin controls</li>
                        <li>Usage analytics</li>
                        <li>SLA support</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    pc1, pc2, pc3, pc4 = st.columns(4)
    with pc1:
        if st.button("Current Plan (Free)", key="btn_plan_free"):
            st.toast("You're already on the Free plan.", icon="ℹ️")
            st.session_state.show_pricing = False; st.rerun()
    with pc2:
        if st.button("⚡ Upgrade to Pro", key="btn_plan_pro"):
            st.toast("Pro upgrade requested! 🎉", icon="✅")
            st.session_state.show_pricing = False; st.rerun()
    with pc3:
        if st.button("Contact Sales (Team)", key="btn_plan_team"):
            st.toast("Sales team will contact you soon.", icon="📧")
            st.session_state.show_pricing = False; st.rerun()
    with pc4:
        if st.button("✕ Close", key="btn_close_pricing"):
            st.session_state.show_pricing = False; st.rerun()


# ╔══════════════════════════════════════════════════════════════╗
# ║  11. SIDEBAR (global — visible on all pages)                ║
# ╚══════════════════════════════════════════════════════════════╝

with st.sidebar:
    st.markdown("### ⚙️  Settings")
    server_ok = check_server()
    if server_ok:
        st.markdown("""<div class="status-chip status-on">
            <span class="status-dot"></span>Server Online</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="status-chip status-off">
            <span class="status-dot"></span>Server Offline</div>""", unsafe_allow_html=True)
    st.divider()
    summary_style = st.selectbox(
        "Summary Style",
        ["Concise", "Detailed", "Bullet Points",
         "Academic", "ELI5", "OCR Clean + Summarize"],
        help="'OCR Clean + Summarize' corrects OCR noise before summarizing.",
    )
    language = st.selectbox(
        "Output Language",
        ["Auto (same as input)", "English", "French", "Spanish",
         "German", "Arabic", "Chinese", "Japanese"],
    )
    temperature = st.slider("Temperature", 0.0, 1.5, 0.3, 0.05,
                            help="Lower = focused, higher = creative.")
    max_tokens = st.slider("Max Tokens", 64, 4096, 1024, 64)
    extra_instructions = st.text_area(
        "Custom Instructions",
        placeholder="e.g. Focus on financial aspects…", height=72,
    )
    st.divider()
    st.markdown("""<div class="sidebar-foot">
        <p><strong>SummarizeAI</strong> v1.0</p>
        <p>llama.cpp · 127.0.0.1:8080</p>
        <p>© 2026 · Built with Streamlit</p>
    </div>""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════╗
# ║  12. PAGE ROUTER                                            ║
# ╚══════════════════════════════════════════════════════════════╝

if _page == "HOME":
    render_home(server_ok, summary_style, language,
                extra_instructions, temperature, max_tokens)
elif _page == "ABOUT":
    render_about()
elif _page == "CONTENT":
    render_content()
elif _page == "OTHERS":
    render_others()


# ╔══════════════════════════════════════════════════════════════╗
# ║  13. FAB + FOOTER (global)                                  ║
# ╚══════════════════════════════════════════════════════════════╝

st.markdown("""
<div class="fab-next" title="Scroll down">
    <svg viewBox="0 0 24 24">
        <line x1="12" y1="5" x2="12" y2="19"/>
        <polyline points="19 12 12 19 5 12"/>
    </svg>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="app-footer">
    <p><strong>SummarizeAI</strong> — Intelligent text summarization, privately.</p>
    <p>© 2026 SummarizeAI · Powered by llama.cpp · Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
