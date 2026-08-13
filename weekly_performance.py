import json
from pathlib import Path


WEEKLY_FILE = Path("weekly_history.json")


def load_weekly_history():
    """
    Carga las estadísticas guardadas de la ejecución anterior.
    """

    if not WEEKLY_FILE.exists():
        return {}

    try:
        with WEEKLY_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return {}


def create_current_snapshot(players):
    """
    Guarda misiones y victorias actuales de cada jugador
    para Simulador y Realista.
    """

    snapshot = {}

    for player in players:
        nick = player.get("nick")

        if not nick:
            continue

        snapshot[nick] = {}

        for mode in ("s", "r"):
            stats = player.get(mode) or {}

            snapshot[nick][mode] = {
                "mission": stats.get("mission") or 0,
                "win": stats.get("win") or 0
            }

    return snapshot


def calculate_weekly_performance(
    players,
    previous_history,
    mode,
    limit=5,
    min_battles=20
):
    """
    Calcula el rendimiento entre la captura anterior
    y la captura actual.
    """

    ranking = []

    for player in players:
        nick = player.get("nick")

        if not nick:
            continue

        current_stats = player.get(mode) or {}

        current_missions = current_stats.get("mission") or 0
        current_wins = current_stats.get("win") or 0

        previous_player = previous_history.get(nick)

        if not previous_player:
            continue

        previous_stats = previous_player.get(mode)

        if not previous_stats:
            continue

        previous_missions = previous_stats.get("mission") or 0
        previous_wins = previous_stats.get("win") or 0

        battles_played = current_missions - previous_missions
        wins = current_wins - previous_wins

        # Ignoramos valores negativos o inconsistentes.
        if battles_played <= 0:
            continue

        if wins < 0:
            continue

        # Mínimo de partidas durante el período.
        if battles_played < min_battles:
            continue

        weekly_winrate = (wins / battles_played) * 100

        ranking.append({
            "nick": nick,
            "battles": battles_played,
            "wins": wins,
            "winrate": round(weekly_winrate, 2)
        })

    ranking.sort(
        key=lambda player: (
            player["winrate"],
            player["battles"]
        ),
        reverse=True
    )

    return ranking[:limit]


def save_weekly_history(snapshot):
    """
    Guarda la captura actual para la próxima ejecución.
    """

    with WEEKLY_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            snapshot,
            file,
            indent=4,
            ensure_ascii=False
        )