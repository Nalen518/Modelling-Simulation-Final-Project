import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="IGD Simulation | DTETI UGM",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

from dashboard.styles import (
    inject_css, render_header, render_section,
    render_info, render_priority_legend
)
from dashboard.animation_component import (
    render_animation
)

inject_css()

PLOTLY_LAYOUT = dict(
    font_family="Inter, sans-serif",
    font_color="#E2E8F0",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=44, b=32, l=16, r=16),
    legend=dict(
        bgcolor="rgba(28, 37, 65, 0.95)",
        bordercolor="#3A506B",
        borderwidth=1,
        font_size=11,
    ),
    xaxis=dict(
        gridcolor="rgba(255, 255, 255, 0.06)",
        linecolor="#3A506B",
        tickfont_size=11,
        title_font_size=12,
    ),
    yaxis=dict(
        gridcolor="rgba(255, 255, 255, 0.06)",
        linecolor="#3A506B",
        tickfont_size=11,
        title_font_size=12,
    ),
)

PRIORITY_COLORS = {
    1: "#C0392B", 2: "#B7950B",
    3: "#1A7A4A", 4: "#95A5A6", 5: "#2C3E50"
}
PRIORITY_NAMES = {
    1: "Red", 2: "Yellow",
    3: "Green", 4: "White", 5: "Black"
}
GRAY = "#95A5A6"

# ── SIDEBAR ───────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="padding:1.2rem 0 0.5rem;
  text-align:center;">
  <div style="font-size:2rem;">🏥</div>
  <div style="font-family:DM Sans,sans-serif;
    font-size:1.05rem;font-weight:700;
    color:white;margin-top:.3rem;">
    IGD Simulation
  </div>
  <div style="font-size:.72rem;
    color:rgba(255,255,255,.55);
    letter-spacing:.06em;
    text-transform:uppercase;
    margin-top:.2rem;">
    DTETI · UGM
  </div>
</div>
<hr style="border-color:rgba(255,255,255,.12);
  margin:.75rem 0 1rem;">
