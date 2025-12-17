from __future__ import annotations

class EconomySystem:
    def __init__(self, leave_fame_penalty: int = 1) -> None:
        self.money = 0
        self.points = 0
        self.fame = 0
        self.base_money = 10
        self.base_points = 5
        self.base_fame = 1
        self.leave_fame_penalty = int(leave_fame_penalty)
        self.money_bonus_flat = 0
        self.fame_bonus_flat = 0

    def set_base_rewards(self, money: int, points: int, fame: int) -> None:
        self.base_money = int(money)
        self.base_points = int(points)
        self.base_fame = int(fame)

    def reward_sale(self) -> None:
        self.money += int(self.base_money + self.money_bonus_flat)
        self.points += int(self.base_points)
        self.fame += int(self.base_fame + self.fame_bonus_flat)

    def customer_left(self) -> None:
        self.fame = max(0, self.fame - self.leave_fame_penalty)

    def to_dict(self) -> dict:
        return {"money": self.money, "points": self.points, "fame": self.fame}

    def load_from(self, data: dict) -> None:
        self.money = int(data.get("money", 0))
        self.points = int(data.get("points", 0))
        self.fame = int(data.get("fame", 0))
