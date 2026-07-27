class SquadronStats:

    def __init__(self, squad_info, players):
        self.squad = squad_info
        self.players = players

    def average(self, mode, stat):
        values = []

        for player in self.players:

            if mode not in player:
                continue

            stats = player[mode] or {}
            value = stats.get(stat)

            if value is None:
                continue

            try:
                values.append(float(value))
            except (TypeError, ValueError):
                continue

        if not values:
            return 0

        return round(sum(values) / len(values), 2)

    def top(self, mode, stat, limit=10, min_battles=0):
        ranking = []

        for player in self.players:

            if mode not in player:
                continue

            stats = player[mode] or {}

            if stat not in stats:
                continue

            missions = stats.get("mission") or 0
            value = stats.get(stat)

            if value is None:
                continue

            try:
                missions = int(missions)
                float(value)
            except (TypeError, ValueError):
                continue

            if missions < min_battles:
                continue

            ranking.append(player)

        ranking.sort(
            key=lambda p: float(p[mode][stat] or 0),
            reverse=True
        )

        return ranking[:limit]

    def best_player(self, mode, stat, min_battles=0):
        ranking = self.top(
            mode,
            stat,
            limit=1,
            min_battles=min_battles
        )

        if not ranking:
            return None

        return ranking[0]

    def dashboard(self, mode="s", min_battles=50):
        best_kd = self.best_player(
            mode,
            "kd",
            min_battles=min_battles
        )

        best_winrate = self.best_player(
            mode,
            "winrate",
            min_battles=min_battles
        )

        most_active = self.best_player(
            mode,
            "mission"
        )

        total_missions = sum(
            player.get(mode, {}).get("mission", 0) or 0
            for player in self.players
        )

        return {
            "members": len(self.players),
            "average_kd": self.average(mode, "kd"),
            "average_winrate": self.average(mode, "winrate"),
            "total_missions": total_missions,
            "best_kd": best_kd,
            "best_winrate": best_winrate,
            "most_active": most_active
        }