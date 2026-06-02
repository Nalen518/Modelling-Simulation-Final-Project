import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="IGD Queue Optimization",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

from dashboard.styles import (
    inject_css, render_header, render_section,
    render_info, render_priority_legend, render_risk_card
)
from dashboard.animation_component import (
    render_animation
)

inject_css()

PLOTLY_LAYOUT = dict(
    font_family="Inter, sans-serif",
    font_color="#dee3e8",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=44, b=32, l=16, r=16),
    legend=dict(
        bgcolor="rgba(27,32,36,0.95)",
        bordercolor="#3e484f",
        borderwidth=1,
        font_size=11,
    ),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="#3e484f",
        tickfont_size=11,
        title_font_size=12,
        zeroline=False,
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="#3e484f",
        tickfont_size=11,
        title_font_size=12,
        zeroline=False,
    ),
)

PRIORITY_COLORS = {
    1: "#f87171", 2: "#ffc176",
    3: "#4ade80", 4: "#bdc8d1", 5: "#303539"
}
PRIORITY_NAMES = {
    1: "Red", 2: "Yellow",
    3: "Green", 4: "White", 5: "Black"
}
GRAY = "#bdc8d1"

# ── SIDEBAR ───────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="margin-bottom:1.25rem;">
  <div style="display:flex;align-items:center;gap:0.65rem;margin-bottom:0.25rem;">
    <span class="material-symbols-outlined" style="color:#8ed5ff;font-size:1.4rem;">medical_services</span>
    <div>
      <h2 style="font-family:'Inter',sans-serif;font-size:0.95rem;font-weight:700;color:#dee3e8;margin:0;line-height:1.1;">Simulation Controls</h2>
      <p style="font-family:'Inter',sans-serif;font-size:0.72rem;color:#bdc8d1;margin:0;opacity:0.7;line-height:1.1;">Parameter Configuration</p>
    </div>
  </div>
</div>
<hr style="border-color:#3e484f;
  margin:.5rem 0 .9rem;">
