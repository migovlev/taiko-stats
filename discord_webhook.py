import requests

from config import DISCORD_WEBHOOK_URL


MODE_NAMES = {
    "a": "Arcade",
    "r": "Realistic",
    "s": "Simulator"
}


def send_dashboard(dashboard, mode="s"):
    """
    Envía el dashboard del escuadrón a Discord mediante un webhook.
    """

    if not DISCORD_WEBHOOK_URL:
        raise ValueError(
            "No se encontró la variable de entorno "
            "DISCORD_WEBHOOK_URL."
        )

    mode_name = MODE_NAMES.get(mode, mode.upper())

    best_kd = dashboard.get("best_kd")
    best_winrate = dashboard.get("best_winrate")
    most_active = dashboard.get("most_active")

    fields = [
        {
            "name": "👥 Miembros",
            "value": str(dashboard["members"]),
            "inline": True
        },
        {
            "name": "⚔️ KD promedio",
            "value": str(dashboard["average_kd"]),
            "inline": True
        },
        {
            "name": "🏆 Win Rate promedio",
            "value": f"{dashboard['average_winrate']}%",
            "inline": True
        },
        {
            "name": "🎮 Misiones totales",
            "value": f"{dashboard['total_missions']:,}",
            "inline": True
        }
    ]

    if best_kd:
        fields.append({
            "name": "🥇 Mejor KD",
            "value": (
                f"**{best_kd['nick']}**\n"
                f"KD: `{best_kd[mode]['kd']}`\n"
                f"Misiones: `{best_kd[mode]['mission']}`"
            ),
            "inline": True
        })

    if best_winrate:
        fields.append({
            "name": "📈 Mejor Win Rate",
            "value": (
                f"**{best_winrate['nick']}**\n"
                f"Win Rate: `{best_winrate[mode]['winrate']}%`\n"
                f"Misiones: `{best_winrate[mode]['mission']}`"
            ),
            "inline": True
        })

    if most_active:
        fields.append({
            "name": "🔥 Jugador más activo",
            "value": (
                f"**{most_active['nick']}**\n"
                f"Misiones: `{most_active[mode]['mission']}`\n"
                f"KD: `{most_active[mode]['kd']}`"
            ),
            "inline": True
        })

    embed = {
        "title": "TAIKO — Estadísticas del escuadrón",
        "description": (
            f"Resumen de estadísticas en modo **{mode_name}**."
        ),
        "color": 15548997,
        "fields": fields,
        "footer": {
            "text": "Datos obtenidos desde ThunderSkill"
        }
    }

    payload = {
        "username": "TAIKO Stats",
        "embeds": [embed]
    }

    response = requests.post(
        DISCORD_WEBHOOK_URL,
        json=payload,
        timeout=15
    )

    if response.status_code not in (200, 204):
        raise RuntimeError(
            f"Discord respondió con el código "
            f"{response.status_code}: {response.text}"
        )

    print("Dashboard enviado correctamente a Discord.")