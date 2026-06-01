import streamlit as st

def get_params() -> dict:
    st.sidebar.title("⚙️ Simulation Parameter")
    st.sidebar.caption("Adjust the variables below to test different hospital scenarios.")
    st.sidebar.divider()

    with st.sidebar.expander("📈 Demand Profile", expanded=True):
        lam = st.slider(
            "Arrival Rate (pts/hr)", 1, 50, 20, 
            help="Average Poisson arrival rate λ")

    with st.sidebar.expander("👨‍⚕️ Staff Configuration", expanded=True):
        n_doctors = st.slider("Doctors (c)", 1, 10, 3, help="Number of doctors treating patients")
        n_nurses  = st.slider("Triage Nurses (s)", 1, 5, 1, help="Nurses performing initial assessment")
        n_reg     = st.slider("Registration Staff", 1, 3, 1)

    with st.sidebar.expander("⏱️ Simulation Settings", expanded=False):
        duration = st.slider(
            "Duration (minutes)", 60, 1440, 480, step=60,
            help="480 mins = 1 typical 8-hour shift"
        )

    with st.sidebar.expander("🏥 Triage Probabilities (%)", expanded=False):
        red   = st.slider("🔴 Red (Critical)",  0, 100, 5)
        yellow= st.slider("🟡 Yellow (Emergency)", 0, 100, 20)
        green = st.slider("🟢 Green (Urgent)", 0, 100, 55)
        white = st.slider("⚪ White (Non-urgent)", 0, 100, 19)
        black = st.slider("⬛ Black (DOA)", 0, 100, 1)

        total = red + yellow + green + white + black
        if total != 100:
            st.warning(f"⚠️ Current sum: {total}%. The simulation will auto-normalize these to 100%.")

    # Auto-normalize probabilities so the math is always perfect (sums to 1.0)
    # even if the user slides them to total > 100 or < 100.
    total_f = float(total) if total > 0 else 1.0
    probs = [red/total_f, yellow/total_f, green/total_f, white/total_f, black/total_f]

    return {
        "lambda":         lam,
        "n_doctors":      n_doctors,
        "n_nurses":       n_nurses,
        "n_registration": n_reg,
        "duration":       duration,
        "triage_probs":   probs
    }
