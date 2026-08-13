from thunderskill import (
    download_data,
    get_players,
    get_squad_info
)
from weekly_performance import (
    load_weekly_history,
    create_current_snapshot,
    calculate_weekly_performance,
    save_weekly_history
)

from stats import SquadronStats
from discord_webhook import send_dashboard, send_weekly_performance, send_squad_performance
from squad_performance import (
    get_current_performance,
    load_previous_performance,
    save_current_performance,
)

MODE = "s"
MIN_BATTLES = 50


def main():
    data = download_data()

    players = get_players(data)
    squad = get_squad_info(data)

    stats = SquadronStats(squad, players)


    previous_weekly = load_weekly_history()

    weekly_simulator = calculate_weekly_performance(
    players=players,
    previous_history=previous_weekly,
    mode="s",
    limit=5,
    min_battles=20
)

    weekly_realistic = calculate_weekly_performance(
    players=players,
    previous_history=previous_weekly,
    mode="r",
    limit=5,
    min_battles=20
)

    dashboard = stats.dashboard(
        mode=MODE,
        min_battles=MIN_BATTLES
    )

    current_performance = get_current_performance(data)
    previous_performance = load_previous_performance()

    send_dashboard(
        dashboard,
        mode=MODE
    )


    send_weekly_performance(
    top_simulator=weekly_simulator,
    top_realistic=weekly_realistic
    )

    send_squad_performance(
    current_performance=current_performance,
    previous_performance=previous_performance
    
    )
    save_current_performance(current_performance)
    
    
    current_weekly = create_current_snapshot(players)

    save_weekly_history(current_weekly)

if __name__ == "__main__":
    main()