import json
import random

from .controller import PID
from .plant import AltitudePlant

DT = 0.005


def load_scenario(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def run_scenario(sc):
    """Запускає сценарій і повертає (time, z, u, setpoint)."""
    rng = random.Random(sc.get("seed", 0))
    p, c = sc["plant"], sc["controller"]
    plant = AltitudePlant(p["mass"], p["drag"], p["motor_tau"])
    pid = PID(c["kp"], c["ki"], c["kd"], -p["max_thrust"], p["max_thrust"])
    t_step, r = sc["setpoint"]["step_time"], sc["setpoint"]["value"]
    t_gust, f_gust = sc["disturbance"]["time"], sc["disturbance"]["force"]
    noise = sc.get("noise_std", 0.0)
    n = int(sc["duration"] / DT)
    T, Z, U, S = [], [], [], []
    for k in range(n):
        t = k * DT
        sp = r if t >= t_step else 0.0
        meas = plant.z + rng.gauss(0.0, noise)
        u = pid.update(sp, meas, DT)
        T.append(t); Z.append(plant.z); U.append(u); S.append(sp)
        plant.step(u, f_gust if t >= t_gust else 0.0, DT)
    return T, Z, U, S


def compute_metrics(sc, T, Z):
    """Перерегулювання, час встановлення (±2 %), стала похибка та просідання від пориву."""
    t0, r = sc["setpoint"]["step_time"], sc["setpoint"]["value"]
    tg = sc["disturbance"]["time"]
    seg = [(t, z) for t, z in zip(T, Z) if t0 <= t < tg]
    overshoot = max(0.0, (max(z for _, z in seg) - r) / r * 100.0)
    out = [t for t, z in seg if abs(z - r) > 0.02 * abs(r)]
    settling = (out[-1] - t0) if out else 0.0
    if out and out[-1] >= seg[-1][0] - 1e-9:
        settling = float("inf")                                  # не встановився до пориву
    tail = [z for t, z in seg if t >= tg - 2.0]
    steady_error = abs(r - sum(tail) / len(tail))
    after = [z for t, z in zip(T, Z) if t >= tg]
    dip = r - min(after)
    return {"overshoot_pct": round(overshoot, 2), "settling_time_s": round(settling, 2),
            "steady_state_error_m": round(steady_error, 4), "gust_dip_m": round(dip, 3)}


def evaluate(sc, metrics):
    """Порівнює показники з критеріями сценарію; повертає (passed, [повідомлення про порушення])."""
    crit = sc["pass_criteria"]
    checks = [
        ("overshoot_pct", "max_overshoot_pct", "перерегулювання, %"),
        ("settling_time_s", "max_settling_time_s", "час встановлення, с"),
        ("steady_state_error_m", "max_steady_state_error_m", "стала похибка, м"),
        ("gust_dip_m", "max_gust_dip_m", "просідання від пориву, м"),
    ]
    fails = []
    for key, limit_key, label in checks:
        if metrics[key] > crit[limit_key]:
            fails.append(f"{label}: {metrics[key]} > {crit[limit_key]}")
    return (not fails), fails
