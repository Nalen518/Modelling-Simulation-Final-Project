import plotly.graph_objects as go

STAGES = [
    "Arrival", "Registration", "Triage",
    "Queue", "Treatment", "Exit"
]
STAGE_KEYS = [
    "arrival", "registration", "triage",
    "queue", "treatment", "exit"
]
COLORS = [
    "#3498DB", "#F39C12", "#9B59B6",
    "#E74C3C", "#27AE60", "#95A5A6"
]

def render_animation(placeholder, state: dict):
    counts = [
        state["stage_counts"].get(k, 0)
        for k in STAGE_KEYS
    ]
    fig = go.Figure(go.Bar(
        x=STAGES,
        y=counts,
        marker_color=COLORS,
        text=counts,
        textposition="outside"
    ))
    fig.update_layout(
        title=f"🏥 Patient Flow — Time: "
              f"{state['time']:.1f} min",
        yaxis_title="Patients in Stage",
        height=350,
        margin=dict(t=60, b=20, l=40, r=40),
        plot_bgcolor="white",
        yaxis=dict(gridcolor="#EEEEEE")
    )
    placeholder.plotly_chart(
        fig, use_container_width=True)
