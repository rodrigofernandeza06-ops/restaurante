from __future__ import annotations
from collections import Counter

class OrdersSystem:
    def __init__(self, recipes: dict[str, list[str]]) -> None:
        self.set_recipes(recipes)

    def set_recipes(self, recipes: dict[str, list[str]]) -> None:
        self._recipe = {k: Counter(v) for k, v in (recipes or {}).items()}

    def recipe_ids(self) -> list[str]:
        return list(self._recipe.keys())

    def find_match(self, inventory: list[str]) -> str | None:
        inv = Counter(inventory)
        for plate_id, req in self._recipe.items():
            if all(inv.get(ing, 0) >= cnt for ing, cnt in req.items()):
                return plate_id
        return None

    def consume_for(self, inventory: list[str], plate_id: str) -> bool:
        if plate_id not in self._recipe:
            return False
        req = self._recipe[plate_id]
        inv = Counter(inventory)
        if not all(inv.get(ing, 0) >= cnt for ing, cnt in req.items()):
            return False
        for ing, cnt in req.items():
            for _ in range(cnt):
                inventory.remove(ing)
        return True
