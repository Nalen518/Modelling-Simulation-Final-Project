import streamlit as st
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dashboard.sidebar import get_params
from dashboard.animation import render_animation
from dashboard.charts import (
    chart_wait_distribution,
    chart_priority_breakdown,
    chart_exit_breakdown,
    chart_scenario_comparison,
    chart_monte_carlo_risk,
    chart_confidence_interval
)

def format_results(results):
    import pandas as pd
    df = pd.DataFrame(results)
    if "per_priority" in df.columns:
        # Flatten the Red (priority 1) data into readable columns
        df["Red Count"] = df["per_priority"].apply(lambda p: p.get(1, {}).get("count", 0))
        df["Red Avg Wait (min)"] = df["per_priority"].apply(lambda p: round(p.get(1, {}).get("avg_wait", 0), 1))
        df["Red Max Wait (min)"] = df["per_priority"].apply(lambda p: round(p.get(1, {}).get("max_wait", 0), 1))
        df = df.drop(columns=["per_priority"])
    return df

st.set_page_config(
    page_title="IGD Queue Simulation",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Emergency Room Queue Optimization")
st.caption(
    "Discrete Event Simulation | "
    "M/M/1 → M/M/s → M/M/c | "
    "Stochastic Priority Queue"
)

params = get_params()

col_run, col_info = st.columns([1, 3])
with col_run:
    run_btn = st.button(
        "▶️ Run Simulation", type="primary",
        use_container_width=True)
with col_info:
    st.info(
        f"λ={params['lambda']} pts/hr | "
        f"Doctors={params['n_doctors']} | "
        f"Nurses={params['n_nurses']} | "
        f"Duration={params['duration']} min"
    )

if run_btn:
    # Import here so dashboard works standalone with mock data
    try:
        from simulation.model import IGDSimulation
        SIMULATION_AVAILABLE = True
    except ImportError:
        SIMULATION_AVAILABLE = False

    anim_placeholder = st.empty()
    state_log = []

    def on_state(state):
        state_log.append(state)
        render_animation(anim_placeholder, state)
        time.sleep(0.005)

    with st.spinner("Running simulation..."):
        if SIMULATION_AVAILABLE:
            sim = IGDSimulation(params,
                                state_callback=on_state)
            result = sim.run()
            patients = result["patients"]
            st.toast("Simulation Complete! 🎉", icon="✅")
        else:
            st.warning(
                "SimPy engine not ready. "
                "Showing mock data.")
            patients = []

    # KPI Cards
    st.divider()
    st.subheader("📊 Key Performance Indicators")
    treated = [p for p in patients
               if (p.exit_type
                   if hasattr(p, 'exit_type')
                   else p["exit_type"]) != "DOA"]
    doa = [p for p in patients
           if (p.exit_type
               if hasattr(p, 'exit_type')
               else p["exit_type"]) == "DOA"]

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Patients", len(patients))
    c2.metric("Treated", len(treated))
    c3.metric("DOA", len(doa))
    c4.metric("Avg Wait (min)",
        f"{sum(p.wait_time if hasattr(p,'wait_time') else p['wait_time'] for p in treated) / max(len(treated),1):.1f}"
        if treated else "N/A")
    c5.metric("Simulation Time",
        f"{result['time']:.0f} min"
        if SIMULATION_AVAILABLE else "—")

    # Charts
    st.divider()
    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(
            chart_wait_distribution(patients),
            use_container_width=True)
    with col_right:
        st.plotly_chart(
            chart_priority_breakdown(patients),
            use_container_width=True)

    st.plotly_chart(
        chart_exit_breakdown(patients),
        use_container_width=True)

st.divider()
st.subheader("🔬 Sensitivity Analysis")

tab_a, tab_b, tab_c = st.tabs([
    "Experiment A — Doctor Count",
    "Experiment B — Arrival Rate",
    "Experiment C — Monte Carlo"
])

with tab_a:
    st.write("Varying doctor count (c=2,3,4,5) "
             "at fixed λ=20 patients/hr")
    if st.button("Run Experiment A"):
        from simulation.analysis import run_experiment_a
        with st.spinner("Running 4 scenarios..."):
            res_a = run_experiment_a({
                **params,
                "duration": 480
            })
        st.plotly_chart(
            chart_scenario_comparison(
                res_a, "Doctors",
                [2, 3, 4, 5]),
            use_container_width=True)
        st.dataframe(format_results(res_a))

with tab_b:
    st.write("Varying arrival rate at fixed c=3 doctors")
    if st.button("Run Experiment B"):
        from simulation.analysis import run_experiment_b
        with st.spinner("Running 4 scenarios..."):
            res_b = run_experiment_b({
                **params,
                "duration": 480
            })
        st.plotly_chart(
            chart_scenario_comparison(
                res_b, "λ",
                [10, 20, 30, 40]),
            use_container_width=True)
        st.dataframe(format_results(res_b))

with tab_c:
    st.markdown("""
    **Monte Carlo Simulation** runs the DES engine 
    N=100 times per scenario to produce probability 
    distributions rather than single-point estimates.

    This answers:
    - *What is the probability a Red patient waits 
      more than 5 minutes?*
    - *What is the 95% confidence interval for 
      average wait time?*
    - *What is the minimum doctor count that keeps 
      risk below acceptable thresholds?*
    """)

    col_mc1, col_mc2 = st.columns(2)

    with col_mc1:
        if st.button("Run MC — Vary Doctors"):
            from simulation.analysis import \
                run_monte_carlo_c1
            with st.spinner(
                "Running 400 simulations "
                "(4 scenarios × 100 runs)..."
            ):
                mc1 = run_monte_carlo_c1(
                    n_replications=100,
                    base_params={**params,
                                 "duration": 480}
                )
            st.plotly_chart(
                chart_monte_carlo_risk(mc1, "Doctors"),
                use_container_width=True)
            st.plotly_chart(
                chart_confidence_interval(
                    mc1, "Doctors"),
                use_container_width=True)
            st.dataframe(mc1)

    with col_mc2:
        if st.button("Run MC — Vary Arrival Rate"):
            from simulation.analysis import \
                run_monte_carlo_c2
            with st.spinner(
                "Running 400 simulations "
                "(4 scenarios × 100 runs)..."
            ):
                mc2 = run_monte_carlo_c2(
                    n_replications=100,
                    base_params={**params,
                                 "duration": 480}
                )
            st.plotly_chart(
                chart_monte_carlo_risk(
                    mc2, "Arrival Rate"),
                use_container_width=True)
            st.plotly_chart(
                chart_confidence_interval(
                    mc2, "Arrival Rate"),
                use_container_width=True)
            st.dataframe(mc2)

    st.markdown("---")
    st.subheader("🎯 Optimal Staffing Finder")
    st.caption(
        "Finds minimum doctors where: "
        "P(Red>5min)<5% AND P(Green>60min)<10% "
        "AND 60%<Utilization<90%"
    )
    if st.button("Find Optimal Doctor Count",
                 type="primary"):
        from simulation.analysis import \
            find_optimal_staffing
        with st.spinner(
            "Running up to 1000 simulations..."
        ):
            optimal = find_optimal_staffing(
                base_params={**params,
                             "duration": 480},
                n_replications=100
            )
        if optimal["conditions_met"]:
            st.success(
                f"✅ Optimal: **"
                f"{optimal['optimal_doctors']} doctors**\n\n"
                f"- P(Red wait > 5 min) = "
                f"{optimal['p_red_breach']}%\n"
                f"- P(Green wait > 60 min) = "
                f"{optimal['p_green_breach']}%\n"
                f"- Utilization = "
                f"{optimal['utilization']}%"
            )
        else:
            st.error(
                "No optimal staffing found "
                "in range c=1–10 at current λ. "
                "Try reducing arrival rate."
            )
