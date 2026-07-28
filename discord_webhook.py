import requests

from config import DISCORD_WEBHOOK_URL


MODE_NAMES = {
    "a": "Arcade",
    "r": "Realistic",
    "s": "Simulator"
}

MEDALS = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

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
        "title": "🌸TAIKO — Estadísticas del escuadrón🌸",
        "description": (
            f"Resumen de estadísticas en modo **{mode_name}**."
        ),
        "color": 16230584,
        "fields": fields,
        "footer": {
            "text": "ThunderSkill.com"
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

    print(f"Discord respondió con código {response.status_code}")
    
    if response.status_code not in (200, 204):
        raise RuntimeError(
            f"Discord respondió con el código "
            f"{response.status_code}: {response.text}"
        )

    print("Dashboard enviado correctamente a Discord.")

def format_top_kpd(players, mode):
    """
    REEMPLAZADO PARA MOSTRAR KPD Y NO KD xd

    Convierte una lista de jugadores en texto para el embed.
     
    players: lista devuelta por SquadronStats.top()
    mode: "s" para simulador o "r" para realista
    """

    if not players:
        return "No se encontraron jugadores suficientes."

    lines = []

    for position, player in enumerate(players):
        nickname = player.get("nick", "Desconocido")
        mode_stats = player.get(mode, {})

        kpd = mode_stats.get("kpd") or 0
        previous_kpd = mode_stats.get("prev_kpd")
        missions = mode_stats.get("mission") or 0


        if previous_kpd is None: 
            comparison = "Sin datos"
        else:
            difference = float(kpd) - float(previous_kpd)
            
            if difference > 0:
                comparison = f"📈 +{difference:.2f}"
            elif difference < 0:
                comparison = f"📉 {difference:.2f}"
            else:
                comparison = "➖ 0.00"       

        medal = MEDALS[position]

        lines.append(
            f"{medal} **{nickname}**\n"
            f"`{float(kpd):.2f}` {comparison} · {int(missions)} partidas"
        )

    return "\n\n".join(lines)


def send_top_kpd(top_simulator, top_realistic):
    """
    REEMPLAZADO PARA MOSTRAR KPD Y NO KD
    """

    if not DISCORD_WEBHOOK_URL:
        raise ValueError(
            "No se encontró la variable de entorno DISCORD_WEBHOOK_URL."
        )

    simulator_text = format_top_kpd(
        top_simulator,
        mode="s"
    )

    realistic_text = format_top_kpd(
        top_realistic,
        mode="r"
    )

    embed = {
        "title": "🏆 Top 5 Eficiencia en Batallas",
        "description": (
            "Mejores jugadores del escuadrón en batallas "
            "de Simulador y Realistas."
        ),
        "color": 16230584,
        "fields": [
            {
                "name": "🛩️ Simulador",
                "value": simulator_text,
                "inline": True
            },
            {
                "name": "⚔️ Realista",
                "value": realistic_text,
                "inline": True
            }
        ],
        "footer": {
            "text": "Mostrando Mínimo de 50 partidas"
        }
    }

    response = requests.post(
        DISCORD_WEBHOOK_URL,
        json={
            "embeds": [embed]
        },
        timeout=15
    )

    response.raise_for_status()

    print("Embed Top 5 KpD enviado correctamente.")    