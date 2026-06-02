import random
import numpy as np
from simulation.model import IGDSimulation

# ─── BASE PARAMS ─────────────────────────────────────────
BASE_PARAMS = {
    "n_nurses":       1,
    "n_registration": 1,
    "duration":       480,
    "triage_probs":   [0.05, 0.20, 0.55, 0.19, 0.01]
}

# ─── METRICS EXTRACTOR ───────────────────────────────────
def compute_metrics(result: dict,
                    n_doctors: int = 3) -> dict:
    patients = result["patients"]
    treated  = [p for p in patients
                if p.exit_type != "DOA"
                and p.exit_type != ""]
    doa      = [p for p in patients
                if p.exit_type == "DOA"]

    # Overall metrics
    avg_wait   = (sum(p.wait_time for p in treated) /
                  max(len(treated), 1))
    max_wait   = max(
        (p.wait_time for p in treated), default=0)
    throughput = len(treated) / max(result["time"] / 60, 1)
    total_treatment_time = sum(
        p.treatment_duration
        for p in treated)
    utilization = (total_treatment_time /
                   max(result["time"] * n_doctors, 1)
                   ) * 100

    # Completed = treatment_end > 0 (fully done)
    completed = [p for p in treated
                 if p.treatment_end > 0]

    # Per-priority metrics
    per_priority = {}
    for pri in [1, 2, 3, 4]:
        pts = [p for p in patients
               if int(p.priority) == pri
               and p.exit_type != "DOA"]
        done = [p for p in pts if p.treatment_end > 0]
        in_treat = [p for p in pts
                    if p.treatment_start > 0
                    and p.treatment_end == 0]
        in_queue = [p for p in pts
                    if p.triage_end > 0
                    and p.treatment_start == 0]

        per_priority[pri] = {
            "count":        len(pts),
            "completed":    len(done),
            "in_progress":  len(in_treat),
            "still_queuing":len(in_queue),
            "avg_wait":  (sum(p.wait_time for p in done) /
                          max(len(done), 1)),
            "max_wait":  max(
                (p.wait_time for p in done), default=0),
            "avg_treat": (sum(
                p.treatment_duration
                for p in done) /
                max(len(done), 1)),
        }

    # Queue metrics from stage_counts log
    max_queue = result["stage_counts"].get("queue", 0)

    return {
        "total":        len(patients),
        "treated":      len(treated),
        "completed":    len(completed),
        "doa":          len(doa),
        "avg_wait":     round(avg_wait, 2),
        "max_wait":     round(max_wait, 2),
        "throughput":   round(throughput, 2),
        "utilization":  round(utilization, 1),
        "max_queue":    max_queue,
        "per_priority": per_priority
    }

# ─── EXPERIMENT A: DOCTOR COUNT ──────────────────────────
def run_experiment_a(base_params: dict = None) -> list:
    """Single DES run per scenario. Vary c=2,3,4,5."""
    params = base_params or BASE_PARAMS
    results = []
    for c in [2, 3, 4, 5]:
        p = {**params, "lambda": 20, "n_doctors": c}
        sim = IGDSimulation(p)
        raw = sim.run()
        m = compute_metrics(raw, n_doctors=c)
        m["scenario"] = f"c={c}"
        m["param_value"] = c
        results.append(m)
        print(f"[A] c={c} -> "
              f"avg_wait={m['avg_wait']} min | "
              f"util={m['utilization']}% | "
              f"Red_wait="
              f"{m['per_priority'][1]['avg_wait']:.1f}")
    return results

# ─── EXPERIMENT B: ARRIVAL RATE ──────────────────────────
def run_experiment_b(base_params: dict = None) -> list:
    """Single DES run per scenario. Vary λ=10,20,30,40."""
    params = base_params or BASE_PARAMS
    results = []
    for lam in [10, 20, 30, 40]:
        p = {**params, "lambda": lam, "n_doctors": 3}
        sim = IGDSimulation(p)
        raw = sim.run()
        m = compute_metrics(raw, n_doctors=3)
        m["scenario"] = f"λ={lam}"
        m["param_value"] = lam
        results.append(m)
        print(f"[B] lambda={lam} -> "
              f"avg_wait={m['avg_wait']} min | "
              f"Red_wait="
              f"{m['per_priority'][1]['avg_wait']:.1f} | "
              f"max_queue={m['max_queue']}")
    return results

