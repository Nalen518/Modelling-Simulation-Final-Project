import plotly.graph_objects as go
import plotly.express as px

PRIORITY_COLORS = {
    1: "#f87171",  # Red
    2: "#ffc176",  # Yellow
    3: "#4ade80",  # Green
    4: "#bdc8d1",  # White/Gray
    5: "#303539",  # Black
}
PRIORITY_NAMES = {
    1: "Red", 2: "Yellow",
    3: "Green", 4: "White", 5: "Black"
}

# ── Shared dark-mode Plotly layout ──────────────────
_DARK_LAYOUT = dict(
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
        orientation="h",
        y=1.12,
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


def _get_priority(p):
    """Safely extract priority as plain int."""
    raw = p["priority"] if isinstance(p, dict) else p.priority
    return int(raw)

def _get_exit(p):
    """Safely extract exit_type as plain string."""
    raw = p["exit_type"] if isinstance(p, dict) else p.exit_type
    return str(raw)

def _get_wait(p):
    """Safely extract wait_time as float."""
    if isinstance(p, dict):
        return float(p.get("wait_time", 0))
    return float(p.wait_time)

def chart_wait_distribution(patients: list) -> go.Figure:
    """Histogram of wait times per priority."""
    fig = go.Figure()
    for pri in [1, 2, 3, 4]:
        pts = [_get_wait(p) for p in patients
               if _get_priority(p) == pri]
        if pts:
            fig.add_trace(go.Histogram(
                x=pts,
                name=PRIORITY_NAMES[pri],
                marker_color=PRIORITY_COLORS[pri],
                opacity=0.8,
                nbinsx=20,
                marker_line_width=0,
            ))
    fig.update_layout(
        **_DARK_LAYOUT,
        title=dict(text="Waiting Time Distribution by Priority", font=dict(size=14, color="#dee3e8")),
        xaxis_title="Wait Time (minutes)",
        yaxis_title="Patient Count",
        barmode="overlay",
        height=350,
        bargap=0.08,
    )
    return fig

def chart_priority_breakdown(patients: list) -> go.Figure:
    """Donut chart of priority distribution."""
    counts = {}
    for p in patients:
        pri = _get_priority(p)
        if pri in PRIORITY_NAMES:
            counts[pri] = counts.get(pri, 0) + 1
    # Ensure at least one entry for empty data
    if not counts:
        counts = {1: 0}
    fig = go.Figure(go.Pie(
        labels=[PRIORITY_NAMES[k] for k in counts],
        values=list(counts.values()),
        hole=0.55,
        marker_colors=[PRIORITY_COLORS[k] for k in counts],
        textinfo="label+percent",
        textfont_size=11,
        textfont_color="#dee3e8",
        marker_line_color="#0f1418",
        marker_line_width=2,
        pull=[0.03]*len(counts),
    ))
    fig.update_layout(
        **_DARK_LAYOUT,
        title=dict(text="Patient Priority Breakdown", font=dict(size=14, color="#dee3e8")),
        height=350,
        showlegend=False,
    )
    return fig

def chart_exit_breakdown(patients: list) -> go.Figure:
    """Stacked bar: discharged vs admitted per priority."""
    data = {pri: {"discharged": 0, "admitted": 0}
            for pri in [1, 2, 3, 4]}
    for p in patients:
        pri = _get_priority(p)
        ext = _get_exit(p)
        if pri in data and ext in data[pri]:
            data[pri][ext] += 1
    fig = go.Figure()
    for outcome, color in [
        ("discharged", "#4ade80"),
        ("admitted",   "#f87171")
    ]:
        fig.add_trace(go.Bar(
            x=[PRIORITY_NAMES[p] for p in [1,2,3,4]],
            y=[data[p][outcome] for p in [1,2,3,4]],
            name=outcome.capitalize(),
            marker_color=color,
            marker_line_width=0,
            marker_line_color="#0f1418",
        ))
    fig.update_layout(
        **_DARK_LAYOUT,
        title=dict(text="Discharge vs Admission by Priority", font=dict(size=14, color="#dee3e8")),
        barmode="stack",
        height=350,
        bargap=0.3,
    )
    return fig

def chart_scenario_comparison(
        results: list, param_name: str,
        param_values: list) -> go.Figure:
    """Bar chart for sensitivity analysis comparison."""
    avg_waits = [r.get("avg_wait", 0) for r in results]
    utils     = [r.get("utilization", 0) for r in results]
    labels    = [f"{param_name}={v}" for v in param_values]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels, y=avg_waits,
        name="Avg Wait (min)",
        marker_color="#8ed5ff",
        marker_line_width=0,
    ))
    fig.add_trace(go.Bar(
        x=labels, y=utils,
        name="Utilization (%)",
        marker_color="#ffc176",
        marker_line_width=0,
    ))
    fig.update_layout(
        **_DARK_LAYOUT,
        title=dict(text=f"Sensitivity Analysis — varying {param_name}", font=dict(size=14, color="#dee3e8")),
        barmode="group",
        height=380,
        bargap=0.2,
    )
    return fig

