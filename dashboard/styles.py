import streamlit as st

MEDICAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Raleway:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

.material-symbols-outlined {
  font-family: 'Material Symbols Outlined' !important;
  font-weight: normal;
  font-style: normal;
  font-size: 24px;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
  -webkit-font-smoothing: antialiased;
}

/* Force Streamlit app background */
.stApp, html, body {
  background-color: #0f1418 !important;
  color: #dee3e8 !important;
  font-family: 'Inter', sans-serif !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
  background-color: #1b2024 !important;
}
[data-testid="stSidebar"] * {
  color: #FFFFFF !important;
}
[data-testid="stSidebar"] label {
  font-family: 'Inter', sans-serif !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.04em !important;
  text-transform: uppercase !important;
  color: rgba(255,255,255,0.75) !important;
}
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] {
  display: none !important;
}

/* Titles and Headers */
h1, h2, h3, h4, h5, h6 {
  font-family: 'Inter', sans-serif !important;
  color: #dee3e8 !important;
}

.main .block-container {
  padding: 1.5rem 2.5rem 3rem !important;
  max-width: 1280px !important;
}
#MainMenu, footer { visibility: hidden !important; }
header[data-testid="stHeader"] {
  background-color: transparent !important;
  background: transparent !important;
  border-bottom: none !important;
  box-shadow: none !important;
}
.stDeployButton { display: none !important; }

/* Buttons styling */
.stButton > button {
  background: #252b2e !important;
  color: #dee3e8 !important;
  border: 1px solid #3e484f !important;
  border-radius: 10px !important;
  padding: 0.65rem 1.75rem !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  box-shadow: none !important;
  transition: all 0.2s ease !important;
  width: 100% !important;
}
.stButton > button:hover {
  background: #303539 !important;
  border-color: #8ed5ff !important;
  color: #8ed5ff !important;
  box-shadow: none !important;
}

/* Sidebar — Run Simulation (primary button) */
[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 0.72rem 1.5rem !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.9rem !important;
  letter-spacing: 0.02em !important;
  box-shadow: 0 4px 14px rgba(34, 197, 94, 0.2) !important;
  transition: all 0.2s ease !important;
  width: 100% !important;
}
[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"]:hover {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
  box-shadow: 0 6px 20px rgba(34, 197, 94, 0.35) !important;
  transform: translateY(-1px) !important;
  color: #ffffff !important;
  border-color: transparent !important;
}

/* Sidebar — Reset All (secondary button) */
[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"] {
  background: transparent !important;
  color: #bdc8d1 !important;
  border: none !important;
  font-size: 0.76rem !important;
  font-weight: 500 !important;
  padding: 0.3rem 0.8rem !important;
  opacity: 0.65 !important;
  box-shadow: none !important;
}
[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"]:hover {
  color: #8ed5ff !important;
  opacity: 1 !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
  background: #1b2024 !important;
  border-radius: 8px !important;
  padding: 4px !important;
  gap: 2px !important;
  border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 6px !important;
  color: #bdc8d1 !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.85rem !important;
  padding: 0.4rem 1.2rem !important;
  border: none !important;
  transition: all 0.15s ease !important;
}
.stTabs [aria-selected="true"] {
  background: #252b2e !important;
  color: #8ed5ff !important;
  font-weight: 700 !important;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
}

/* Metric card container */
[data-testid="metric-container"] {
  background: #252b2e !important;
  border-radius: 10px !important;
  padding: 1rem 1.25rem !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
  border: 1px solid #3e484f !important;
}
[data-testid="metric-container"] label {
  font-size: 0.72rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.07em !important;
  text-transform: uppercase !important;
  color: #bdc8d1 !important;
  font-family: 'Inter', sans-serif !important;
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
  border: 1px solid #3e484f !important;
  background: #252b2e !important;
}

/* Custom styled lines */
hr {
  border: none !important;
  border-top: 1.5px solid #3e484f !important;
  margin: 1.25rem 0 !important;
}