# ─── SINGLE REPLICATION ──────────────────────────────────
def run_single_replication(params: dict,
                           n_doctors: int,
                           seed: int = None) -> dict:
    """One Monte Carlo replication with risk flags."""
    if seed is not None:
        random.seed(seed)
    p = {**params, "n_doctors": n_doctors}
    sim = IGDSimulation(p)
    raw = sim.run()
    m = compute_metrics(raw, n_doctors=n_doctors)

    patients = raw["patients"]
    treated  = [pt for pt in patients
                if pt.exit_type != "DOA"
                and pt.exit_type != ""]

    red_patients   = [pt for pt in treated
                      if int(pt.priority) == 1
                      and pt.treatment_start > 0]
    green_patients = [pt for pt in treated
                      if int(pt.priority) == 3
                      and pt.treatment_start > 0]

    # Risk flags — Kemenkes 10-min threshold for Red
    red_breach_10 = any(pt.wait_time > 10
                        for pt in red_patients)
    red_breach_5  = any(pt.wait_time > 5
                        for pt in red_patients)
    green_breach  = any(pt.wait_time > 60
                        for pt in green_patients)
    queue_breach  = m["max_queue"] > 20
    util_breach   = m["utilization"] > 95

    return {
        **m,
        "red_breach":    red_breach_5,
        "red_breach_10": red_breach_10,
        "green_breach":  green_breach,
        "queue_breach":  queue_breach,
        "util_breach":   util_breach,
        "red_avg_wait":  m["per_priority"][1]["avg_wait"],
        "green_avg_wait":m["per_priority"][3]["avg_wait"],
    }

# ─── MC: OPTIMAL DOCTOR SCAN (Q1) ───────────────────────
def mc_optimal_doctors(
        base_params: dict = None,
        n_replications: int = 100) -> dict:
    """
    Q1: Scan c=1..10 at λ=20. N=100 reps each.
    Find minimum c where:
      P(Red wait > 10 min) < 5%
      P(Green wait > 60 min) < 10%
      60% < Utilization < 90%
    """
    params = {**(base_params or BASE_PARAMS),
              "lambda": 20}
    print("[MC-Q1] Scanning c=1..10...")

    scan_results = []
    optimal = None

    for c in range(1, 11):
        reps = []
        for i in range(n_replications):
            rep = run_single_replication(
                params, n_doctors=c, seed=i*7)
            reps.append(rep)

        p_red   = round(sum(r["red_breach_10"]
                    for r in reps) /
                    n_replications * 100, 1)
        p_green = round(sum(r["green_breach"]
                    for r in reps) /
                    n_replications * 100, 1)
        util_m  = round(np.mean([r["utilization"]
                    for r in reps]), 1)
        red_wait_m = round(np.mean([r["red_avg_wait"]
                    for r in reps]), 2)

        cond_red   = p_red < 5.0
        cond_green = p_green < 10.0
        cond_util  = 60.0 < util_m < 90.0
        all_met    = cond_red and cond_green and cond_util

        entry = {
            "c":                  c,
            "p_red_breach":       p_red,
            "p_green_breach":     p_green,
            "utilization_mean":   util_m,
            "red_wait_mean":      red_wait_m,
            "all_conditions_met": all_met,
        }
        scan_results.append(entry)
        print(f"  c={c}: P(Red>10m)={p_red}% | "
              f"P(Grn>60m)={p_green}% | "
              f"Util={util_m}% | "
              f"{'[OK]' if all_met else '[FAIL]'}")

        if all_met and optimal is None:
            optimal = entry

    if optimal:
        return {
            "conditions_met":  True,
            "optimal_doctors": optimal["c"],
            "p_red_breach":    optimal["p_red_breach"],
            "p_green_breach":  optimal["p_green_breach"],
            "utilization_mean":optimal["utilization_mean"],
            "scan_results":    scan_results,
        }
    return {
        "conditions_met": False,
        "optimal_doctors": None,
        "scan_results":   scan_results,
    }

# ─── MC: OVERLOAD PROBABILITY (Q2) ──────────────────────
def mc_overload_probability(
        base_params: dict = None,
        n_replications: int = 100) -> list:
    """
    Q2: Vary λ=10,20,30,40 at c=3.
    Overload = ANY of: queue>20, util>95%, Red>10min.
    Returns per-scenario overload probabilities.
    """
    params = {**(base_params or BASE_PARAMS),
              "n_doctors": 3}
    results = []

    for lam in [10, 20, 30, 40]:
        print(f"[MC-Q2] lambda={lam}...")
        p = {**params, "lambda": lam}
        reps = []
        for i in range(n_replications):
            rep = run_single_replication(
                p, n_doctors=3, seed=i*13)
            reps.append(rep)

        p_queue = round(sum(r["queue_breach"]
                    for r in reps) /
                    n_replications * 100, 1)
        p_util  = round(sum(r["util_breach"]
                    for r in reps) /
                    n_replications * 100, 1)
        p_red   = round(sum(r["red_breach_10"]
                    for r in reps) /
                    n_replications * 100, 1)
        p_any   = round(sum(
                    1 for r in reps
                    if r["queue_breach"]
                    or r["util_breach"]
                    or r["red_breach_10"]) /
                    n_replications * 100, 1)

        # Identify main driver
        drivers = {"Queue>20": p_queue,
                   "Util>95%": p_util,
                   "Red>10min": p_red}
        main_driver = max(drivers,
                          key=drivers.get)

        results.append({
            "scenario":       f"λ={lam}",
            "p_overload":     p_any,
            "p_queue_breach": p_queue,
            "p_util_breach":  p_util,
            "p_red_breach":   p_red,
            "overload_driver":main_driver,
        })
        print(f"  -> P(overload)={p_any}% | "
              f"Driver: {main_driver}")

    return results

