from __future__ import annotations
import pygame

class Customer:
    def __init__(self, rect: pygame.Rect, order_id: str, patience_sec: float, sprite: pygame.Surface) -> None:
        self.rect = rect
        self.order_id = order_id
        self.patience = patience_sec
        self.max_patience = patience_sec
        self.sprite = sprite

    def update(self, dt: float) -> None:
        self.patience -= dt

    def is_gone(self) -> bool:
        return self.patience <= 0

    def patience_ratio(self) -> float:
        return max(0.0, min(1.0, self.patience / self.max_patience)) if self.max_patience else 0.0

    def draw(self, screen: pygame.Surface) -> None:
        sw, sh = self.sprite.get_size()
        screen.blit(self.sprite, (self.rect.centerx - sw//2, self.rect.bottom - sh))
