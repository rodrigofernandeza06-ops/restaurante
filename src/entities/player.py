from __future__ import annotations
import pygame
from config.settings import PLAYER
from core.collision import move_rect_with_collisions

class Player:
    def __init__(self, x: int, y: int, sprite: pygame.Surface) -> None:
        self.sprite = sprite
        w, h = self.sprite.get_size()
        self.rect = pygame.Rect(x, y, int(w*0.70), int(h*0.70))
        self._draw_offset = ((w - self.rect.w)//2, (h - self.rect.h)//2)
        self.speed = PLAYER.speed_px_s

        self.inventory: list[str] = []
        self.max_inventory = 3
        self.current_plate: str | None = None

        self.last_message = ""
        self.message_timer = 0.0

    def set_message(self, msg: str, seconds: float = 1.8) -> None:
        self.last_message = msg
        self.message_timer = seconds

    def update(self, dt: float, keys, colliders: list[pygame.Rect]) -> None:
        mx = 0.0; my = 0.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: mx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: mx += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]: my -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: my += 1
        if mx and my:
            mx *= 0.7071; my *= 0.7071
        self.rect = move_rect_with_collisions(self.rect, mx*self.speed*dt, my*self.speed*dt, colliders)
        if self.message_timer > 0:
            self.message_timer -= dt

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, (self.rect.x - self._draw_offset[0], self.rect.y - self._draw_offset[1]))

    def interact_zone(self) -> pygame.Rect:
        return self.rect.inflate(PLAYER.interact_range_px*2, PLAYER.interact_range_px*2)

    def try_add_item(self, item_code: str) -> bool:
        if self.current_plate is not None:
            return False
        if len(self.inventory) >= self.max_inventory:
            return False
        self.inventory.append(item_code)
        return True

    def can_prepare(self) -> bool:
        return self.current_plate is None

    def set_plate(self, plate_id: str) -> None:
        self.current_plate = plate_id

    def clear_plate(self) -> None:
        self.current_plate = None

    def drop_last_item(self) -> str | None:
        if not self.inventory:
            return None
        return self.inventory.pop()

    def drop_all_items(self) -> int:
        n = len(self.inventory)
        self.inventory.clear()
        return n
