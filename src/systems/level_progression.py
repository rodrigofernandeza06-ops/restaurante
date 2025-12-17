from __future__ import annotations

class LevelProgression:
    def __init__(self, levels: list[dict]) -> None:
        self.levels = sorted(levels or [], key=lambda x: int(x.get("level", 1)))
        if not self.levels:
            self.levels = [{
                "level": 1, "points_target": 200,
                "spawn_interval_sec": 6, "patience_sec": 20,
                "reward_money": 10, "reward_points": 5, "reward_fame": 1,
                "ingredients": ["I1","I2","I3"],
                "max_queue": 1
            }]

    def get_level_cfg(self, level: int) -> dict:
        for c in self.levels:
            if int(c.get("level", 1)) == int(level):
                return c
        return self.levels[-1]

    def points_target(self, level: int) -> int:
        return int(self.get_level_cfg(level).get("points_target", 200))

    def spawn_interval(self, level: int) -> float:
        return float(self.get_level_cfg(level).get("spawn_interval_sec", 6))

    def patience(self, level: int) -> float:
        return float(self.get_level_cfg(level).get("patience_sec", 20))

    def rewards(self, level: int) -> tuple[int,int,int]:
        c = self.get_level_cfg(level)
        return int(c.get("reward_money", 10)), int(c.get("reward_points", 5)), int(c.get("reward_fame", 1))

    def ingredients(self, level: int) -> list[str]:
        return list(self.get_level_cfg(level).get("ingredients", ["I1","I2","I3"]))

    def max_queue(self, level: int) -> int:
        return int(self.get_level_cfg(level).get("max_queue", 1))