/* Scrollbar customization */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0f1418; }
::-webkit-scrollbar-thumb {
  background: #303539;
  border-radius: 3px;
}
</style>
"""

def inject_css():
    st.markdown(MEDICAL_CSS, unsafe_allow_html=True)


def render_header(params: dict | None = None):
    lam = params.get("lambda", 20) if params else 20
    docs = params.get("n_doctors", 3) if params else 3
    nurs = params.get("n_nurses", 1) if params else 1
    dur = params.get("duration", 480) if params else 480

    tag_style = (
        "background:#303539;border:1px solid #3e484f;"
        "font-size:0.66rem;font-weight:700;"
        "letter-spacing:0.04em;text-transform:uppercase;"
        "padding:0.22rem 0.6rem;border-radius:20px;"
        "font-family:'JetBrains Mono',monospace;white-space:nowrap;"
    )

    cfg_item = (
        '<div style="text-align:center;min-width:64px;">'
        '  <div style="font-size:0.75rem;margin-bottom:2px;opacity:0.7;">{icon}</div>'
        '  <div style="font-family:\'JetBrains Mono\',monospace;font-size:1.15rem;'
        '    font-weight:700;color:#ffffff;line-height:1.15;">{val}</div>'
        '  <div style="font-size:0.62rem;color:#bdc8d1;opacity:0.7;'
        '    margin-top:1px;font-weight:500;">{label}</div>'
        '</div>'
    )

    st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:flex-start;
  flex-wrap:wrap;gap:1rem;padding-bottom:1rem;margin-bottom:1.25rem;
  border-bottom:1px solid #3e484f;">

  <!-- Left: title + tags -->
  <div style="flex:1;min-width:280px;">
    <h1 style="font-family:'Inter',sans-serif;font-size:1.65rem;font-weight:700;
      color:#dee3e8;margin:0 0 0.2rem;line-height:1.15;letter-spacing:-0.02em;">
      IGD Queue Optimization
    </h1>
    <p style="color:#bdc8d1;font-size:0.82rem;margin:0 0 0.7rem;font-weight:400;
      font-family:'Inter',sans-serif;line-height:1.35;">
      Emergency Room Discrete Event Simulation — Triage-Based Patient Flow Analysis
    </p>
    <div style="display:flex;gap:0.35rem;flex-wrap:wrap;align-items:center;">
      <span style="{tag_style}color:#8ed5ff;">SimPy DES</span>
      <span style="{tag_style}color:#c4b5fd;">M/M/1 → M/M/S → M/M/C</span>
      <span style="{tag_style}color:#ffc176;">Monte Carlo N=100</span>
      <span style="{tag_style}color:#4ade80;">Kemenkes Standard</span>
    </div>
  </div>

  <!-- Right: live config card -->
  <div style="background:#1b2024;border:1px solid #3e484f;border-radius:10px;
    padding:0.6rem 0.9rem 0.7rem;min-width:300px;flex-shrink:0;">
    <div style="display:flex;justify-content:space-between;align-items:center;
      margin-bottom:0.45rem;">
      <span style="font-family:'Inter',sans-serif;font-size:0.62rem;font-weight:700;
        letter-spacing:0.09em;color:#bdc8d1;text-transform:uppercase;">
        Current Configuration</span>
      <span class="material-symbols-outlined"
        style="font-size:0.95rem;color:#bdc8d1;opacity:0.5;">dashboard</span>
    </div>
    <div style="display:flex;justify-content:space-around;gap:0.4rem;">
      {cfg_item.format(icon='λ', val=lam, label='pts/hr')}
      {cfg_item.format(icon='👨‍⚕️', val=docs, label='Doctors')}
      {cfg_item.format(icon='👩‍⚕️', val=nurs, label='Nurses')}
      {cfg_item.format(icon='⏱️', val=dur, label='min')}
    </div>
  </div>

</div>""", unsafe_allow_html=True)


