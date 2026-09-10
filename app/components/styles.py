"""
app/components/styles.py
Global colourful CSS injected into every page.
"""
import streamlit as st

_CSS = """
<style>
/* ── Root palette ── */
:root {
    --blue:    #1a56db;
    --purple:  #7e3af2;
    --green:   #057a55;
    --orange:  #d97706;
    --pink:    #db2777;
    --teal:    #0891b2;
    --surface: #f0f4ff;
    --border:  #dde3f7;
    --text:    #111827;
    --muted:   #6b7280;
}

/* ── Force light background on main content ── */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] { background: #f0f4ff !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg,#1a1a2e 0%,#16213e 60%,#0f3460 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] label,
[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNavItems"] span {
    color: #e2e8f0 !important;
    font-weight: 500;
}
[data-testid="stSidebarNavItems"] a:hover span { color: #93c5fd !important; }
/* Active nav item highlight */
[data-testid="stSidebarNavItems"] [aria-current="page"] span {
    color: #60a5fa !important;
    font-weight: 700;
}

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #1a56db 0%, #7e3af2 55%, #db2777 100%);
    color: #fff;
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(126,58,242,0.25);
}
.hero h1 { color:#fff; font-size:2.2rem; margin:0 0 .5rem 0; letter-spacing:-.5px; }
.hero p  { color:rgba(255,255,255,.88); margin:0; font-size:1.05rem; }

/* ── Coloured feature cards ── */
.fcard {
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: .8rem;
    color: #fff;
    min-height: 110px;
    display: flex; flex-direction: column; justify-content: space-between;
    box-shadow: 0 4px 18px rgba(0,0,0,.12);
    transition: transform .15s;
}
.fcard:hover { transform: translateY(-3px); }
.fcard b  { font-size: 1.05rem; }
.fcard small { opacity: .88; font-size: .82rem; margin-top:.4rem; }
.fc-blue   { background: linear-gradient(135deg,#1a56db,#3b82f6); }
.fc-purple { background: linear-gradient(135deg,#7e3af2,#a78bfa); }
.fc-green  { background: linear-gradient(135deg,#057a55,#34d399); }
.fc-orange { background: linear-gradient(135deg,#d97706,#fbbf24); }
.fc-pink   { background: linear-gradient(135deg,#db2777,#f472b6); }
.fc-teal   { background: linear-gradient(135deg,#0891b2,#22d3ee); }
.fc-indigo { background: linear-gradient(135deg,#4338ca,#818cf8); }

/* ── Plain utility card ── */
.card {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(26,86,219,.07);
}

/* ── Metric tiles ── */
[data-testid="stMetric"] {
    background: #fff;
    border-radius: 14px;
    border: 1px solid var(--border);
    padding: .9rem 1.2rem !important;
    box-shadow: 0 2px 8px rgba(26,86,219,.07);
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size:.8rem; }
[data-testid="stMetricValue"] { color: var(--blue) !important; font-weight:700; }

/* ── Flashcard ── */
.fc-inner {
    background: linear-gradient(135deg,#eff6ff,#f5f3ff);
    border: 2px solid var(--blue);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    min-height: 150px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.15rem; font-weight: 600; color: var(--text);
    box-shadow: 0 4px 20px rgba(26,86,219,.1);
}
.fc-back {
    background: linear-gradient(135deg,#f5f3ff,#fce7f3);
    border-color: var(--purple);
    font-weight: 400; font-size: 1rem;
}

/* ── Badges ── */
.badge {
    display:inline-block; padding:3px 12px;
    border-radius:999px; font-size:.75rem; font-weight:600;
}
.badge-blue   { background:#dbeafe; color:#1d4ed8; }
.badge-purple { background:#ede9fe; color:#6d28d9; }
.badge-green  { background:#d1fae5; color:#065f46; }
.badge-red    { background:#fee2e2; color:#991b1b; }
.badge-orange { background:#fef3c7; color:#92400e; }

/* ── Buttons ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg,#1a56db,#7e3af2) !important;
    border: none !important; border-radius: 10px !important;
    color: #fff !important; font-weight: 600 !important;
    padding: .5rem 1.5rem !important;
    box-shadow: 0 4px 14px rgba(126,58,242,.3) !important;
}
.stButton > button[kind="primary"]:hover {
    opacity: .92 !important; transform: translateY(-1px);
}
.stButton > button[kind="secondary"] {
    border-radius: 10px !important;
}

/* ── Section headings (pages only) ── */
h1 { color: var(--blue) !important; }
h2, h3 { color: #1e293b !important; }
/* Hero overrides — keep hero text white no matter what */
.hero h1, .hero h2, .hero h3, .hero p, .hero span { color: #fff !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    background: #fff !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    border-radius: 14px !important;
    margin-bottom: .5rem !important;
}

/* ── Page layout ── */
.block-container { padding-top: 1.5rem !important; }
</style>
"""


def inject_css() -> None:
    """Inject shared colourful CSS into the current Streamlit page."""
    st.markdown(_CSS, unsafe_allow_html=True)
