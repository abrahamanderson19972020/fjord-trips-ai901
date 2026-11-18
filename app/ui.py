"""Fjord Trips · shared look and feel (UI only: styles, headers and cards, no app logic)."""
import base64
from functools import lru_cache
from html import escape
from pathlib import Path

import streamlit as st

PHOTOS = Path(__file__).resolve().parent.parent / "data" / "media" / "photos"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
:root {
  --ft-navy: #0b2540; --ft-deep: #10335a; --ft-teal: #138a83; --ft-aurora: #43d6b5;
  --ft-snow: #f5f8fb; --ft-ink: #1c2b3a; --ft-mute: #5d6b7a; --ft-line: #e2e8f0; --ft-coral: #ff6b5a;
}
html, body, [class*="css"], .stMarkdown, p, li, label, input, textarea, button {
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
}
.stApp { background: radial-gradient(1200px 500px at 85% -10%, #e3f4f2 0%, rgba(227,244,242,0) 60%), var(--ft-snow); color: var(--ft-ink); }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2.2rem; padding-bottom: 4rem; max-width: 1080px; }
h1, h2, h3 { font-family: 'Fraunces', Georgia, serif !important; color: var(--ft-navy); letter-spacing: -0.01em; }
h3 { font-size: 1.35rem !important; margin-top: 1.6rem !important; }

/* sidebar */
[data-testid="stSidebar"] { background: linear-gradient(180deg, var(--ft-navy) 0%, #0e3a5c 100%); }
[data-testid="stSidebar"] * { color: #dbe7f1 !important; }
[data-testid="stSidebarNav"] a { border-radius: 10px; margin: 2px 8px; }
[data-testid="stSidebarNav"] a:hover { background: rgba(255,255,255,0.08); }
[data-testid="stSidebarNav"] a[aria-current="page"] { background: rgba(67,214,181,0.18); }
[data-testid="stSidebarNav"] a[aria-current="page"] span { color: #ffffff !important; font-weight: 700; }
[data-testid="stSidebarNav"] li:first-child a p { font-size: 0 !important; }
[data-testid="stSidebarNav"] li:first-child a p::after { content: "Home"; font-size: 0.95rem; }
[data-testid="stSidebarNav"]::before { content: "⛰️  Fjord Trips"; display: block; padding: 0 22px 2px 22px;
  font-family: 'Fraunces', Georgia, serif; font-size: 1.45rem; font-weight: 700; color: #ffffff; }
[data-testid="stSidebarNav"] ul::before { content: "AI TRAVEL ASSISTANT"; display: block; padding: 0 22px 14px 22px;
  font-size: 0.7rem; letter-spacing: 0.16em; font-weight: 700; color: #43d6b5; }
.ft-brand { display: flex; align-items: center; gap: 10px; padding: 4px 6px 14px 6px; }
.ft-brand b { font-family: 'Fraunces', serif; font-size: 1.35rem; color: #fff !important; }
.ft-brand small { display: block; font-size: 0.72rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--ft-aurora) !important; }
.ft-side-note { margin-top: 18px; padding: 12px 14px; border-radius: 12px; background: rgba(255,255,255,0.06); font-size: 0.8rem; line-height: 1.45; }

/* hero */
.ft-hero { position: relative; overflow: hidden; border-radius: 22px; padding: 46px 44px 78px 44px; margin-bottom: 18px;
  color: #fff; background-color: var(--ft-navy); background-size: cover; background-position: center;
  box-shadow: 0 18px 40px -18px rgba(11,37,64,0.55); }
.ft-hero.small { padding: 30px 34px 62px 34px; }
.ft-hero::after { content: ""; position: absolute; inset: 0; background: linear-gradient(100deg, rgba(8,28,50,0.88) 0%, rgba(8,28,50,0.55) 55%, rgba(8,28,50,0.15) 100%); }
.ft-hero > * { position: relative; z-index: 1; }
.ft-kicker { display: inline-block; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--ft-aurora); background: rgba(67,214,181,0.14); border: 1px solid rgba(67,214,181,0.35); padding: 5px 12px; border-radius: 999px; }
.ft-hero h1 { color: #fff !important; font-size: 2.7rem !important; line-height: 1.08; margin: 14px 0 10px 0 !important; padding: 0 !important; }
.ft-hero.small h1 { font-size: 2.1rem !important; }
.ft-hero p { color: #dce8f2; font-size: 1.08rem; max-width: 640px; margin: 0; }
.ft-hero svg.ft-ridge { position: absolute; left: 0; right: 0; bottom: -2px; width: 100%; height: 48px; z-index: 1; opacity: 0.95; }

/* responsible-AI notice */
.ft-notice { display: flex; gap: 12px; align-items: center; background: #ffffff; border: 1px solid var(--ft-line);
  border-left: 5px solid var(--ft-teal); border-radius: 14px; padding: 12px 16px; margin: 6px 0 18px 0; color: var(--ft-ink); font-size: 0.95rem;
  box-shadow: 0 6px 18px -14px rgba(11,37,64,0.35); }
.ft-notice span { font-size: 1.25rem; }

/* home cards */
.ft-section { display: flex; align-items: baseline; gap: 10px; margin: 26px 0 10px 0; }
.ft-section h3 { margin: 0 !important; }
.ft-section small { color: var(--ft-mute); }
[data-testid="stVerticalBlockBorderWrapper"]:has(.ft-card) { background: #fff; border-radius: 18px !important; border-color: var(--ft-line) !important;
  box-shadow: 0 10px 26px -20px rgba(11,37,64,0.5); transition: transform .15s ease, box-shadow .15s ease; }
[data-testid="stVerticalBlockBorderWrapper"]:has(.ft-card):hover { transform: translateY(-3px); box-shadow: 0 18px 34px -20px rgba(11,37,64,0.55); }
.ft-card .ft-thumb { height: 120px; border-radius: 12px; background-size: cover; background-position: center; margin-bottom: 12px; }
.ft-card .ft-thumb.plain { background: linear-gradient(135deg, var(--ft-deep), var(--ft-teal)); display: flex; align-items: center; justify-content: center; font-size: 2.6rem; }
.ft-card p { color: var(--ft-mute); font-size: 0.9rem; margin: 0 0 4px 0; min-height: 2.6em; }
[data-testid="stPageLink"] a { background: var(--ft-navy); border-radius: 10px; padding: 6px 12px; }
[data-testid="stPageLink"] a:hover { background: var(--ft-teal); }
[data-testid="stPageLink"] a p, [data-testid="stPageLink"] a span { color: #fff !important; font-weight: 600; }

/* widgets */
.stButton > button, .stDownloadButton > button { border-radius: 12px; font-weight: 600; padding: 0.55rem 1.2rem; }
.stButton > button[kind="primary"], .stDownloadButton > button { background: linear-gradient(135deg, var(--ft-teal), #0f6f8f); border: 0; color: #fff; }
.stButton > button[kind="primary"]:hover { filter: brightness(1.08); }
[data-testid="stTextInput"] input, [data-baseweb="select"] > div { border-radius: 12px !important; }
[data-testid="stFileUploaderDropzone"] { border-radius: 16px; border: 2px dashed #b9d6dc; background: #ffffff; }
[data-testid="stAudioInput"] { border-radius: 16px; }
[data-testid="stImage"] img { border-radius: 16px; box-shadow: 0 16px 34px -20px rgba(11,37,64,0.6); }
[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; border: 1px solid var(--ft-line); }

/* chat */
[data-testid="stChatMessage"] { background: #ffffff; border: 1px solid var(--ft-line); border-radius: 18px; padding: 14px 18px;
  box-shadow: 0 8px 22px -18px rgba(11,37,64,0.45); }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) { background: #e9f6f4; border-color: #cfe9e5; }
[data-testid="stChatInput"] { border-radius: 16px; }
[data-testid="stChatInput"] textarea { font-size: 1rem; }
.ft-tips { display: flex; flex-wrap: wrap; gap: 8px; margin: 4px 0 14px 0; }
.ft-tips span { background: #fff; border: 1px solid var(--ft-line); border-radius: 999px; padding: 6px 14px; font-size: 0.85rem; color: var(--ft-mute); }

/* metrics */
[data-testid="stMetric"] { background: #fff; border: 1px solid var(--ft-line); border-radius: 16px; padding: 16px 18px;
  box-shadow: 0 8px 22px -18px rgba(11,37,64,0.45); }
[data-testid="stMetricValue"] { font-family: 'Fraunces', serif; color: var(--ft-navy); }
.ft-panel { background: #fff; border: 1px solid var(--ft-line); border-radius: 16px; padding: 18px 20px; line-height: 1.6; }
.ft-chip { display: inline-block; background: #eef6f8; color: var(--ft-deep); border-radius: 999px; padding: 5px 12px; margin: 3px 4px 3px 0; font-size: 0.88rem; font-weight: 600; }
footer { visibility: hidden; }
[data-testid="stRadioOption"][data-selected="true"] > div > div:first-child { background-color: var(--ft-teal) !important; border-color: var(--ft-teal) !important; }
[data-testid="stChatInput"] > div { border-color: #9fd3cc !important; border-radius: 16px !important; box-shadow: 0 10px 28px -18px rgba(11,37,64,0.5); }
[data-testid="stChatInput"] > div:focus-within { border-color: var(--ft-teal) !important; }
[data-testid="stBottom"] > div { background: transparent; }
.ft-foot { text-align: center; color: var(--ft-mute); font-size: 0.8rem; margin-top: 40px; }
</style>
"""

RIDGE = """<svg class="ft-ridge" viewBox="0 0 1200 70" preserveAspectRatio="none"><path fill="#f5f8fb"
d="M0,70 L0,46 L90,30 L170,44 L260,14 L340,38 L420,22 L520,48 L610,18 L700,40 L790,26 L880,50 L980,20 L1080,42 L1200,28 L1200,70 Z"/></svg>"""


@lru_cache(maxsize=16)
def _photo(name):
    """Return a CSS background for a photo in data/media/photos, or '' if it isn't there."""
    path = PHOTOS / name
    try:
        data = base64.b64encode(path.read_bytes()).decode()
    except OSError:
        return ""
    return f"background-image: url('data:image/jpeg;base64,{data}');"


def style():
    """Apply the Fjord Trips look and the sidebar brand. Call once, right after st.set_page_config."""
    st.markdown(CSS, unsafe_allow_html=True)


def sidebar_note():
    with st.sidebar:
        st.markdown('<div class="ft-side-note">🤝 A human travel advisor confirms every booking.<br>'
                    'Fjord Trips is a fictional company for the AI-901 course.</div>', unsafe_allow_html=True)


def hero(kicker, title, subtitle="", photo=None, small=True):
    bg = _photo(photo) if photo else ""
    cls = "ft-hero small" if small else "ft-hero"
    sub = f"<p>{escape(subtitle)}</p>" if subtitle else ""
    st.markdown(f'<div class="{cls}" style="{bg}"><span class="ft-kicker">{escape(kicker)}</span>'
                f'<h1>{escape(title)}</h1>{sub}{RIDGE}</div>', unsafe_allow_html=True)


def notice(text, icon="🤝"):
    st.markdown(f'<div class="ft-notice"><span>{icon}</span><div>{escape(text)}</div></div>', unsafe_allow_html=True)


def section(title, note=""):
    small = f"<small>{escape(note)}</small>" if note else ""
    st.markdown(f'<div class="ft-section"><h3>{escape(title)}</h3>{small}</div>', unsafe_allow_html=True)


def card_top(text, photo=None, icon="⛰️"):
    bg = _photo(photo) if photo else ""
    thumb = f'<div class="ft-thumb" style="{bg}"></div>' if bg else f'<div class="ft-thumb plain">{icon}</div>'
    st.markdown(f'<div class="ft-card">{thumb}<p>{escape(text)}</p></div>', unsafe_allow_html=True)


def tips(items):
    st.markdown('<div class="ft-tips">' + "".join(f"<span>{escape(i)}</span>" for i in items) + "</div>", unsafe_allow_html=True)


def chips(items):
    st.markdown("".join(f'<span class="ft-chip">{escape(i)}</span>' for i in items), unsafe_allow_html=True)


def panel(text):
    st.markdown(f'<div class="ft-panel">{escape(text)}</div>', unsafe_allow_html=True)


def footer():
    st.markdown('<div class="ft-foot">Fjord Trips · built with Microsoft Foundry · AI, Actually · AI-901 course</div>', unsafe_allow_html=True)
