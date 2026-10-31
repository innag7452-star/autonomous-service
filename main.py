"""Точка входу сервісу (CMD у Dockerfile): запускає типовий сценарій і виводить показники."""
import sys

from run_simulation import main

if __name__ == "__main__":
    sys.exit(main(["--scenario", "test_scenario_01.json"]))
