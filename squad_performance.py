import json
from pathlib import Path
from typing import Any

HISTORY_FILE = Path("squad_history.json")


def load_previous_performance() -> dict[str, float] | None:
    """Carga la eficiencia guardada"""
    if not HISTORY_FILE.exists():
        return None

    try:
        with HISTORY_FILE.open("r", encoding="utf-8") as file:
            history = json.load(file)

        return {
            "a": float(history["a"]),
            "r": float(history["r"]),
            "s": float(history["s"]),
        }
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        return None


def get_current_performance(data: dict[str, Any]) -> dict[str, float]:
    """Extrae la eficiencia actual del escuadrón."""
    return {
        "a": float(data.get("kpd_a") or 0),
        "r": float(data.get("kpd_r") or 0),
        "s": float(data.get("kpd_s") or 0),
    }


def save_current_performance(performance: dict[str, float]) -> None:
    """Guarda la eficiencia para compararla en la próxima ejecución."""
    with HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(performance, file, indent=4, ensure_ascii=False)


def format_change(current: float, previous: float | None) -> str:
    """Devuelve la variación con flecha y signo."""
    if previous is None:
        return "➖ Sin comparación anterior"

    difference = current - previous

    if difference > 0.005:
        return f"📈 +{difference:.2f}"

    if difference < -0.005:
        return f"📉 {difference:.2f}"

    return "➖ 0.00"