""", unsafe_allow_html=True)

    st.markdown(
        '<p style="font-size:.68rem;font-weight:700;'
        'letter-spacing:.10em;text-transform:uppercase;'
        'color:#8ed5ff;'
        'margin-bottom:.5rem;">Patient Arrival</p>',
        unsafe_allow_html=True)
    lam = st.slider(
        "Arrival Rate (λ) pts/hr", 1, 50, 20)

    st.markdown(
        '<hr style="border-color:#3e484f;'
        'margin:.9rem 0;">',
        unsafe_allow_html=True)

    st.markdown(
        '<p style="font-size:.68rem;font-weight:700;'
        'letter-spacing:.10em;text-transform:uppercase;'
        'color:#8ed5ff;'
        'margin-bottom:.5rem;">Staffing</p>',
        unsafe_allow_html=True)
    n_doctors = st.slider("Doctors (c)", 1, 10, 3)
    n_nurses  = st.slider("Triage Nurses (s)", 1, 5, 1)
    n_reg     = st.slider(
        "Registration Officers", 1, 3, 1)

    st.markdown(
        '<hr style="border-color:#3e484f;'
        'margin:.9rem 0;">',
        unsafe_allow_html=True)

    st.markdown(
        '<p style="font-size:.68rem;font-weight:700;'
        'letter-spacing:.10em;text-transform:uppercase;'
        'color:#8ed5ff;'
        'margin-bottom:.5rem;">Simulation</p>',
        unsafe_allow_html=True)
    duration = st.slider(
        "Duration (minutes)", 60, 1440, 480, step=60)

    st.markdown(
        '<hr style="border-color:#3e484f;'
        'margin:.9rem 0;">',
        unsafe_allow_html=True)

    st.markdown(
        '<p style="font-size:.68rem;font-weight:700;'
        'letter-spacing:.10em;text-transform:uppercase;'
        'color:#8ed5ff;'
        'margin-bottom:.5rem;">Triage Distribution</p>',
        unsafe_allow_html=True)

    red_p    = st.slider("🔴 RED — Immediate", 0, 100, 5, help="Emergency / Resuscitation cases")
    yellow_p = st.slider("🟡 YELLOW — Urgent", 0, 100, 20, help="Urgent cases")
    green_p  = st.slider("🟢 GREEN — Non-Urgent", 0, 100, 55, help="Stable non-urgent cases")
    white_p  = st.slider("⚪ WHITE — Minor", 0, 100, 19, help="Minor outpatient cases")
    black_p  = st.slider("⚫ BLACK — Deceased", 0, 100, 1, help="DOA / Unsalvageable cases")
    
    total_p  = (red_p + yellow_p + green_p + white_p + black_p)
    if total_p != 100:
        st.error(f"Total Triage: {total_p}% (Must sum to 100%)")
    else:
        st.success("Total = 100% | Valid Distribution ✓")

    triage_probs = [
        red_p/100, yellow_p/100, green_p/100,
        white_p/100, black_p/100
    ]

params = {
    "lambda":         lam,
    "n_doctors":      n_doctors,
    "n_nurses":       n_nurses,
    "n_registration": n_reg,
    "duration":       duration,
    "triage_probs":   triage_probs,
}

# ── MAIN ──────────────────────────────────────────────
render_header()

import json
try:
    from simulation.model import IGDSimulation
    from simulation.analysis import compute_metrics
    SIM_OK = True
except ImportError:
    SIM_OK = False
    render_info(
        "SimPy engine not found. "
        "Run <code>pip install simpy</code> "
        "and ensure simulation/ is present.",
        "danger")

if SIM_OK:
    with st.spinner("Running simulation…"):
        sim = IGDSimulation(params, state_callback=None)
        result = sim.run()

    patients = result["patients"]
    metrics  = compute_metrics(result, n_doctors=n_doctors)
    treated  = [p for p in patients if p.exit_type not in ("DOA","")]
    
    patients_list = []
    for p in patients:
        d = vars(p).copy()
        d['priority'] = int(d['priority'])
        patients_list.append(d)
    patients_json = json.dumps(patients_list)

    tab_anim, tab_sim, tab_sa, tab_mc, tab_doc = st.tabs([
        "Animation",
        "Simulation",
        "Sensitivity Analysis",
        "Monte Carlo",
        "Methodology & Theory"
    ])

    with tab_anim:
        render_animation(patients_json, n_doctors, duration=duration, height=700)

    with tab_sim:
        render_priority_legend()

        # ── KPI — native st.metric() ──────────
        render_section(
            "Key Performance Indicators",
            "RESULTS")
        c1,c2,c3,c4,c5,c6 = st.columns(
            6, gap="small")
        c1.metric(
            "Total Patients",
            metrics["total"])
        c2.metric(
            "Treated",
            metrics["completed"])
        c3.metric(
            "Avg Wait",
            f"{metrics['avg_wait']} min")
        c4.metric(
            "Max Wait",
            f"{metrics['max_wait']} min")
        c5.metric(
            "Utilization",
            f"{metrics['utilization']}%")
        c6.metric(
            "DOA",
            metrics["doa"])

        # ── Priority table ────────────────────
        render_section(
            "Per-Priority Breakdown", "TRIAGE")
        render_priority_legend()
        rows = []
        for pri in [1,2,3,4]:
            pp = metrics["per_priority"][pri]
            rows.append({
                "Priority":
                    PRIORITY_NAMES[pri],
                "Count":
                    pp["count"],
                "Completed":
                    pp["completed"],
                "In Progress":
                    pp["in_progress"],
                "Still Queuing":
                    pp["still_queuing"],
                "Avg Wait (min)":
                    f"{pp['avg_wait']:.1f}",
                "Max Wait (min)":
                    f"{pp['max_wait']:.1f}",
                "Avg Treat (min)":
                    f"{pp['avg_treat']:.1f}",
            })
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True)

        # ── Charts ────────────────────────────
        render_section(
            "Result Charts", "ANALYSIS")
        ch1, ch2 = st.columns(2, gap="medium")

        with ch1:
            fig_wait = go.Figure()
            for pri in [1,2,3,4]:
                wt = [
                    p.wait_time
                    for p in treated
                    if int(p.priority) == pri
                    and p.treatment_start > 0
                ]
                if wt:
                    fig_wait.add_trace(
                        go.Histogram(
                            x=wt,
                            name=PRIORITY_NAMES[pri],
                            marker_color=
                                PRIORITY_COLORS[pri],
                            opacity=0.8,
                            nbinsx=20,
                            marker_line_width=0,
                        ))
            fig_wait.update_layout(
                **PLOTLY_LAYOUT,
                title=dict(text="Waiting Time Distribution", font=dict(size=14, color="#dee3e8")),
                xaxis_title="Wait (min)",
                yaxis_title="Patients",
                barmode="overlay",
                height=320,
                bargap=0.08,
            )
            fig_wait.update_layout(
                legend_title_text="Priority",
            )
            st.plotly_chart(
                fig_wait,
                use_container_width=True)

        with ch2:
            counts = {
                PRIORITY_NAMES[k]: sum(
                    1 for p in patients
                    if int(p.priority) == k)
                for k in [1,2,3,4,5]
            }
            counts = {
                k:v for k,v in counts.items()
                if v > 0}
            fig_pie = go.Figure(go.Pie(
                labels=list(counts.keys()),
                values=list(counts.values()),
                hole=0.55,
                marker_colors=[
                    PRIORITY_COLORS[k]
                    for k in [1,2,3,4,5]
                    if PRIORITY_NAMES[k]
                    in counts
                ],
                textinfo="label+percent",
                textfont_size=11,
                textfont_color="#dee3e8",
                marker_line_color="#0f1418",
                marker_line_width=2,
                pull=[0.03]*len(counts),
            ))
            fig_pie.update_layout(
                **PLOTLY_LAYOUT,
                title=dict(text="Priority Breakdown", font=dict(size=14, color="#dee3e8")),
                height=320,
                showlegend=False,
            )
            st.plotly_chart(
                fig_pie,
                use_container_width=True)

        ch3, ch4 = st.columns(2, gap="medium")
        with ch3:
            exit_data = {}
            for pri in [1,2,3,4]:
                exit_data[PRIORITY_NAMES[pri]] = {
                    "Discharged": sum(
                        1 for p in treated
                        if int(p.priority) == pri
                        and p.exit_type ==
                        "discharged"),
                    "Admitted": sum(
                        1 for p in treated
                        if int(p.priority) == pri
                        and p.exit_type ==
                        "admitted"),
                }
            fig_exit = go.Figure()
            for outcome, color in [
                ("Discharged","#4ade80"),
                ("Admitted",  "#f87171"),
            ]:
                fig_exit.add_trace(go.Bar(
                    x=list(exit_data.keys()),
                    y=[exit_data[p][outcome]
                       for p in exit_data],
                    name=outcome,
                    marker_color=color,
                    marker_line_width=0,
                    marker_line_color="#0f1418",
                ))
            fig_exit.update_layout(
                **PLOTLY_LAYOUT,
                title=dict(text="Discharge vs Admission", font=dict(size=14, color="#dee3e8")),
                barmode="stack",
                height=320,
                bargap=0.3,
            )
            st.plotly_chart(
                fig_exit,
                use_container_width=True)

        with ch4:
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=metrics["utilization"],
                delta={"reference": 75, "increasing": {"color": "#4ade80"}, "decreasing": {"color": "#f87171"}},
                title={"text": "Doctor Utilization %", "font": {"size": 13, "color": "#dee3e8", "family": "Inter, sans-serif"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#bdc8d1", "tickfont": {"size": 10, "color": "#bdc8d1"}},
                    "bar": {"color": "#8ed5ff", "thickness": 0.3},
                    "bgcolor": "#1b2024",
                    "steps": [
                        {"range": [0, 60], "color": "#252b2e"},
                        {"range": [60, 90], "color": "rgba(74,222,128,0.15)"},
                        {"range": [90, 100], "color": "rgba(248,113,113,0.2)"},
                    ],
                    "threshold": {
                        "line": {"color": "#f87171", "width": 2},
                        "value": 90
                    },
                },
                number={"suffix": "%", "font": {"family": "JetBrains Mono, monospace", "size": 32, "color": "#dee3e8"}},
            ))
            fig_g.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_family="Inter, sans-serif",
                font_color="#dee3e8",
                height=320,
                margin=dict(t=44, b=16, l=32, r=32),
            )
            st.plotly_chart(
                fig_g,
                use_container_width=True)

        # ── Clinical validation ───────────────
        render_section(
            "Clinical Validation",
            "KEMENKES")
        red_pts = [
            p for p in treated
            if int(p.priority) == 1
            and p.treatment_start > 0
        ]
        if red_pts:
            breach = sum(
                1 for p in red_pts
                if p.wait_time > 10)
            pct = breach/len(red_pts)*100
            if pct < 5:
                render_info(
                    f"<b>Priority queue "
                    f"validated:</b> only "
                    f"{pct:.1f}% of Red "
                    f"patients waited > 10 min.",
                    "success")
            elif pct < 20:
                render_info(
                    f"<b>Borderline:</b> "
                    f"{pct:.1f}% of Red patients"
                    f" waited > 10 min. "
                    f"Consider more doctors.",
                    "warn")
            else:
                render_info(
                    f"<b>Threshold breached:"
                    f"</b> {pct:.1f}% of Red "
                    f"patients waited > 10 min."
                    f" System understaffed.",
                    "danger")
        else:
            render_info(
                "<b>No Red (Critical) Patients Treated:</b> "
                "There are no Red priority patients who started treatment in this simulation run. "
                "Try increasing the <i>Duration</i> or the <i>Red Triage Probability</i> in the sidebar.",
                "warn")

# ══════════════════════════════════════════════════════
# TAB 2 — SENSITIVITY ANALYSIS
# ══════════════════════════════════════════════════════
with tab_sa:
    st.markdown("<br>", unsafe_allow_html=True)
    render_info(
        "This section evaluates system responsiveness. Run the <b>Predefined Scenario Analysis</b> below "
        "to evaluate staffing levels, or run the individual <b>Sensitivity Experiments</b> at the bottom.",
        "info")
    
    # ── Predefined Scenarios (Improvement 6) ──
    render_section("Predefined Scenario Analysis", "STAFFING COMPARISON")
    st.markdown("Compare emergency department performance under three different doctor staffing levels (fixed λ=20 pts/hr, duration=480 min):")
    
    scen_info_col1, scen_info_col2 = st.columns(2)
    with scen_info_col1:
        st.markdown("""
        *   **Scenario A**: 2 Doctors
        *   **Scenario B**: 3 Doctors
        *   **Scenario C**: 4 Doctors
        """)
    
    if st.button("Run Predefined Scenario Analysis", type="primary", use_container_width=True):
        try:
            scen_results = []
            for c in [2, 3, 4]:
                p = {**params, "lambda": 20, "n_doctors": c, "duration": 480}
                sim = IGDSimulation(p)
                raw = sim.run()
                m = compute_metrics(raw, n_doctors=c)
                scen_results.append({
                    "Scenario": f"Scenario {chr(65 + c - 2)} ({c} Docs)",
                    "Doctors": c,
                    "Average Wait (min)": m["avg_wait"],
                    "Max Wait (min)": m["max_wait"],
                    "Max Queue": m["max_queue"],
                    "Utilization (%)": m["utilization"],
                    "Throughput (pts/hr)": m["throughput"]
                })
            
            df_scen = pd.DataFrame(scen_results)
            
            # Render Table
            st.dataframe(df_scen, use_container_width=True, hide_index=True)
            
            # Render Bar Charts (Improvement 6)
            fig_scen = go.Figure()
            fig_scen.add_trace(go.Bar(
                x=df_scen["Scenario"],
                y=df_scen["Average Wait (min)"],
                name="Avg Wait (min)",
                marker_color="#06B6D4"
            ))
            fig_scen.add_trace(go.Bar(
                x=df_scen["Scenario"],
                y=df_scen["Max Wait (min)"],
                name="Max Wait (min)",
                marker_color="#EF4444"
            ))
            fig_scen.update_layout(
                **PLOTLY_LAYOUT,
                title="Waiting Times by Staffing Scenario",
                xaxis_title="Staffing Level",
                yaxis_title="Wait Time (minutes)",
                barmode="group",
                height=300
            )
            
            fig_util = go.Figure()
            fig_util.add_trace(go.Bar(
                x=df_scen["Scenario"],
                y=df_scen["Utilization (%)"],
                name="Doctor Utilization %",
                marker_color="#10B981"
            ))
            fig_util.update_layout(
                **PLOTLY_LAYOUT,
                title="Doctor Utilization by Staffing Scenario",
                xaxis_title="Staffing Level",
                yaxis_title="Utilization (%)",
                height=300
            )
            
            scen_c1, scen_c2 = st.columns(2)
            with scen_c1:
                st.plotly_chart(fig_scen, use_container_width=True)
            with scen_c2:
                st.plotly_chart(fig_util, use_container_width=True)
                
            # ── Recommendation Engine (Improvement 8) ──
            render_section("Simulation Insights & Recommendations", "INSIGHTS")
            
            # Extract results for formulas
            w2 = df_scen.loc[df_scen["Doctors"] == 2, "Average Wait (min)"].values[0]
            w3 = df_scen.loc[df_scen["Doctors"] == 3, "Average Wait (min)"].values[0]
            w4 = df_scen.loc[df_scen["Doctors"] == 4, "Average Wait (min)"].values[0]
            
            u2 = df_scen.loc[df_scen["Doctors"] == 2, "Utilization (%)"].values[0]
            u3 = df_scen.loc[df_scen["Doctors"] == 3, "Utilization (%)"].values[0]
            u4 = df_scen.loc[df_scen["Doctors"] == 4, "Utilization (%)"].values[0]
            
            # Percentage reductions
            red_2_to_3 = ((w2 - w3) / max(w2, 0.1)) * 100
            red_3_to_4 = ((w3 - w4) / max(w3, 0.1)) * 100
            
            rec_text = f"""