def chart_monte_carlo_risk(
        mc_results: list,
        param_label: str) -> go.Figure:
    """
    Risk probability chart from Monte Carlo results.
    Shows P(Red breach) and P(Green breach) per scenario.
    """
    scenarios  = [r["scenario"] for r in mc_results]
    p_red      = [r["p_red_breach"] for r in mc_results]
    p_green    = [r.get("p_green_breach", 0)
                  for r in mc_results]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=scenarios, y=p_red,
        name="P(Red wait > 5 min) %",
        marker_color="#f87171",
        marker_line_width=0,
    ))
    fig.add_trace(go.Bar(
        x=scenarios, y=p_green,
        name="P(Green wait > 60 min) %",
        marker_color="#ffc176",
        marker_line_width=0,
    ))
    # 5% threshold line
    fig.add_hline(
        y=5,
        line_dash="dash",
        line_color="#f87171",
        annotation_text="5% Red threshold",
        annotation_font_color="#bdc8d1",
    )
    fig.update_layout(
        **_DARK_LAYOUT,
        title=dict(
            text=f"Monte Carlo Risk Analysis — varying {param_label} (N=100 replications)",
            font=dict(size=14, color="#dee3e8")),
        yaxis_title="Probability (%)",
        barmode="group",
        height=400,
        bargap=0.2,
    )
    return fig

def chart_confidence_interval(
        mc_results: list,
        param_label: str) -> go.Figure:
    """
    95% CI chart for Red patient wait time
    across Monte Carlo scenarios.
    """
    scenarios = [r["scenario"] for r in mc_results]
    means     = [r["red_wait_mean"] for r in mc_results]
    ci_lo     = [r["red_wait_ci_lo"] for r in mc_results]
    ci_hi     = [r["red_wait_ci_hi"] for r in mc_results]

    fig = go.Figure()
    # CI band
    fig.add_trace(go.Scatter(
        x=scenarios + scenarios[::-1],
        y=ci_hi + ci_lo[::-1],
        fill="toself",
        fillcolor="rgba(248,113,113,0.12)",
        line=dict(color="rgba(255,255,255,0)"),
        name="95% CI"
    ))
    # Mean line
    fig.add_trace(go.Scatter(
        x=scenarios, y=means,
        mode="lines+markers",
        line=dict(color="#f87171", width=2),
        marker=dict(size=8, color="#f87171", line=dict(color="#0f1418", width=1)),
        name="Mean Red Wait"
    ))
    # 5-minute threshold
    fig.add_hline(
        y=5,
        line_dash="dash",
        line_color="rgba(248,113,113,0.5)",
        annotation_text="5 min threshold",
        annotation_font_color="#bdc8d1",
    )
    fig.update_layout(
        **_DARK_LAYOUT,
        title=dict(
            text=f"Red Patient Wait Time — 95% CI (Monte Carlo, N=100) varying {param_label}",
            font=dict(size=14, color="#dee3e8")),
        yaxis_title="Wait Time (minutes)",
        height=400,
    )
    return fig
