import copy
from pathlib import Path

from pid_service.simulation import compute_metrics, evaluate, load_scenario, run_scenario

SCENARIO = Path(__file__).resolve().parent.parent / "test_scenario_01.json"


def _run(sc):
    T, Z, U, S = run_scenario(sc)
    return compute_metrics(sc, T, Z)


def test_reference_scenario_passes():
    sc = load_scenario(SCENARIO)
    passed, fails = evaluate(sc, _run(sc))
    assert passed, fails


def test_simulation_is_deterministic():
    sc = load_scenario(SCENARIO)
    assert _run(sc) == _run(sc)


def test_poorly_tuned_pid_fails_criteria():
    sc = load_scenario(SCENARIO)
    bad = copy.deepcopy(sc)
    bad["controller"] = {"kp": 1.0, "ki": 0.5, "kd": 0.1}
    passed, _ = evaluate(bad, _run(bad))
    assert not passed


def test_final_altitude_reaches_setpoint():
    sc = load_scenario(SCENARIO)
    assert _run(sc)["steady_state_error_m"] < 0.05
