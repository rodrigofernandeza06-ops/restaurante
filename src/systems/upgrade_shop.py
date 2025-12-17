from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class UpgradeDef:
    id: str
    name: str
    base_cost: int
    cost_mult: float
    max_level: int
    desc: str

def _scaled_cost(base: int, mult: float, level: int) -> int:
    return int(round(base * (mult ** level)))

class UpgradeShopSystem:
    """Upgrades por niveles (puedes comprar la misma mejora varias veces)."""

    def __init__(self, upgrades: list[dict]) -> None:
        self.upgrades = [
            UpgradeDef(
                id=str(u.get("id")),
                name=str(u.get("name", u.get("id", "upgrade"))),
                base_cost=int(u.get("base_cost", u.get("cost", 0))),
                cost_mult=float(u.get("cost_mult", 1.35)),
                max_level=int(u.get("max_level", 1)),
                desc=str(u.get("desc", "")),
            )
            for u in (upgrades or [])
        ]
        self.levels: dict[str, int] = {}

    def load_unlocked(self, data) -> None:
        self.levels = {}
        if isinstance(data, dict):
            for k, v in data.items():
                try:
                    self.levels[str(k)] = max(0, int(v))
                except Exception:
                    self.levels[str(k)] = 1
        elif isinstance(data, list):
            for k in data:
                self.levels[str(k)] = 1

    def unlocked_list(self) -> dict[str, int]:
        return dict(self.levels)

    def level_of(self, upgrade_id: str) -> int:
        return int(self.levels.get(upgrade_id, 0))

    def next_cost(self, up: UpgradeDef) -> int:
        lvl = self.level_of(up.id)
        if lvl >= up.max_level:
            return 0
        return _scaled_cost(up.base_cost, up.cost_mult, lvl)

    def buy(self, idx: int, economy) -> tuple[bool, str]:
        if idx < 0 or idx >= len(self.upgrades):
            return False, "Upgrade inválido."
        up = self.upgrades[idx]
        lvl = self.level_of(up.id)
        if lvl >= up.max_level:
            return False, "Ya está al máximo."
        cost = self.next_cost(up)
        if economy.money < cost:
            return False, "No tienes dinero suficiente."
        economy.money -= cost
        self.levels[up.id] = lvl + 1
        return True, f"Comprado: {up.name} (nivel {lvl+1}/{up.max_level})"

    def apply_effects(self, *, economy, game_state, player, level_rules) -> None:
        # Defaults
        economy.money_bonus_flat = 0
        economy.fame_bonus_flat = 0
        game_state.spawn_interval_mult = 1.0
        player.max_inventory = 3
        level_rules.patience_mult_bonus = 1.0

        tips_lvl = self.level_of("better_tips")
        if tips_lvl:
            economy.money_bonus_flat += 5 * tips_lvl

        speed_lvl = self.level_of("faster_customers")
        if speed_lvl:
            game_state.spawn_interval_mult *= (0.90 ** speed_lvl)

        bag_lvl = self.level_of("bigger_bag")
        if bag_lvl:
            player.max_inventory = 3 + bag_lvl

        pat_lvl = self.level_of("patience_boost")
        if pat_lvl:
            level_rules.patience_mult_bonus *= (1.10 ** pat_lvl)

        fame_lvl = self.level_of("fame_boost")
        if fame_lvl:
            economy.fame_bonus_flat += 1 * fame_lvl
