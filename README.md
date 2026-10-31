# Сервіс керування висотою БПА (Docker + GitHub Actions)

Навчальний сервіс автономної системи: PID-регулятор висоти БПА, модель об'єкта та симуляційний сценарій.
Для кожного Pull Request у `main` GitHub Actions виконує: юніт-тести → симуляційний сценарій → збірку Docker-образу → запуск контейнера.

## Структура
| Файл | Призначення |
|---|---|
| `pid_service/` | PID-регулятор, модель висоти, симуляція та оцінка показників |
| `run_simulation.py` | запуск сценарію (код виходу 1, якщо критерії не виконано) |
| `test_scenario_01.json` | сценарій: крок 0→3 м, порив вітру, критерії якості |
| `tests/` | юніт-тести (pytest) |
| `Dockerfile` | збірка образу сервісу |
| `.github/workflows/ci.yml` | конвеєр CI |

## Локальний запуск
```bash
pip install -r requirements.txt
pytest tests/ -v
python run_simulation.py --scenario test_scenario_01.json
```

## Docker
```bash
docker build -t my-autonomous-service:local .
docker run --rm my-autonomous-service:local
```

Lab 9 - author: I. Holovach
