from thunderskill import (
    download_data,
    get_players,
    get_squad_info
)

from stats import SquadronStats
from discord_webhook import send_dashboard, send_top_kpd


MODE = "s"
MIN_BATTLES = 50


def main():
    data = download_data()

    players = get_players(data)
    squad = get_squad_info(data)

    stats = SquadronStats(squad, players)

    dashboard = stats.dashboard(
        mode=MODE,
        min_battles=MIN_BATTLES
    )
    top_simulator = stats.top(
        mode="s",
        stat="kpd",
        limit=5,
        min_battles=50
    )

    top_realistic = stats.top(
        mode="r",
        stat="kpd",
        limit=5,
        min_battles=50
    )

    send_dashboard(
        dashboard,
        mode=MODE
    )
    send_top_kpd(
        top_simulator=top_simulator,
        top_realistic=top_realistic
    )


if __name__ == "__main__":
    main()