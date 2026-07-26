import json
from stats import get_average_stat, get_top_players

from thunderskill import (
    download_data,
    get_players,
    get_squad_info
)

print("Descargando datos...")

data = download_data()

squad = get_squad_info(data)
players = get_players(data)

print("\n===== TOP 10 KD SIMULATOR =====\n")

top = get_top_players(
    players,
    "s",
    "kd",
    limit=10,
    min_battles=50
)

print("\n===== TOP KD SIMULATOR =====\n")

for i, player in enumerate(top, start=1):

    print(
        f"{i:2}. "
        f"{player['nick']:<20}"
        f"KD: {player['s']['kd']:<5} "
        f"WR: {player['s']['winrate']}%"
    )