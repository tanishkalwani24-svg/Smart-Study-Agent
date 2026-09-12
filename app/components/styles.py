"""
app/components/styles.py
Global dark-theme CSS injected into every page.
"""
import streamlit as st

_CSS = """
<style>
/* ── Root palette (dark) ── */
:root {
    --bg:        #0f0f1a;
    --surface:   #1a1a2e;
    --surface2:  #16213e;
    --border:    #2d2d4e;
    --blue:      #4f8ef7;
    --purple:    #a78bfa;
    --green:     #34d399;
    --orange:    #fbbf24;
    --pink:      #f472b6;
    --teal:      #22d3ee;
    --indigo:    #818cf8;
    --text:      #e2e8f0;
    --muted:     #94a3b8;
}

/* ── Full dark background everywhere ── */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"],
section.main,
.main .block-container {
    background: #0f0f1a !important;
    color: #e2e8f0 !important;
}

/* ── All text dark-mode ── */
p, span, li, label, div {
    color: #e2e8f0 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg,#0a0a18 0%,#12122a 50%,#0f1b35 100%) !important;
    border-right: 1px solid #2d2d4e !important;
}
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] label,
[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNavItems"] span {
    color: #cbd5e1 !important;
    font-weight: 500;
}
[data-testid="stSidebarNavItems"] a:hover span { color: #60a5fa !important; }
[data-testid="stSidebarNavItems"] [aria-current="page"] span {
    color: #818cf8 !important;
    font-weight: 700;
}

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #1a1f6e 0%, #3b1f8c 45%, #6b1f5c 100%);
    color: #fff;
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 1.5rem;
    border: 1px solid #3d3d6e;
    box-shadow: 0 8px 40px rgba(79,142,247,0.2);
}
.hero h1, .hero h2, .hero h3, .hero p, .hero span { color: #fff !important; }
.hero h1 { font-size:2.2rem; margin:0 0 .5rem 0; letter-spacing:-.5px; }
.hero p  { color:rgba(255,255,255,.85); margin:0; font-size:1.05rem; }

/* ── Coloured feature cards ── */
.fcard {
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: .8rem;
    color: #fff;
    min-height: 110px;
    display: flex; flex-direction: column; justify-content: space-between;
    box-shadow: 0 4px 24px rgba(0,0,0,.4);
    transition: transform .15s, box-shadow .15s;
    border: 1px solid rgba(255,255,255,.08);
}
.fcard:hover { transform: translateY(-4px); box-shadow: 0 8px 32px rgba(0,0,0,.5); }
.fcard b  { font-size: 1.05rem; color: #fff !important; }
.fcard small { opacity: .85; font-size: .82rem; margin-top:.4rem; color: rgba(255,255,255,.85) !important; }
.fc-blue   { background: linear-gradient(135deg,#1a3a8f,#2563eb); }
.fc-purple { background: linear-gradient(135deg,#4c1d95,#7c3aed); }
.fc-green  { background: linear-gradient(135deg,#064e3b,#059669); }
.fc-orange { background: linear-gradient(135deg,#78350f,#d97706); }
.fc-pink   { background: linear-gradient(135deg,#831843,#db2777); }
.fc-teal   { background: linear-gradient(135deg,#164e63,#0891b2); }
.fc-indigo { background: linear-gradient(135deg,#312e81,#4338ca); }

/* ── Plain utility card ── */
.card {
    background: #1a1a2e !important;
    border: 1px solid #2d2d4e;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,.3);
    color: #e2e8f0 !important;
}

/* ── Metric tiles ── */
[data-testid="stMetric"] {
    background: #1a1a2e !important;
    border-radius: 14px;
    border: 1px solid #2d2d4e !important;
    padding: .9rem 1.2rem !important;
    box-shadow: 0 2px 12px rgba(0,0,0,.3);
}
[data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size:.8rem; }
[data-testid="stMetricValue"] { color: #4f8ef7 !important; font-weight:700; }
[data-testid="stMetricDelta"] { color: #34d399 !important; }

/* ── Flashcard ── */
.fc-inner {
    background: linear-gradient(135deg,#1a1a3e,#1e1b4b);
    border: 2px solid #4f8ef7;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    min-height: 150px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.15rem; font-weight: 600; color: #e2e8f0 !important;
    box-shadow: 0 4px 24px rgba(79,142,247,.2);
}
.fc-back {
    background: linear-gradient(135deg,#1e1b4b,#2d1f4e);
    border-color: #a78bfa;
    font-weight: 400; font-size: 1rem;
    color: #e2e8f0 !important;
}

/* ── Badges ── */
.badge {
    display:inline-block; padding:3px 12px;
    border-radius:999px; font-size:.75rem; font-weight:600;
}
.badge-blue   { background:#1e3a5f; color:#60a5fa; }
.badge-purple { background:#2e1a5e; color:#a78bfa; }
.badge-green  { background:#064e3b; color:#34d399; }
.badge-red    { background:#4c0519; color:#f87171; }
.badge-orange { background:#451a03; color:#fbbf24; }

/* ── Buttons ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg,#1a3a8f,#5b21b6) !important;
    border: 1px solid #4f8ef7 !important;
    border-radius: 10px !important;
    color: #fff !important; font-weight: 600 !important;
    padding: .5rem 1.5rem !important;
    box-shadow: 0 4px 14px rgba(79,142,247,.3) !important;
}
.stButton > button[kind="primary"]:hover {
    opacity: .9 !important; transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(79,142,247,.45) !important;
}
.stButton > button[kind="secondary"] {
    border-radius: 10px !important;
    background: #1a1a2e !important;
    border: 1px solid #2d2d4e !important;
    color: #e2e8f0 !important;
}

/* ── Headings ── */
h1 { color: #4f8ef7 !important; }
h2, h3 { color: #a78bfa !important; }
h4, h5, h6 { color: #cbd5e1 !important; }

/* ── Inputs / Selectbox / Textarea ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input {
    background: #1a1a2e !important;
    color: #e2e8f0 !important;
    border: 1px solid #2d2d4e !important;
    border-radius: 8px !important;
}
[data-testid="stSelectbox"] > div,
[data-testid="stMultiSelect"] > div {
    background: #1a1a2e !important;
    border: 1px solid #2d2d4e !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}

/* ── Slider ── */
[data-testid="stSlider"] > div > div {
    color: #e2e8f0 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    border: 1px solid #2d2d4e !important;
    border-radius: 12px !important;
    background: #1a1a2e !important;
}
[data-testid="stExpander"] summary {
    color: #cbd5e1 !important;
}

/* ── Alert / banner boxes ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
}
.stSuccess { background: #052e16 !important; border-left: 4px solid #34d399 !important; }
.stWarning { background: #431407 !important; border-left: 4px solid #fbbf24 !important; }
.stError   { background: #3b0764 !important; border-left: 4px solid #f87171 !important; }
.stInfo    { background: #0c1a40 !important; border-left: 4px solid #60a5fa !important; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    border-radius: 14px !important;
    background: #1a1a2e !important;
    border: 1px solid #2d2d4e !important;
    margin-bottom: .5rem !important;
}

/* ── Radio buttons ── */
[data-testid="stRadio"] label { color: #cbd5e1 !important; }

/* ── Checkbox ── */
[data-testid="stCheckbox"] label { color: #cbd5e1 !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #1a1a2e !important;
    border: 2px dashed #2d2d4e !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"] span { color: #94a3b8 !important; }

/* ── Divider ── */
hr { border-color: #2d2d4e !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f0f1a; }
::-webkit-scrollbar-thumb { background: #2d2d4e; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #4f8ef7; }

/* ── Page layout ── */
.block-container { padding-top: 1.5rem !important; }

/* ── Plotly chart backgrounds ── */
.js-plotly-plot .plotly { background: transparent !important; }

/* ── Clickable feature cards ── */
a.fcard-link {
    display: block;
    text-decoration: none !important;
    color: inherit;
    cursor: pointer;
}
a.fcard-link:hover .fcard {
    transform: translateY(-6px);
    box-shadow: 0 12px 40px rgba(0,0,0,.6);
}
</style>
"""


def inject_css() -> None:
    """Inject shared dark-theme CSS into the current Streamlit page."""
    st.markdown(_CSS, unsafe_allow_html=True)
