def get_average_stat(players, mode, stat):
    """
    Calcula el promedio de una estadística para todos los jugadores.
    """

    values = []

    for player in players:

        if mode not in player:
            continue

        if stat not in player[mode]:
            continue

        value = player[mode][stat]

        if value is None:
            continue

        values.append(value)

    if not values:
        return 0

    return round(sum(values) / len(values), 2)



def get_top_players(players, mode, stat, limit=10, min_battles=0):
    """
    Devuelve los mejores jugadores ordenados por una estadística.

    Parameters
    ----------
    players : list
        Lista de jugadores.
    mode : str
        "a", "r" o "s".
    stat : str
        Estadística por la cual ordenar.
    limit : int
        Número máximo de jugadores.
    min_battles : int
        Misiones mínimas requeridas.
    """

    ranking = []

    for player in players:

        if mode not in player:
            continue

        stats = player[mode]

        if stat not in stats:
            continue

        if stats.get("mission", 0) < min_battles:
            continue

        value = stats.get(stat)

        if value is None:
            continue

        ranking.append(player)

    ranking.sort(
        key=lambda p: p[mode][stat],
        reverse=True
    )

    return ranking[:limit]