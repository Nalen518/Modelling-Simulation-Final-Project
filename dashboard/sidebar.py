import streamlit as st

def get_params() -> dict:
    st.sidebar.title("⚙️ Simulation Params")
    st.sidebar.markdown("---")

    st.sidebar.subheader("Patient Arrivals")
    lam = st.sidebar.slider(
        "Arrival Rate (patients/hr)", 1, 50, 10, help="Poisson arrival rate λ")

    with st.sidebar.expander("👨‍⚕️ Staff Configuration", expanded=True):
        n_doctors = st.slider("Doctors (c)", 1, 10, 3)
        n_nurses = st.slider("Triage Nurses (s)", 1, 5, 1)
        n_reg = st.slider("Registration Officers", 1, 3, 1)

    with st.sidebar.expander("⏱️ Simulation Settings"):
        duration = st.slider("Duration (minutes)", 60, 1440, 480)

    with st.sidebar.expander("🚦 Triage Probabilities (%)"):
        red   = st.slider("🔴 Red (Critical)",  1, 20, 5)
        yellow= st.slider("🟡 Yellow (Emergency)", 5, 40, 20)
        green = st.slider("🟢 Green (Urgent)", 20, 70, 55)
        white = st.slider("⚪ White (Non-urgent)", 5, 40, 19)
        black = st.slider("⬛ Black (DOA)", 0, 5, 1)

        total = red + yellow + green + white + black
        if total != 100:
            st.error(f"Sums to {total}% (must be 100%)")

    probs = [red/100, yellow/100, green/100, white/100, black/100]

    return {
        "lambda":         lam,
        "n_doctors":      n_doctors,
        "n_nurses":       n_nurses,
        "n_registration": n_reg,
        "duration":       duration,
        "triage_probs":   probs
    }
