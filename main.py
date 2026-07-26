from thunderskill import (
    download_data,
    get_players,
    get_squad_info
)

from stats import SquadronStats
from discord_webhook import send_dashboard


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

    send_dashboard(
        dashboard,
        mode=MODE
    )


if __name__ == "__main__":
    main()