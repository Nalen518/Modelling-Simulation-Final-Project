from simulation.analysis import (
    run_experiment_a,
    run_experiment_b,
    run_monte_carlo_c1,
    run_monte_carlo_c2,
    find_optimal_staffing
)

print("=" * 50)
print("EXPERIMENT A — Doctor Count (single run)")
print("=" * 50)
exp_a = run_experiment_a()

print("\n" + "=" * 50)
print("EXPERIMENT B — Arrival Rate (single run)")
print("=" * 50)
exp_b = run_experiment_b()

print("\n" + "=" * 50)
print("EXPERIMENT C1 — Monte Carlo: Doctor Count")
print("=" * 50)
mc_c1 = run_monte_carlo_c1(n_replications=100)

print("\n" + "=" * 50)
print("EXPERIMENT C2 — Monte Carlo: Arrival Rate")
print("=" * 50)
mc_c2 = run_monte_carlo_c2(n_replications=100)

print("\n" + "=" * 50)
print("EXPERIMENT C3 — Optimal Staffing")
print("=" * 50)
optimal = find_optimal_staffing(n_replications=100)
print(f"\nFINAL RECOMMENDATION: {optimal}")