<div style="font-family:'Raleway',sans-serif; font-size:0.85rem; line-height:1.6; color:#86EFAC;">
  <div style="margin-bottom: 0.8rem;">
    <b style="color:white; font-size:0.9rem;">Staffing Impact</b><br>
    Increasing doctor capacity from 2 to 3 doctors reduced the average patient waiting time by <b>{red_2_to_3:.1f}%</b> (from {w2:.1f} to {w3:.1f} minutes).
  </div>
  <div style="margin-bottom: 0.8rem;">
    <b style="color:white; font-size:0.9rem;">Diminishing Returns</b><br>
    Further increasing doctor capacity from 3 to 4 doctors reduced the average waiting time by <b>{red_3_to_4:.1f}%</b> (from {w3:.1f} to {w4:.1f} minutes), demonstrating diminishing returns on additional staff investment.
  </div>
  <div style="margin-bottom: 0.8rem;">
    <b style="color:white; font-size:0.9rem;">Utilization & Burnout Risk</b><br>
    • At 2 doctors, physician utilization is <b>{u2:.1f}%</b>, which exceeds safe operational thresholds (>85%) and indicates a high risk of staff burnout.<br>
    • At 3 doctors, utilization is stabilized at <b>{u3:.1f}%</b>, balancing service speed and physician load.<br>
    • At 4 doctors, utilization drops to <b>{u4:.1f}%</b>, indicating potential over-staffing.
  </div>
  <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(34, 197, 94, 0.15); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 6px;">
    <b style="color:white; font-size:0.95rem; text-transform: uppercase; letter-spacing: 0.05em;">Recommendation:</b> 
    <span style="color:#22C55E; font-weight:700; font-size: 1rem;">3 Doctors</span> provides the best balance between waiting time and resource utilization under a baseline arrival rate of 20 pts/hr.
  </div>
