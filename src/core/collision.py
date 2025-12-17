from __future__ import annotations
import pygame

def move_rect_with_collisions(rect: pygame.Rect, dx: float, dy: float, colliders: list[pygame.Rect]) -> pygame.Rect:
    r = rect.copy()
    r.x += int(round(dx))
    for c in colliders:
        if r.colliderect(c):
            if dx > 0: r.right = c.left
            elif dx < 0: r.left = c.right
    r.y += int(round(dy))
    for c in colliders:
        if r.colliderect(c):
            if dy > 0: r.bottom = c.top
            elif dy < 0: r.top = c.bottom
    return r