def render_section(title: str, tag: str = ""):
    tag_html = (
        f'<span style="margin-left:auto;'
        f'background:#303539;color:#8ed5ff;'
        f'font-size:10px;font-weight:600;'
        f'letter-spacing:.05em;text-transform:uppercase;'
        f'padding:3px 8px;border-radius:4px;'
        f'font-family:\'JetBrains Mono\',monospace;border:1px solid #3e484f;">{tag}</span>'
        if tag else "")
    st.markdown(
        f'<div style="display:flex;align-items:center;'
        f'gap:10px;margin:20px 0 12px;padding-bottom:8px;'
        f'border-bottom:1.5px solid #3e484f;">'
        f'<div style="width:8px;height:8px;'
        f'border-radius:50%;background:#8ed5ff;'
        f'flex-shrink:0"></div>'
        f'<span style="font-size:15px;font-weight:700;'
        f'color:#dee3e8;font-family:\'Inter\',sans-serif">'
        f'{title}</span>'
        f'{tag_html}</div>',
        unsafe_allow_html=True)


def render_info(text: str, kind: str = "info"):
    palette = {
        "info":    ("#1b2024", "#8ed5ff", "#38bdf8"),
        "warn":    ("#2b2211", "#ffc176", "#f1a02b"),
        "success": ("#0C2B1B", "#4ade80", "#22C55E"),
        "danger":  ("#371318", "#f87171", "#ef4444"),
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
    font-size:12px;color:#bdc8d1;font-family:'Inter',sans-serif;">
    <div style="width:12px;height:12px;border-radius:50%;
      background:#f87171;border:1.5px solid #ef4444">
    </div>Red – critical
  </div>
  <div style="display:flex;align-items:center;gap:5px;
    font-size:12px;color:#bdc8d1;font-family:'Inter',sans-serif;">
    <div style="width:12px;height:12px;border-radius:50%;
      background:#ffc176;border:1.5px solid #f1a02b">
    </div>Yellow – emergency
  </div>
  <div style="display:flex;align-items:center;gap:5px;
    font-size:12px;color:#bdc8d1;font-family:'Inter',sans-serif;">
    <div style="width:12px;height:12px;border-radius:50%;
      background:#4ade80;border:1.5px solid #22c55e">
    </div>Green – urgent
  </div>
  <div style="display:flex;align-items:center;gap:5px;
    font-size:12px;color:#bdc8d1;font-family:'Inter',sans-serif;">
    <div style="width:12px;height:12px;border-radius:50%;
      background:#303539;border:1.5px solid #bdc8d1">
    </div>White – non-urgent
  </div>
  <div style="display:flex;align-items:center;gap:5px;
    font-size:12px;color:#bdc8d1;font-family:'Inter',sans-serif;">
    <div style="width:12px;height:12px;border-radius:50%;
      background:#1b2024;border:1.5px solid #3e484f">
    </div>Black – DOA
  </div>
</div>""", unsafe_allow_html=True)


def render_risk_card(label: str, probability: float, description: str):
    if probability < 10.0:
        color = "#4ade80"
        bg = "#0C2B1B"
        border = "rgba(74, 222, 128, 0.2)"
        status = "Low Risk"
    elif probability < 40.0:
        color = "#ffc176"
        bg = "#2B2211"
        border = "rgba(255, 193, 118, 0.2)"
        status = "Moderate Risk"
    else:
        color = "#f87171"
        bg = "#371318"
        border = "rgba(248, 113, 113, 0.2)"
        status = "High Risk"
        
    card_html = f"""
    <div style="background:{bg}; border: 1px solid {border}; border-top: 4px solid {color}; border-radius: 10px; padding: 1.2rem; min-height: 140px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); margin-bottom: 12px;">
      <div style="font-size: 0.72rem; color: #bdc8d1; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem;">{label}</div>
      <div style="font-size: 2.2rem; font-family: 'JetBrains Mono', monospace; font-weight: 700; color: white; line-height: 1.1; margin-bottom: 0.2rem;">{probability:.1f}%</div>
      <div style="font-size: 0.78rem; font-weight: 600; color: {color}; margin-bottom: 0.5rem;">{status}</div>
      <div style="font-size: 0.75rem; color: #bdc8d1; line-height: 1.4;">{description}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
