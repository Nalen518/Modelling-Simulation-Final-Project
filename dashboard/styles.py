import streamlit as st

MEDICAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* Force Streamlit app background to Deep Slate */
.stApp, html, body {
  background-color: #0B132B !important;
  color: #F1F5F9 !important;
  font-family: 'Inter', sans-serif !important;
}

/* Force sidebar background to even darker slate */
[data-testid="stSidebar"] {
  background-color: #080D1A !important;
}
[data-testid="stSidebar"] * {
  color: #FFFFFF !important;
}
[data-testid="stSidebar"] label {
  font-family: 'Raleway', sans-serif !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.04em !important;
  text-transform: uppercase !important;
  color: rgba(255,255,255,0.75) !important;
}
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] {
  background: #06B6D4 !important;
  color: white !important;
  border-radius: 4px !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.75rem !important;
}

/* Titles and Headers */
h1, h2, h3, h4, h5, h6 {
  font-family: 'Raleway', sans-serif !important;
  color: #F1F5F9 !important;
}

.main .block-container {
  padding: 1.5rem 2.5rem 3rem !important;
  max-width: 1280px !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Buttons styling */
.stButton > button {
  background: linear-gradient(135deg, #0891B2 0%, #06B6D4 100%) !important;
  color: white !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 0.65rem 1.75rem !important;
  font-family: 'Raleway', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  box-shadow: 0 2px 8px rgba(6,182,212,0.25) !important;
  transition: all 0.2s ease !important;
  width: 100% !important;
}
.stButton > button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 16px rgba(6,182,212,0.4) !important;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
  background: #080D1A !important;
  border-radius: 8px !important;
  padding: 4px !important;
  gap: 2px !important;
  border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 6px !important;
  color: #94A3B8 !important;
  font-family: 'Raleway', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.85rem !important;
  padding: 0.4rem 1.2rem !important;
  border: none !important;
  transition: all 0.15s ease !important;
}
.stTabs [aria-selected="true"] {
  background: #1C2541 !important;
  color: #06B6D4 !important;
  font-weight: 700 !important;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
}

/* Metric card container */
[data-testid="metric-container"] {
  background: #1C2541 !important;
  border-radius: 10px !important;
  padding: 1rem 1.25rem !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
  border-top: 3px solid #06B6D4 !important;
}
[data-testid="metric-container"] label {
  font-size: 0.72rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.07em !important;
  text-transform: uppercase !important;
  color: #94A3B8 !important;
  font-family: 'Raleway', sans-serif !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 1.75rem !important;
  color: #FFFFFF !important;
  font-weight: 600 !important;
}

/* Dataframes */
[data-testid="stDataFrame"] {
  border-radius: 10px !important;
  overflow: hidden !important;
  border: 1px solid #1E2D4A !important;
  background: #1C2541 !important;
}

/* Custom styled lines */
hr {
  border: none !important;
  border-top: 1.5px solid #1E2D4A !important;
  margin: 1.25rem 0 !important;
}

/* Scrollbar customization */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0B132B; }
::-webkit-scrollbar-thumb {
  background: #1C2541;
  border-radius: 3px;
}
</style>
"""

def inject_css():
    st.markdown(MEDICAL_CSS, unsafe_allow_html=True)


def render_header():
    st.markdown("""
<div style="background:linear-gradient(135deg, #080D1A 0%, #1C2541 100%);
  border:1px solid #1E2D4A;
  border-radius:16px;padding:2rem 2.5rem;
  margin-bottom:1.75rem;position:relative;
  overflow:hidden;">
  <h1 style="font-family:'Raleway',sans-serif;
    font-size:1.9rem;font-weight:700;color:white;
    margin:0 0 0.35rem 0;line-height:1.2;">
    IGD Queue Optimization
  </h1>
  <p style="color:#94A3B8;
    font-size:0.88rem;margin:0;font-weight:400;font-family:'Inter',sans-serif;">
    Emergency Room Discrete Event Simulation
    — Triage-Based Patient Flow Analysis
  </p>
  <div style="display:flex;gap:0.5rem;
    margin-top:1rem;flex-wrap:wrap;">
    <span style="background:rgba(6,182,212,0.12);
      border:1px solid rgba(6,182,212,0.25);
      color:#06B6D4;font-size:0.72rem;
      font-weight:600;letter-spacing:0.06em;
      text-transform:uppercase;padding:0.28rem 0.75rem;
      border-radius:20px;
      font-family:'JetBrains Mono',monospace;">
      SimPy DES
    </span>
    <span style="background:rgba(6,182,212,0.12);
      border:1px solid rgba(6,182,212,0.25);
      color:#06B6D4;font-size:0.72rem;
      font-weight:600;letter-spacing:0.06em;
      text-transform:uppercase;padding:0.28rem 0.75rem;
      border-radius:20px;
      font-family:'JetBrains Mono',monospace;">
      M/M/1 → M/M/s → M/M/c
    </span>
    <span style="background:rgba(6,182,212,0.12);
      border:1px solid rgba(6,182,212,0.25);
      color:#06B6D4;font-size:0.72rem;
      font-weight:600;letter-spacing:0.06em;
      text-transform:uppercase;padding:0.28rem 0.75rem;
      border-radius:20px;
      font-family:'JetBrains Mono',monospace;">
      Monte Carlo N=100
    </span>
    <span style="background:rgba(6,182,212,0.12);
      border:1px solid rgba(6,182,212,0.25);
      color:#06B6D4;font-size:0.72rem;
      font-weight:600;letter-spacing:0.06em;
      text-transform:uppercase;padding:0.28rem 0.75rem;
      border-radius:20px;
      font-family:'JetBrains Mono',monospace;">
      Kemenkes Standard
    </span>
  </div>