# ─── MC: CRITICAL PATIENT RISK (Q3) ─────────────────────
def mc_critical_patient_risk(
        base_params: dict = None,
        n_replications: int = 100) -> dict:
    """
    Q3: Red patient breach analysis.
    Q3a: Vary c=2,3,4,5 at λ=20 — P(Red>10min) + 95% CI.
    Q3b: Vary λ=10,20,30,40 at c=3 — same metrics.
    """
    params_base = base_params or BASE_PARAMS

    # Q3a: Vary doctors
    print("[MC-Q3a] Varying doctors...")
    q3a = []
    for c in [2, 3, 4, 5]:
        p = {**params_base, "lambda": 20, "n_doctors": c}
        reps = []
        for i in range(n_replications):
            rep = run_single_replication(
                p, n_doctors=c, seed=i*17)
            reps.append(rep)

        red_waits = [r["red_avg_wait"] for r in reps]
        p_breach  = round(sum(r["red_breach_10"]
                    for r in reps) /
                    n_replications * 100, 1)

        entry = {
            "scenario":        f"c={c}",
            "red_wait_mean":   round(np.mean(red_waits), 2),
            "red_wait_ci_lo":  round(
                np.percentile(red_waits, 2.5), 2),
            "red_wait_ci_hi":  round(
                np.percentile(red_waits, 97.5), 2),
            "p_red_breach_10": p_breach,
            "safe":            p_breach < 5.0,
        }
        q3a.append(entry)
        print(f"  c={c}: P(Red>10m)={p_breach}% | "
              f"Mean={entry['red_wait_mean']} min")

    # Q3b: Vary arrival rate
    print("[MC-Q3b] Varying lambda...")
    q3b = []
    for lam in [10, 20, 30, 40]:
        p = {**params_base, "lambda": lam, "n_doctors": 3}
        reps = []
        for i in range(n_replications):
            rep = run_single_replication(
                p, n_doctors=3, seed=i*23)
            reps.append(rep)

        red_waits = [r["red_avg_wait"] for r in reps]
        p_breach  = round(sum(r["red_breach_10"]
                    for r in reps) /
                    n_replications * 100, 1)

        entry = {
            "scenario":        f"λ={lam}",
            "red_wait_mean":   round(np.mean(red_waits), 2),
            "red_wait_ci_lo":  round(
                np.percentile(red_waits, 2.5), 2),
            "red_wait_ci_hi":  round(
                np.percentile(red_waits, 97.5), 2),
            "p_red_breach_10": p_breach,
            "safe":            p_breach < 5.0,
        }
        q3b.append(entry)
        print(f"  lambda={lam}: P(Red>10m)={p_breach}% | "
              f"Mean={entry['red_wait_mean']} min")

    return {
        "q3a_by_doctors": q3a,
        "q3b_by_lambda":  q3b,
    }

# ─── LEGACY FUNCTIONS (backward compat) ─────────────────
def run_monte_carlo_c1(n_replications=100,
                       base_params=None):
    """Legacy wrapper for old app.py."""
    params = {**(base_params or BASE_PARAMS),
              "lambda": 20}
    results = []
    for c in [2, 3, 4, 5]:
        reps = []
        for i in range(n_replications):
            rep = run_single_replication(
                params, n_doctors=c, seed=i)
            reps.append(rep)
        red_waits = [r["red_avg_wait"] for r in reps]
        results.append({
            "scenario":       f"c={c}",
            "p_red_breach":   round(sum(r["red_breach"]
                              for r in reps) /
                              n_replications * 100, 1),
            "p_green_breach": round(sum(r["green_breach"]
                              for r in reps) /
                              n_replications * 100, 1),
            "red_wait_mean":  round(np.mean(red_waits), 2),
            "red_wait_ci_lo": round(
                np.percentile(red_waits, 2.5), 2),
            "red_wait_ci_hi": round(
                np.percentile(red_waits, 97.5), 2),
        })
    return results

def run_monte_carlo_c2(n_replications=100,
                       base_params=None):
    """Legacy wrapper for old app.py."""
    params = {**(base_params or BASE_PARAMS),
              "n_doctors": 3}
    results = []
    for lam in [10, 20, 30, 40]:
        p = {**params, "lambda": lam}
        reps = []
        for i in range(n_replications):
            rep = run_single_replication(
                p, n_doctors=3, seed=i*100)
            reps.append(rep)
        red_waits = [r["red_avg_wait"] for r in reps]
        results.append({
            "scenario":       f"λ={lam}",
            "p_red_breach":   round(sum(r["red_breach"]
                              for r in reps) /
                              n_replications * 100, 1),
            "p_queue_breach": round(sum(r["queue_breach"]
                              for r in reps) /
                              n_replications * 100, 1),
            "red_wait_mean":  round(np.mean(red_waits), 2),
            "red_wait_ci_lo": round(
                np.percentile(red_waits, 2.5), 2),
            "red_wait_ci_hi": round(
                np.percentile(red_waits, 97.5), 2),
        })
    return results

def find_optimal_staffing(base_params=None,
                          n_replications=100):
    """Legacy wrapper."""
    return mc_optimal_doctors(base_params, n_replications)