""", unsafe_allow_html=True)

    st.markdown(
        '<p style="font-size:.68rem;font-weight:700;'
        'letter-spacing:.10em;text-transform:uppercase;'
        'color:rgba(255,255,255,.50);'
        'margin-bottom:.5rem;">Patient Arrivals</p>',
        unsafe_allow_html=True)
    lam = st.slider(
        "Arrival Rate (λ) pts/hr", 1, 50, 20)

    st.markdown(
        '<hr style="border-color:rgba(255,255,255,.10);'
        'margin:.9rem 0;">',
        unsafe_allow_html=True)

    st.markdown(
        '<p style="font-size:.68rem;font-weight:700;'
        'letter-spacing:.10em;text-transform:uppercase;'
        'color:rgba(255,255,255,.50);'
        'margin-bottom:.5rem;">Staffing</p>',
        unsafe_allow_html=True)
    n_doctors = st.slider("Doctors (c)", 1, 10, 3)
    n_nurses  = st.slider("Triage Nurses (s)", 1, 5, 1)
    n_reg     = st.slider(
        "Registration Officers", 1, 3, 1)

    st.markdown(
        '<hr style="border-color:rgba(255,255,255,.10);'
        'margin:.9rem 0;">',
        unsafe_allow_html=True)

    st.markdown(
        '<p style="font-size:.68rem;font-weight:700;'
        'letter-spacing:.10em;text-transform:uppercase;'
        'color:rgba(255,255,255,.50);'
        'margin-bottom:.5rem;">Simulation</p>',
        unsafe_allow_html=True)
    duration = st.slider(
        "Duration (minutes)", 60, 1440, 480, step=60)

    st.markdown(
        '<hr style="border-color:rgba(255,255,255,.10);'
        'margin:.9rem 0;">',
        unsafe_allow_html=True)

    st.markdown(
        '<p style="font-size:.68rem;font-weight:700;'
        'letter-spacing:.10em;text-transform:uppercase;'
        'color:rgba(255,255,255,.50);'
        'margin-bottom:.5rem;">'
        'Triage Distribution</p>',
        unsafe_allow_html=True)

    with st.expander("Configure Probabilities"):
        red_p    = st.slider("Red",    0, 20,  5)
        yellow_p = st.slider("Yellow", 0, 40, 20)
        green_p  = st.slider("Green",  0, 70, 55)
        white_p  = st.slider("White",  0, 40, 19)
        black_p  = st.slider("Black",  0,  5,  1)
        total_p  = (red_p + yellow_p + green_p
                    + white_p + black_p)
        if total_p != 100:
            st.warning(
                f"Sum = {total_p}% (need 100%)")
        else:
            st.success("Sum = 100%")

    triage_probs = [
        red_p/100, yellow_p/100, green_p/100,
        white_p/100, black_p/100
    ]

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="background:rgba(255,255,255,.07);'
        f'border:1px solid rgba(255,255,255,.12);'
        f'border-radius:8px;padding:.85rem 1rem;'
        f'font-size:.78rem;'
        f'color:rgba(255,255,255,.80);'
        f'font-family:DM Mono,monospace;'
        f'line-height:1.8;">'
        f'λ = {lam} pts/hr<br>'
        f'c = {n_doctors} doctors<br>'
        f's = {n_nurses} nurses<br>'
        f'T = {duration} min</div>',
        unsafe_allow_html=True)

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

col_btn, col_info = st.columns([1, 3], gap="medium")
with col_btn:
    run_btn = st.button(
        "Run Simulation",
        type="primary",
        use_container_width=True)
with col_info:
    render_info(
        f"<b>Config:</b> λ={lam} pts/hr &nbsp;·&nbsp;"
        f" {n_doctors} doctors &nbsp;·&nbsp;"
        f" {n_nurses} nurse(s) &nbsp;·&nbsp;"
        f" {duration} min &nbsp;·&nbsp;"
        f" Threshold: <b>Kemenkes 10 min</b>",
        "info")

tab_anim, tab_sim, tab_sa, tab_mc = st.tabs([
    "Animation",
    "Simulation",
    "Sensitivity Analysis",
    "Monte Carlo",
])

# ══════════════════════════════════════════════════════
# TAB 0 — ANIMATION
# ══════════════════════════════════════════════════════
with tab_anim:
    st.markdown("<br>", unsafe_allow_html=True)
    render_info(
        "Watch patients move through each IGD stage "
        "in real time. Use the <b>Speed</b> and "
        "<b>Doctors</b> sliders inside the animation "
        "to adjust live. Hover any patient dot "
        "to see their details.",
        "info")
    render_animation(duration=duration, height=680)

# ══════════════════════════════════════════════════════
# TAB 1 — SIMULATION
# ══════════════════════════════════════════════════════
with tab_sim:

    if not run_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        render_info(
            "Configure parameters in the sidebar "
            "then click <b>Run Simulation</b>. "
            "The SimPy engine will produce real "
            "results from your exact parameters.",
            "info")
        render_priority_legend()

    if run_btn:
        try:
            from simulation.model import IGDSimulation
            from simulation.analysis import (
                compute_metrics)
            SIM_OK = True
        except ImportError:
            SIM_OK = False
            render_info(
                "SimPy engine not found. "
                "Run <code>pip install simpy</code> "
                "and ensure simulation/ is present.",
                "danger")

        if SIM_OK:
            render_section(
                "Real-time Patient Flow", "LIVE")
            anim_ph = st.empty()
            state_log = []

            STAGE_LABELS = [
                "Arrival","Registration","Triage",
                "Queue","Treatment","Exit"
            ]
            STAGE_KEYS = [
                "arrival","registration","triage",
                "queue","treatment","exit"
            ]
            STAGE_COLORS = [
                "#2E86C1","#B7950B","#6C3483",
                "#C0392B","#1A7A4A","#95A5A6"
            ]

            def on_state(state):
                state_log.append(state)
                counts = [
                    state["stage_counts"].get(k, 0)
                    for k in STAGE_KEYS
                ]
                fig = go.Figure(go.Bar(
                    x=STAGE_LABELS,
                    y=counts,
                    marker_color=STAGE_COLORS,
                    marker_line_width=0,
                    text=counts,
                    textposition="outside",
                    textfont=dict(
                        family="JetBrains Mono,monospace",
                        size=12, color="#F1F5F9"),
                ))
                fig.update_layout(
                    **PLOTLY_LAYOUT,
                    title=dict(
                        text=(f"Patient Flow  —  "
                              f"t = "
                              f"{state['time']:.1f}"
                              f" min"),
                        font=dict(size=13,
                                  color="#F1F5F9",
                                  family="Raleway, sans-serif"),
                        x=0, xanchor="left",
                        pad=dict(l=8)),
                    yaxis_title="Patients",
                    height=300,
                    bargap=0.25,
                    yaxis_rangemode="tozero",
                )
                anim_ph.plotly_chart(
                    fig, use_container_width=True)
                time.sleep(0.004)

            with st.spinner(
                "Running simulation…"
            ):
                sim = IGDSimulation(
                    params,
                    state_callback=on_state)
                result = sim.run()

            patients = result["patients"]
            metrics  = compute_metrics(
                result,
                n_doctors=n_doctors)
            treated  = [
                p for p in patients
                if p.exit_type not in ("DOA","")]

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
                                opacity=0.75,
                                nbinsx=20,
                            ))
                fig_wait.update_layout(
                    **PLOTLY_LAYOUT,
                    title="Waiting Time Distribution",
                    xaxis_title="Wait (min)",
                    yaxis_title="Patients",
                    barmode="overlay",
                    height=300,
                    legend_title="Priority",
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
                    hole=0.5,
                    marker_colors=[
                        PRIORITY_COLORS[k]
                        for k in [1,2,3,4,5]
                        if PRIORITY_NAMES[k]
                        in counts
                    ],
                    textinfo="label+percent",
                    textfont_size=11,
                ))
                fig_pie.update_layout(
                    **PLOTLY_LAYOUT,
                    title="Priority Breakdown",
                    height=300,
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
                    ("Discharged","#1A7A4A"),
                    ("Admitted",  "#C0392B"),
                ]:
                    fig_exit.add_trace(go.Bar(
                        x=list(exit_data.keys()),
                        y=[exit_data[p][outcome]
                           for p in exit_data],
                        name=outcome,
                        marker_color=color,
                        marker_line_width=0,
                    ))
                fig_exit.update_layout(
                    **PLOTLY_LAYOUT,
                    title="Discharge vs Admission",
                    barmode="stack",
                    height=300,
                )
                st.plotly_chart(
                    fig_exit,
                    use_container_width=True)

            with ch4:
                fig_g = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=metrics["utilization"],
                    delta={"reference": 75},
                    title={"text": "Doctor Utilization %", "font": {"size": 13, "color": "#F1F5F9", "family": "Raleway, sans-serif"}},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": "#94A3B8"},
                        "bar": {"color": "#06B6D4", "thickness": 0.25},
                        "steps": [
                            {"range": [0, 60], "color": "#1C2541"},
                            {"range": [60, 90], "color": "#1B4332"},
                            {"range": [90, 100], "color": "#4A1525"},
                        ],
                        "threshold": {
                            "line": {"color": "#EF4444", "width": 2},
                            "value": 90
                        },
                    },
                    number={"suffix": "%", "font": {"family": "JetBrains Mono, monospace", "size": 32, "color": "#F1F5F9"}},
                ))
                fig_g.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_family="Inter, sans-serif",
                    font_color="#F1F5F9",
                    height=300,
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
        "<b>Sensitivity Analysis</b> runs single DES "
        "simulations across multiple parameter values. "
        "Experiment A varies doctor count at λ=20. "
        "Experiment B varies arrival rate at c=3.",
        "info")
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

    mc_q1_tab, mc_q2_tab, mc_q3_tab = st.tabs([
        "Q1 — Doctors Needed",
        "Q2 — P(Overload)",
        "Q3 — Critical Risk",
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
