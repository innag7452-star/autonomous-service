"""Запуск симуляційного сценарію: python run_simulation.py --scenario test_scenario_01.json
Код завершення 0 - сценарій пройдено, 1 - критерії не виконано (CI позначає крок як невдалий)."""
import argparse
import json
import sys

from pid_service.simulation import compute_metrics, evaluate, load_scenario, run_scenario


def main(argv=None):
    ap = argparse.ArgumentParser(description="Симуляція висоти БПА з PID-регулятором")
    ap.add_argument("--scenario", required=True, help="шлях до JSON-сценарію")
    ap.add_argument("--output", help="куди зберегти результат у JSON")
    args = ap.parse_args(argv)

    sc = load_scenario(args.scenario)
    T, Z, U, S = run_scenario(sc)
    metrics = compute_metrics(sc, T, Z)
    passed, fails = evaluate(sc, metrics)

    c = sc["controller"]
    print(f"Сценарій: {sc['name']}")
    print(f"PID: Kp={c['kp']}, Ki={c['ki']}, Kd={c['kd']}")
    for k, v in metrics.items():
        print(f"  {k}: {v}")
    print("РЕЗУЛЬТАТ:", "PASS" if passed else "FAIL")
    for f in fails:
        print("  порушено критерій ->", f)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            json.dump({"scenario": sc["name"], "metrics": metrics, "passed": passed},
                      fh, ensure_ascii=False, indent=2)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
