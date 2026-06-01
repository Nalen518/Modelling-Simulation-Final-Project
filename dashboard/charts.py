import plotly.graph_objects as go
import plotly.express as px

PRIORITY_COLORS = {
    1: "#E74C3C",  # Red
    2: "#F39C12",  # Yellow
    3: "#27AE60",  # Green
    4: "#95A5A6",  # White/Gray
    5: "#1C2833",  # Black
}
PRIORITY_NAMES = {
    1: "Red", 2: "Yellow",
    3: "Green", 4: "White", 5: "Black"
}

def chart_wait_distribution(patients: list) -> go.Figure:
    """Histogram of wait times per priority."""
    fig = go.Figure()
    for pri in [1, 2, 3, 4]:
        pts = [p["wait_time"] if isinstance(p, dict)
               else p.wait_time
               for p in patients
               if (p["priority"] if isinstance(p, dict)
               else p.priority) == pri]
        if pts:
            fig.add_trace(go.Histogram(
                x=pts,
                name=PRIORITY_NAMES[pri],
                marker_color=PRIORITY_COLORS[pri],
                opacity=0.7,
                nbinsx=20
            ))
    fig.update_layout(
        title="Waiting Time Distribution by Priority",
        xaxis_title="Wait Time (minutes)",
        yaxis_title="Patient Count",
        barmode="overlay",
        height=350,
        legend_title="Priority"
    )
    return fig

def chart_priority_breakdown(patients: list) -> go.Figure:
    """Donut chart of priority distribution."""
    counts = {k: 0 for k in PRIORITY_NAMES}
    for p in patients:
        pri = p["priority"] if isinstance(p, dict) \
              else p.priority
        counts[pri] = counts.get(pri, 0) + 1
    fig = go.Figure(go.Pie(
        labels=[PRIORITY_NAMES[k] for k in counts],
        values=list(counts.values()),
        hole=0.4,
        marker_colors=[PRIORITY_COLORS[k] for k in counts]
    ))
    fig.update_layout(
        title="Patient Priority Breakdown",
        height=350
    )
    return fig

def chart_exit_breakdown(patients: list) -> go.Figure:
    """Stacked bar: discharged vs admitted per priority."""
    data = {pri: {"discharged": 0, "admitted": 0}
            for pri in [1, 2, 3, 4]}
    for p in patients:
        pri = p["priority"] if isinstance(p, dict) \
              else p.priority
        ext = p["exit_type"] if isinstance(p, dict) \
              else p.exit_type
        if pri in data and ext in data[pri]:
            data[pri][ext] += 1
    fig = go.Figure()
    for outcome, color in [
        ("discharged", "#27AE60"),
        ("admitted",   "#E74C3C")
    ]:
        fig.add_trace(go.Bar(
            x=[PRIORITY_NAMES[p] for p in [1,2,3,4]],
            y=[data[p][outcome] for p in [1,2,3,4]],
            name=outcome.capitalize(),
            marker_color=color
        ))
    fig.update_layout(
        title="Discharge vs Admission by Priority",
        barmode="stack",
        height=350
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
        marker_color="#2E86C1"
    ))
    fig.add_trace(go.Bar(
        x=labels, y=utils,
        name="Utilization (%)",
        marker_color="#E67E22"
    ))
    fig.update_layout(
        title=f"Sensitivity Analysis — varying {param_name}",
        barmode="group",
        height=380
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
        marker_color="#E74C3C"
    ))
    fig.add_trace(go.Bar(
        x=scenarios, y=p_green,
        name="P(Green wait > 60 min) %",
        marker_color="#F39C12"
    ))
    # 5% threshold line
    fig.add_hline(
        y=5,
        line_dash="dash",
        line_color="#922B21",
        annotation_text="5% Red threshold"
    )
    fig.update_layout(
        title=f"Monte Carlo Risk Analysis "
              f"— varying {param_label} "
              f"(N=100 replications)",
        yaxis_title="Probability (%)",
        barmode="group",
        height=400,
        legend_title="Risk Metric"
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
        fillcolor="rgba(231,76,60,0.15)",
        line=dict(color="rgba(255,255,255,0)"),
        name="95% CI"
    ))
    # Mean line
    fig.add_trace(go.Scatter(
        x=scenarios, y=means,
        mode="lines+markers",
        line=dict(color="#E74C3C", width=2),
        marker=dict(size=8),
        name="Mean Red Wait"
    ))
    # 5-minute threshold
    fig.add_hline(
        y=5,
        line_dash="dash",
        line_color="#922B21",
        annotation_text="5 min threshold"
    )
    fig.update_layout(
        title=f"Red Patient Wait Time — 95% CI "
              f"(Monte Carlo, N=100) "
              f"varying {param_label}",
        yaxis_title="Wait Time (minutes)",
        height=400
    )
    return fig
