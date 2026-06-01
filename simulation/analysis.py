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
                if p.exit_type != "DOA"]
    doa      = [p for p in patients
                if p.exit_type == "DOA"]

    # Overall metrics
    avg_wait   = (sum(p.wait_time for p in treated) /
                  max(len(treated), 1))
    max_wait   = max(
        (p.wait_time for p in treated), default=0)
    throughput = len(treated) / (result["time"] / 60)
    total_treatment_time = sum(
        p.treatment_duration
        for p in treated)
    utilization = (total_treatment_time /
                   max(result["time"] * n_doctors, 1)
                   ) * 100

    # Per-priority metrics
    per_priority = {}
    for pri in [1, 2, 3, 4]:
        pts = [p for p in treated
               if p.priority == pri]
        per_priority[pri] = {
            "count":     len(pts),
            "avg_wait":  (sum(p.wait_time for p in pts) /
                          max(len(pts), 1)),
            "max_wait":  max(
                (p.wait_time for p in pts), default=0),
            "avg_treat": (sum(
                p.treatment_duration
                for p in pts) / max(sum(1 for p in pts if p.treatment_end > 0), 1))
        }

    # Queue metrics from stage_counts log
    max_queue = result["stage_counts"].get("queue", 0)

    return {
        "total":        len(patients),
        "treated":      len(treated),
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
        print(f"[A] c={c} → "
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
        print(f"[B] λ={lam} → "
              f"avg_wait={m['avg_wait']} min | "
              f"Red_wait="
              f"{m['per_priority'][1]['avg_wait']:.1f} | "
              f"max_queue={m['max_queue']}")
    return results

# ─── EXPERIMENT C: MONTE CARLO ───────────────────────────
def run_single_replication(params: dict,
                           n_doctors: int,
                           seed: int = None) -> dict:
    """
    One Monte Carlo replication.
    Sets random seed for reproducibility.
    Returns flat metrics dict for aggregation.
    """
    if seed is not None:
        random.seed(seed)
    p = {**params, "n_doctors": n_doctors}
    sim = IGDSimulation(p)
    raw = sim.run()
    m = compute_metrics(raw, n_doctors=n_doctors)

    # Extract specific risk indicators
    patients = raw["patients"]
    treated  = [p for p in patients
                if p.exit_type != "DOA"]

    red_patients = [p for p in treated
                    if p.priority == 1]
    green_patients = [p for p in treated
                      if p.priority == 3]

    # Risk flags for this replication
    red_breach   = any(p.wait_time > 5
                       for p in red_patients)
    green_breach = any(p.wait_time > 60
                       for p in green_patients)
    queue_breach = m["max_queue"] > 20

    return {
        **m,
        "red_breach":   red_breach,    # bool
        "green_breach": green_breach,  # bool
        "queue_breach": queue_breach,  # bool
        "red_avg_wait": m["per_priority"][1]["avg_wait"],
        "green_avg_wait": m["per_priority"][3]["avg_wait"],
    }

def run_monte_carlo_c1(
        n_replications: int = 100,
        base_params: dict = None) -> list:
    """
    C1: Vary doctor count c=2,3,4,5 at λ=20.
    N=100 replications per scenario.
    Returns list of scenario summary dicts.
    """
    params = {**(base_params or BASE_PARAMS),
              "lambda": 20}
    results = []

    for c in [2, 3, 4, 5]:
        print(f"[MC-C1] Running {n_replications} "
              f"replications at c={c}...")
        replications = []
        for i in range(n_replications):
            rep = run_single_replication(
                params, n_doctors=c, seed=i)
            replications.append(rep)

        # Aggregate across replications
        avg_waits    = [r["avg_wait"] for r in replications]
        red_waits    = [r["red_avg_wait"]
                        for r in replications]
        utils        = [r["utilization"]
                        for r in replications]
        red_breaches = [r["red_breach"]
                        for r in replications]
        grn_breaches = [r["green_breach"]
                        for r in replications]

        summary = {
            "scenario":       f"c={c}",
            "param_value":    c,
            "n_replications": n_replications,

            # Avg wait — mean + 95% CI
            "avg_wait_mean":  round(np.mean(avg_waits), 2),
            "avg_wait_ci_lo": round(
                np.percentile(avg_waits, 2.5), 2),
            "avg_wait_ci_hi": round(
                np.percentile(avg_waits, 97.5), 2),

            # Red patient wait — mean + 95% CI
            "red_wait_mean":  round(np.mean(red_waits), 2),
            "red_wait_ci_lo": round(
                np.percentile(red_waits, 2.5), 2),
            "red_wait_ci_hi": round(
                np.percentile(red_waits, 97.5), 2),

            # Utilization — mean
            "utilization_mean": round(np.mean(utils), 1),

            # Risk probabilities
            "p_red_breach": round(
                sum(red_breaches) /
                n_replications * 100, 1),
            "p_green_breach": round(
                sum(grn_breaches) /
                n_replications * 100, 1),
        }
        results.append(summary)
        print(f"  → P(Red wait>5min)="
              f"{summary['p_red_breach']}% | "
              f"Red wait 95CI=["
              f"{summary['red_wait_ci_lo']}, "
              f"{summary['red_wait_ci_hi']}] min")

    return results

def run_monte_carlo_c2(
        n_replications: int = 100,
        base_params: dict = None) -> list:
    """
    C2: Vary arrival rate λ=10,20,30,40 at c=3.
    N=100 replications per scenario.
    """
    params = {**(base_params or BASE_PARAMS),
              "n_doctors": 3}
    results = []

    for lam in [10, 20, 30, 40]:
        print(f"[MC-C2] Running {n_replications} "
              f"replications at λ={lam}...")
        p = {**params, "lambda": lam}
        replications = []
        for i in range(n_replications):
            rep = run_single_replication(
                p, n_doctors=3, seed=i*100)
            replications.append(rep)

        red_waits     = [r["red_avg_wait"]
                         for r in replications]
        queue_breaches= [r["queue_breach"]
                         for r in replications]
        red_breaches  = [r["red_breach"]
                         for r in replications]

        summary = {
            "scenario":       f"λ={lam}",
            "param_value":    lam,
            "n_replications": n_replications,

            "red_wait_mean":  round(np.mean(red_waits), 2),
            "red_wait_ci_lo": round(
                np.percentile(red_waits, 2.5), 2),
            "red_wait_ci_hi": round(
                np.percentile(red_waits, 97.5), 2),

            "p_red_breach":   round(
                sum(red_breaches) /
                n_replications * 100, 1),
            "p_queue_breach": round(
                sum(queue_breaches) /
                n_replications * 100, 1),
        }
        results.append(summary)
        print(f"  → P(Red>5min)="
              f"{summary['p_red_breach']}% | "
              f"P(Queue>20)="
              f"{summary['p_queue_breach']}%")

    return results

def find_optimal_staffing(
        base_params: dict = None,
        n_replications: int = 100) -> dict:
    """
    C3: Find minimum c where ALL conditions met:
    - P(Red wait > 5 min) < 5%
    - P(Green wait > 60 min) < 10%
    - 60% < Utilization < 90%
    """
    params = {**(base_params or BASE_PARAMS),
              "lambda": 20}
    print("[MC-C3] Finding optimal staffing...")

    for c in range(1, 11):
        replications = []
        for i in range(n_replications):
            rep = run_single_replication(
                params, n_doctors=c, seed=i*7)
            replications.append(rep)

        p_red   = sum(r["red_breach"]
                      for r in replications
                      ) / n_replications * 100
        p_green = sum(r["green_breach"]
                      for r in replications
                      ) / n_replications * 100
        util    = np.mean([r["utilization"]
                           for r in replications])

        print(f"  c={c}: P(Red)={p_red:.1f}% | "
              f"P(Green)={p_green:.1f}% | "
              f"Util={util:.1f}%")

        cond_red   = p_red   < 5.0
        cond_green = p_green < 10.0
        cond_util  = 60.0 < util < 90.0

        if cond_red and cond_green and cond_util:
            print(f"\n✅ OPTIMAL: c={c} doctors")
            print(f"   P(Red wait>5min)  = {p_red:.1f}%  < 5%")
            print(f"   P(Green wait>60m) = {p_green:.1f}% < 10%")
            print(f"   Utilization       = {util:.1f}%  in 60-90%")
            return {
                "optimal_doctors": c,
                "p_red_breach":    round(p_red, 1),
                "p_green_breach":  round(p_green, 1),
                "utilization":     round(util, 1),
                "conditions_met":  True
            }

    return {
        "optimal_doctors": None,
        "conditions_met":  False,
        "message": "No c in range 1-10 satisfies all conditions at λ=20"
    }