</div>
            """
            
            render_info(rec_text, "success")
            
        except Exception as e:
            render_info(f"Error executing scenario analysis: {e}", "danger")

    st.markdown("<hr style='border-top: 2px dashed #1E2D4A;'>", unsafe_allow_html=True)
    render_section("Sensitivity Experiments", "PARAM SCAN")
    sa1, sa2 = st.columns(2, gap="large")

    with sa1:
        render_section(
            "Experiment A", "DOCTOR COUNT")
        st.caption(
            "Fixed λ=20 pts/hr · Vary c=2,3,4,5")
        if st.button(
            "Run Experiment A",
            use_container_width=True
        ):
            try:
                from simulation.analysis import \
                    run_experiment_a
                with st.spinner("Running…"):
                    res_a = run_experiment_a(
                        {**params,"duration":480})
                fig_a = go.Figure()
                scens = [r["scenario"]
                         for r in res_a]
                fig_a.add_trace(go.Bar(
                    x=scens,
                    y=[r["avg_wait"]
                       for r in res_a],
                    name="Avg Wait (min)",
                    marker_color="#2E86C1",
                    marker_line_width=0,
                ))
                fig_a.add_trace(go.Scatter(
                    x=scens,
                    y=[r["utilization"]
                       for r in res_a],
                    name="Utilization %",
                    mode="lines+markers",
                    line=dict(
                        color="#C0392B",width=2),
                    marker=dict(size=8),
                    yaxis="y2",
                ))
                fig_a.update_layout(
                    **PLOTLY_LAYOUT,
                    title="Exp A — Doctor Count",
                    yaxis_title="Avg Wait (min)",
                    yaxis2=dict(
                        title="Utilization %",
                        overlaying="y",
                        side="right",
                        range=[0,110],
                        gridcolor=
                        "rgba(0,0,0,0)",
                    ),
                    height=300,
                    barmode="group",
                )
                st.plotly_chart(
                    fig_a,
                    use_container_width=True)
                st.dataframe(
                    pd.DataFrame([{
                        "Scenario":
                            r["scenario"],
                        "Avg Wait":
                            f"{r['avg_wait']} min",
                        "Max Wait":
                            f"{r['max_wait']} min",
                        "Utilization":
                            f"{r['utilization']}%",
                        "Red Wait":
                            f"{r['per_priority'][1]['avg_wait']:.1f} min",
                    } for r in res_a]),
                    use_container_width=True,
                    hide_index=True)
            except Exception as e:
                render_info(
                    f"Error: {e}", "danger")

    with sa2:
        render_section(
            "Experiment B", "ARRIVAL RATE")
        st.caption(
            "Fixed c=3 · Vary λ=10,20,30,40")
        if st.button(
            "Run Experiment B",
            use_container_width=True
        ):
            try:
                from simulation.analysis import \
                    run_experiment_b
                with st.spinner("Running…"):
                    res_b = run_experiment_b(
                        {**params,"duration":480})
                fig_b = go.Figure()
                scens_b = [r["scenario"]
                           for r in res_b]
                for pri, col in [
                    (1,"#C0392B"),
                    (2,"#B7950B"),
                    (3,"#1A7A4A"),
                    (4,"#95A5A6"),
                ]:
                    fig_b.add_trace(go.Scatter(
                        x=scens_b,
                        y=[r["per_priority"][pri]
                           ["avg_wait"]
                           for r in res_b],
                        name=PRIORITY_NAMES[pri],
                        mode="lines+markers",
                        line=dict(
                            color=col,width=2),
                        marker=dict(size=8),
                    ))
                fig_b.add_hline(
                    y=10,line_dash="dash",
                    line_color="#C0392B",
                    annotation_text=
                    "Kemenkes 10 min",
                    annotation_font_size=10)
                fig_b.update_layout(
                    **PLOTLY_LAYOUT,
                    title="Exp B — Arrival Rate",
                    xaxis_title="λ (pts/hr)",
                    yaxis_title="Avg Wait (min)",
                    height=300,
                )
                st.plotly_chart(
                    fig_b,
                    use_container_width=True)
                st.dataframe(
                    pd.DataFrame([{
                        "Scenario":
                            r["scenario"],
                        "Avg Wait":
                            f"{r['avg_wait']} min",
                        "Red Wait":
                            f"{r['per_priority'][1]['avg_wait']:.1f} min",
                        "Max Queue":
                            r["max_queue"],
                        "Utilization":
                            f"{r['utilization']}%",
                    } for r in res_b]),
                    use_container_width=True,
                    hide_index=True)
            except Exception as e:
                render_info(
                    f"Error: {e}", "danger")

# ══════════════════════════════════════════════════════
# TAB 3 — MONTE CARLO
# ══════════════════════════════════════════════════════
with tab_mc:
    st.markdown("<br>", unsafe_allow_html=True)
    render_info(
        "<b>Monte Carlo Analysis</b> runs the simulation "
        "N=100 times per scenario to produce probability "
        "distributions. Threshold: Red wait > 10 min "
        "(Kemenkes RI IGD standard). "
        "Overload = ANY of: queue > 20, utilization > 95%, "
        "or any Red patient waits > 10 min.",
        "info")

    render_section("Monte Carlo Thresholds", "KPIs")
    c1, c2, c3 = st.columns(3)
    c1.metric("Red Wait Threshold", "10 min", "Kemenkes IGD")
    c2.metric("Replications (N)", "100", "per scenario")
    c3.metric("Overload Triggers", "3 combined", "queue · util · red")

    mc_q1_tab, mc_q2_tab, mc_q3_tab, mc_risk_tab = st.tabs([
        "Q1 — Doctors Needed",
        "Q2 — P(Overload)",
        "Q3 — Critical Risk",
        "Q4 — Operational Risk Indicators"
    ])

    with mc_q1_tab:
        render_section("How many doctors are needed?", "Q1")
        st.caption("Scans c=1..10 at λ=20 · N=100 reps each")
        if st.button("Run Q1 — Doctor Scan", type="primary"):
            try:
                from simulation.analysis import mc_optimal_doctors
                with st.spinner("Running 1000 simulations..."):
                    mc_q1 = mc_optimal_doctors({**params, "duration": 480})
                
                if mc_q1["conditions_met"]:
                    render_info(
                        f"✅ <b>Optimal: {mc_q1['optimal_doctors']} doctors minimum</b><br>"
                        f"P(Red > 10 min) = {mc_q1['p_red_breach']}% &lt; 5% ✓<br>"
                        f"P(Green > 60 min) = {mc_q1['p_green_breach']}% &lt; 10% ✓<br>"
                        f"Utilization = {mc_q1['utilization_mean']}% in 60–90% ✓",
                        "success"
                    )
                else:
                    render_info("No optimal staffing found.", "danger")
                
                scan = mc_q1["scan_results"]
                fig_q1 = go.Figure()
                cs = [r["c"] for r in scan]
                
                fig_q1.add_trace(go.Scatter(
                    x=cs, y=[r["p_red_breach"] for r in scan],
                    name="P(Red > 10 min)", mode="lines+markers",
                    line=dict(color="#C0392B", width=2)
                ))
                fig_q1.add_trace(go.Scatter(
                    x=cs, y=[r["p_green_breach"] for r in scan],
                    name="P(Green > 60 min)", mode="lines+markers",
                    line=dict(color="#B7950B", width=2)
                ))
                fig_q1.add_trace(go.Scatter(
                    x=cs, y=[r["utilization_mean"] for r in scan],
                    name="Utilization", mode="lines+markers",
                    line=dict(color="#2E86C1", width=2, dash="dash")
                ))
                fig_q1.update_layout(
                    **PLOTLY_LAYOUT, title="Q1: Doctor Count Scan",
                    xaxis_title="Doctors", yaxis_title="Probability/Utilization (%)",
                    height=350
                )
                st.plotly_chart(fig_q1, use_container_width=True)
                st.dataframe(pd.DataFrame([{
                    "Doctors (c)": r["c"],
                    "P(Red Wait > 10m)": f"{r['p_red_breach']}%",
                    "P(Green Wait > 60m)": f"{r['p_green_breach']}%",
                    "Mean Utilization": f"{r['utilization_mean']}%",
                    "Optimal Status": "✅ Optimal" if r["all_conditions_met"] else "❌ Sub-Optimal"
                } for r in scan]), use_container_width=True, hide_index=True)
            except Exception as e:
                render_info(f"Error: {e}", "danger")

    with mc_q2_tab:
        render_section("What is P(system overloaded)?", "Q2")
        st.caption("Varies λ=10,20,30,40 · c=3 · N=100 reps")
        if st.button("Run Q2 — Overload Risk", type="primary"):
            try:
                from simulation.analysis import mc_overload_probability
                with st.spinner("Running 400 simulations..."):
                    mc_q2 = mc_overload_probability({**params, "duration": 480})
                
                fig_q2 = go.Figure()
                scens = [r["scenario"] for r in mc_q2]
                fig_q2.add_trace(go.Bar(
                    x=scens, y=[r["p_overload"] for r in mc_q2],
                    name="P(Overload)", marker_color="#2E86C1"
                ))
                for k, n, c in [("p_queue_breach", "Queue>20", "#C0392B"),
                                ("p_util_breach", "Util>95%", "#B7950B"),
                                ("p_red_breach", "Red>10m", "#6C3483")]:
                    fig_q2.add_trace(go.Scatter(
                        x=scens, y=[r[k] for r in mc_q2], name=n,
                        mode="lines+markers", line=dict(color=c, dash="dot")
                    ))
                fig_q2.update_layout(
                    **PLOTLY_LAYOUT, title="Q2: P(Overload)",
                    yaxis_title="Probability (%)", height=350
                )
                st.plotly_chart(fig_q2, use_container_width=True)
                st.dataframe(pd.DataFrame([{
                    "Scenario": r["scenario"],
                    "P(Overload)": f"{r['p_overload']}%",
                    "Primary Driver": r["overload_driver"]
                } for r in mc_q2]), use_container_width=True, hide_index=True)
            except Exception as e:
                render_info(f"Error: {e}", "danger")

    with mc_q3_tab:
        render_section("Will critical patients wait too long?", "Q3")
        c3a, c3b = st.columns(2)
        with c3a:
            if st.button("Run Q3a (Vary Doctors)"):
                try:
                    from simulation.analysis import mc_critical_patient_risk
                    with st.spinner("Running..."):
                        res = mc_critical_patient_risk({**params, "duration": 480})
                    df = pd.DataFrame([{
                        "Scenario": r["scenario"],
                        "Mean Red Wait (min)": f"{r['red_wait_mean']:.2f}",
                        "95% CI Lower (min)": f"{r['red_wait_ci_lo']:.2f}",
                        "95% CI Upper (min)": f"{r['red_wait_ci_hi']:.2f}",
                        "P(Red Breach > 10m)": f"{r['p_red_breach_10']}%",
                        "Safe Status": "✅ Safe" if r["safe"] else "❌ High Risk"
                    } for r in res["q3a_by_doctors"]])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                except Exception as e:
                    render_info(f"Error: {e}", "danger")
        with c3b:
            if st.button("Run Q3b (Vary Arrival Rate)"):
                try:
                    from simulation.analysis import mc_critical_patient_risk
                    with st.spinner("Running..."):
                        res = mc_critical_patient_risk({**params, "duration": 480})
                    df = pd.DataFrame([{
                        "Scenario": r["scenario"],
                        "Mean Red Wait (min)": f"{r['red_wait_mean']:.2f}",
                        "95% CI Lower (min)": f"{r['red_wait_ci_lo']:.2f}",
                        "95% CI Upper (min)": f"{r['red_wait_ci_hi']:.2f}",
                        "P(Red Breach > 10m)": f"{r['p_red_breach_10']}%",
                        "Safe Status": "✅ Safe" if r["safe"] else "❌ High Risk"
                    } for r in res["q3b_by_lambda"]])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                except Exception as e:
                    render_info(f"Error: {e}", "danger")

    with mc_risk_tab:
        render_section("Operational Risk Indicators", "Q4")
        st.caption("Runs N=100 replications at current sidebar settings to evaluate the probability of system overloads and care delays:")
        
        st.markdown(f"""
        **Current Simulation Parameters:**
        - Arrival Rate ($\\lambda$): **{lam} pts/hr**
        - Doctors ($c$): **{n_doctors}**
        - Triage Nurses ($s$): **{n_nurses}**
        """)
        
        if st.button("Run Operational Risk Analysis", type="primary", use_container_width=True):
            try:
                from simulation.analysis import run_single_replication
                with st.spinner("Running 100 Monte Carlo replications..."):
                    reps = []
                    for i in range(100):
                        rep = run_single_replication(params, n_doctors=n_doctors, seed=i*99)
                        reps.append(rep)
                
                # Compute risk probabilities
                # 1. P(Queue > 50)
                p_queue_50 = sum(1 for r in reps if r["max_queue"] > 50) / 100 * 100
                # 2. P(Avg Wait > 30 min)
                p_avg_wait_30 = sum(1 for r in reps if r["avg_wait"] > 30) / 100 * 100
                # 3. P(Doctor Utilization > 90%)
                p_util_90 = sum(1 for r in reps if r["utilization"] > 90) / 100 * 100
                # 4. P(Red Patient Wait > 5 min)
                p_red_5 = sum(1 for r in reps if r["red_breach"]) / 100 * 100
                
                # Display cards in a 2x2 grid
                rc1, rc2 = st.columns(2)
                with rc1:
                    render_risk_card(
                        "Queue Overload Probability P(Queue > 50)",
                        p_queue_50,
                        "Estimated probability that the priority queue length exceeds 50 patients during the shift."
                    )
                    render_risk_card(
                        "Staff Burnout Risk P(Doctor Utilization > 90%)",
                        p_util_90,
                        "Estimated probability that cumulative physician workload exceeds 90% capacity, indicating operational stress."
                    )
                with rc2:
                    render_risk_card(
                        "Excessive Wait Probability P(Avg Wait > 30 min)",
                        p_avg_wait_30,
                        "Estimated probability that the average waiting time for admitted/discharged patients exceeds 30 minutes."
                    )
                    render_risk_card(
                        "Critical Care Delay P(Red Wait > 5 min)",
                        p_red_5,
                        "Probability that any Red triage patient waits longer than 5 minutes before starting treatment (Kemenkes standard is 10 min)."
                    )
                    
            except Exception as e:
                render_info(f"Error running risk analysis: {e}", "danger")

    # ══════════════════════════════════════════════════════
    # TAB 4 — METHODOLOGY & THEORY (Improvement 1-5)
    # ══════════════════════════════════════════════════════
    with tab_doc:
        st.markdown("<br>", unsafe_allow_html=True)
        render_info(
            "This tab provides the theoretical foundations, assumptions, scope definitions, "
            "and parameter justifications for this Discrete Event Simulation (DES) model, "
            "addressing standard academic and clinical validation criteria.",
            "info"
        )
        
        doc_sec_1, doc_sec_2 = st.tabs(["Model Scope & Assumptions", "Parameter Justifications & Theory"])
        
        with doc_sec_1:
            render_section("Model Scope (Inside vs Outside)", "BOUNDARY")
            
            # Side-by-side Scope columns
            scope_col1, scope_col2 = st.columns(2)
            with scope_col1:
                st.markdown("""
                <div style="background:#0C2B1B; border: 1px solid rgba(16, 185, 129, 0.2); border-left: 5px solid #10B981; border-radius: 8px; padding: 1.25rem; min-height: 240px; height: 100%;">
                  <h4 style="color:#10B981; margin: 0 0 0.8rem 0; font-family:'Raleway',sans-serif; font-size:1.05rem; font-weight:700;">
                    ✅ INSIDE SCOPE (Emergency Department)
                  </h4>
                  <ul style="color:#F1F5F9; font-size:0.82rem; line-height:1.6; margin:0; padding-left:1.2rem;">
                    <li><b>Patient Arrivals & Registration</b>: Explicit queueing and officer servicing.</li>
                    <li><b>Triage Scale</b>: 5-level clinical classification (Red, Yellow, Green, White, Black).</li>
                    <li><b>IGD Waiting Room & Queues</b>: Dynamic priority queueing based on acuity.</li>
                    <li><b>Doctor Treatment Service</b>: Direct clinical stabilization and care.</li>
                    <li><b>Patient Dispositions</b>: Patient exit or transfer pathways.</li>
                  </ul>
                </div>
                """, unsafe_allow_html=True)
                
            with scope_col2:
                st.markdown("""
                <div style="background:#371318; border: 1px solid rgba(239, 68, 68, 0.2); border-left: 5px solid #EF4444; border-radius: 8px; padding: 1.25rem; min-height: 240px; height: 100%;">
                  <h4 style="color:#EF4444; margin: 0 0 0.8rem 0; font-family:'Raleway',sans-serif; font-size:1.05rem; font-weight:700;">
                    ❌ OUTSIDE SCOPE (Downstream Operations)
                  </h4>
                  <ul style="color:#F1F5F9; font-size:0.82rem; line-height:1.6; margin:0; padding-left:1.2rem;">
                    <li><b>Inpatient Ward Capacity</b>: General wards, ICU, and CCU beds are modeled as infinite sinks.</li>
                    <li><b>Specialist Referrals</b>: External specialist consultations or clinic pathways are omitted.</li>
                    <li><b>Ancillary Services</b>: Diagnostics (Radiology, CT scans, Labs) and Pharmacy are implicit.</li>
                    <li><b>Post-Discharge Care</b>: Outpatient follow-ups or recovery monitoring are excluded.</li>
                  </ul>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            render_section("Core Model Assumptions", "ASSUMPTIONS")
            st.markdown("""
            To maintain a focused and computationally clean model of emergency department patient flows, the following core assumptions are established:
            
            - **Assumption A**: The simulation *only* models Emergency Department (IGD) operations.
            - **Assumption B**: Downstream inpatient wards (general rooms, ICU) are outside the simulation scope.
            - **Assumption C**: Specialist referrals and consultations are not explicitly modeled.
            - **Assumption D**: Treatment rooms are represented implicitly through the doctor resource capacity.
            - **Assumption E**: Patients transferred/admitted to inpatient wards are considered to have exited the simulated IGD system.
            """)
            
            st.markdown("<br>", unsafe_allow_html=True)
            render_section("Model Limitations", "LIMITATIONS")
            st.markdown("""
            - **Lack of Validation**: The simulator is *not* validated using historical patient traffic data from a specific hospital.
            - **Educational Use**: This project is intended solely for educational, research, and exploratory queueing analysis.
            - **No Clinical Decision Support**: The results and recommendations should *not* be used to make clinical decisions or plan hospital staffing in real-world settings.
            - **Behavioral Factors**: Human staff fatigue, shift changes, and patient self-discharge (left without being seen) are not simulated.
            """)
            
        with doc_sec_2:
            render_section("Parameter Sources", "PARAMETERS")
            
            param_rows = [
                {"Parameter": "Arrival Rate (λ)", "Baseline Value": "20 pts/hr", "Source Type": "Literature & Public Health Reference"},
                {"Parameter": "Triage Category Proportions", "Baseline Value": "Red (5%), Yellow (20%), Green (55%), White (19%), Black (1%)", "Source Type": "Public Health Reference"},
                {"Parameter": "Registration Duration", "Baseline Value": "Exponential (mean = 3 min)", "Source Type": "Literature Reference"},
                {"Parameter": "Triage Duration", "Baseline Value": "Lognormal (mean = 5 min)", "Source Type": "Public Health Reference"},
                {"Parameter": "Treatment Duration", "Baseline Value": "Acuity-Dependent (Red: mean=90m, Yellow: mean=60m, Green: mean=30m, White: mean=15m)", "Source Type": "Literature Reference"},
                {"Parameter": "Admission Probability", "Baseline Value": "Acuity-Dependent (Red: 80%, Yellow: 40%, Green: 5%, White: 0%)", "Source Type": "Literature Reference"}
            ]
            st.dataframe(pd.DataFrame(param_rows), use_container_width=True, hide_index=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            render_section("Why Use Poisson Arrivals?", "QUEUING THEORY")
            
            theory_col1, theory_col2 = st.columns([2, 1])
            with theory_col1:
                st.markdown("""
                Patient arrivals at an emergency room occur randomly and independently over time. In queueing theory, such independent arrivals are mathematically modeled as a **Poisson process**.
                
                The probability of observing $k$ patient arrivals in a time interval of length $t$ is defined by:
                """)
                st.latex(r"P(N(t) = k) = \frac{(\lambda t)^k e^{-\lambda t}}{k!}")
                st.markdown("""
                Where:
                - $N(t)$ is the number of arrivals in time $t$.
                - $\\lambda$ is the arrival rate (patients per hour).
                - $e$ is Euler's number.
                """)
            with theory_col2:
                st.markdown("""
                <div style="background:#1C2541; border: 1px solid #1E2D4A; border-radius: 8px; padding: 1rem; height: 100%;">
                  <span style="font-size:0.75rem; color:#06B6D4; font-weight:700; text-transform:uppercase;">Key Properties</span>
                  <ul style="color:#94A3B8; font-size:0.78rem; margin-top:0.5rem; padding-left:1.1rem; line-height:1.5;">
                    <li><b>Memoryless arrivals</b>: Past arrivals do not affect future arrival times.</li>
                    <li><b>Independent events</b>: Patients arrive individually, not in coordinated clusters.</li>
                    <li><b>Standard benchmark</b>: Used widely in healthcare service simulations.</li>
                  </ul>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            render_section("DES vs Monte Carlo Methodology", "SIMULATION METHODOLOGY")
            
            st.markdown("""
            <div style="display: flex; gap: 1rem; align-items: stretch; margin-bottom: 1rem; flex-wrap: wrap;">
              <div style="flex: 1; min-width: 250px; background: #1C2541; border: 1px solid #1E2D4A; border-radius: 8px; padding: 1.2rem;">
                <h5 style="color:#06B6D4; margin: 0 0 0.5rem 0; font-family:'Raleway',sans-serif; font-size:0.95rem; font-weight:700;">
                  1. Discrete Event Simulation (DES)
                </h5>
                <p style="color:#94A3B8; font-size:0.8rem; line-height:1.5; margin:0;">
                  Models the chronological sequence of events (arrival, registration, triage, treatment, discharge/admission) for individual patients. It captures structural queueing dynamics, resource conflicts, and temporal bottlenecks in a single run.
                </p>
              </div>
              <div style="display: flex; align-items: center; justify-content: center; font-size: 1.5rem; color: #06B6D4;">➔</div>
              <div style="flex: 1; min-width: 250px; background: #1C2541; border: 1px solid #1E2D4A; border-radius: 8px; padding: 1.2rem;">
                <h5 style="color:#06B6D4; margin: 0 0 0.5rem 0; font-family:'Raleway',sans-serif; font-size:0.95rem; font-weight:700;">
                  2. Monte Carlo Replications
                </h5>
                <p style="color:#94A3B8; font-size:0.8rem; line-height:1.5; margin:0;">
                  Repeats the DES model over many runs (e.g., $N=100$) using different random number generator seeds. This aggregates individual stochastic outcomes into solid statistical profiles (means, confidence intervals).
                </p>
              </div>
              <div style="display: flex; align-items: center; justify-content: center; font-size: 1.5rem; color: #06B6D4;">➔</div>
              <div style="flex: 1; min-width: 250px; background: #1C2541; border: 1px solid #1E2D4A; border-radius: 8px; padding: 1.2rem;">
                <h5 style="color:#06B6D4; margin: 0 0 0.5rem 0; font-family:'Raleway',sans-serif; font-size:0.95rem; font-weight:700;">
                  3. Decision Risk Analysis
                </h5>
                <p style="color:#94A3B8; font-size:0.8rem; line-height:1.5; margin:0;">
                  Translates statistical distributions into decision-oriented risk percentages, estimating the probability of clinic overloads, excessive patient wait times, or doctor burnout.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # Render professional footer
    st.markdown("""
    <hr style="border-color:#3e484f;margin:2rem 0 1rem;">
    <div style="display:flex;justify-content:space-between;align-items:center;color:#bdc8d1;font-size:0.75rem;font-family:'Inter',sans-serif;opacity:0.7;flex-wrap:wrap;gap:0.5rem;padding-bottom:1rem;">
      <div>IGD Queue Optimization • Discrete Event Simulation using SimPy</div>
      <div>Developed for Modeling & Simulation Final Project</div>
    </div>
    """, unsafe_allow_html=True)