</div>""", unsafe_allow_html=True)


def render_section(title: str, tag: str = ""):
    tag_html = (
        f'<span style="margin-left:auto;'
        f'background:#1C2541;color:#06B6D4;'
        f'font-size:10px;font-weight:600;'
        f'letter-spacing:.05em;text-transform:uppercase;'
        f'padding:3px 8px;border-radius:4px;'
        f'font-family:\'JetBrains Mono\',monospace;border:1px solid #1E2D4A;">{tag}</span>'
        if tag else "")
    st.markdown(
        f'<div style="display:flex;align-items:center;'
        f'gap:10px;margin:20px 0 12px;padding-bottom:8px;'
        f'border-bottom:1.5px solid #1E2D4A;">'
        f'<div style="width:8px;height:8px;'
        f'border-radius:50%;background:#06B6D4;'
        f'flex-shrink:0"></div>'
        f'<span style="font-size:15px;font-weight:700;'
        f'color:#F1F5F9;font-family:\'Raleway\',sans-serif">'
        f'{title}</span>'
        f'{tag_html}</div>',
        unsafe_allow_html=True)


def render_info(text: str, kind: str = "info"):
    palette = {
        "info":    ("#132238", "#93C5FD", "#3B82F6"),
        "warn":    ("#2B2211", "#FDE047", "#EAB308"),
        "success": ("#0C2B1B", "#86EFAC", "#22C55E"),
        "danger":  ("#371318", "#FCA5A5", "#EF4444"),
    }
    bg, tc, bc = palette.get(kind, palette["info"])
    st.markdown(
        f'<div style="background:{bg};'
        f'border-left:4px solid {bc};'
        f'border-radius:0 8px 8px 0;'
        f'padding:10px 14px;font-size:14px;'
        f'color:{tc};margin:6px 0;line-height:1.5;'
        f'font-family:\'Inter\',sans-serif">'
        f'{text}</div>',
        unsafe_allow_html=True)


def render_priority_legend():
    st.markdown("""
<div style="display:flex;gap:8px;flex-wrap:wrap;
  margin:6px 0 14px 0;">
  <div style="display:flex;align-items:center;gap:5px;
    font-size:12px;color:#94A3B8;font-family:'Inter',sans-serif;">
    <div style="width:12px;height:12px;border-radius:50%;
      background:#f7c1c1;border:1.5px solid #e24b4a">
    </div>Red – critical
  </div>
  <div style="display:flex;align-items:center;gap:5px;
    font-size:12px;color:#94A3B8;font-family:'Inter',sans-serif;">
    <div style="width:12px;height:12px;border-radius:50%;
      background:#fac775;border:1.5px solid #ba7517">
    </div>Yellow – emergency
  </div>
  <div style="display:flex;align-items:center;gap:5px;
    font-size:12px;color:#94A3B8;font-family:'Inter',sans-serif;">
    <div style="width:12px;height:12px;border-radius:50%;
      background:#c0dd97;border:1.5px solid #639922">
    </div>Green – urgent
  </div>
  <div style="display:flex;align-items:center;gap:5px;
    font-size:12px;color:#94A3B8;font-family:'Inter',sans-serif;">
    <div style="width:12px;height:12px;border-radius:50%;
      background:#2A3547;border:1.5px solid #95A5A6">
    </div>White – non-urgent
  </div>
  <div style="display:flex;align-items:center;gap:5px;
    font-size:12px;color:#94A3B8;font-family:'Inter',sans-serif;">
    <div style="width:12px;height:12px;border-radius:50%;
      background:#1C2541;border:1.5px solid #475569">
    </div>Black – DOA
  </div>
</div>""", unsafe_allow_html=True)
