import random

TRIAGE_PROBS_DEFAULT = [0.05, 0.20, 0.55, 0.19, 0.01]

TREATMENT_PARAMS = {
    1: (45,  180, 90),
    2: (20,  90,  40),
    3: (10,  45,  20),
    4: (5,   20,  8),
    5: (0,   0,   0),
}

DISCHARGE_PROB = {1: 0.30, 2: 0.50, 3: 0.85, 4: 0.98}

def inter_arrival_time(lam: float) -> float:
    """Poisson process: lam = patients per hour"""
    return random.expovariate(lam / 60.0)

def registration_time() -> float:
    return random.triangular(1, 5, 2)

def triage_time() -> float:
    return random.triangular(1, 8, 3)

def treatment_time(priority: int) -> float:
    lo, hi, mode = TREATMENT_PARAMS[priority]
    if priority == 5:
        return 0.0
    return random.triangular(lo, hi, mode)

def assign_priority(probs: list = None) -> int:
    p = probs or TRIAGE_PROBS_DEFAULT
    return random.choices([1, 2, 3, 4, 5], weights=p, k=1)[0]

def exit_type(priority: int) -> str:
    prob = DISCHARGE_PROB.get(priority, 1.0)
    return "discharged" if random.random() < prob else "admitted"
