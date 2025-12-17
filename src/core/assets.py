from __future__ import annotations
import pygame
from utils.paths import project_root
from config.settings import IMAGES_DIR, SFX_DIR

class AssetManager:
    def __init__(self) -> None:
        self._img_cache: dict[str, pygame.Surface] = {}

    def image(self, filename: str, size: tuple[int,int] | None = None) -> pygame.Surface:
        key = f"{filename}|{size}"
        if key in self._img_cache:
            return self._img_cache[key]
        p = project_root() / IMAGES_DIR / filename
        try:
            if p.exists():
                s = pygame.image.load(str(p)).convert_alpha()
            else:
                s = self._placeholder(size or (64,64), f"MISS\n{filename}")
        except Exception:
            s = self._placeholder(size or (64,64), f"ERR\n{filename}")
        if size and s.get_size() != size:
            s = pygame.transform.smoothscale(s, size)
        self._img_cache[key] = s
        return s

    def sfx_path(self, filename: str):
        return project_root() / SFX_DIR / filename

    def _placeholder(self, size: tuple[int,int], label: str) -> pygame.Surface:
        w,h = size
        surf = pygame.Surface((w,h), pygame.SRCALPHA)
        surf.fill((90,90,105,255))
        pygame.draw.rect(surf, (140,140,160), pygame.Rect(0,0,w,h), 2)
        pygame.font.init()
        f = pygame.font.SysFont("consolas", 12)
        y = 6
        for line in label.split("\n")[:3]:
            t = f.render(line[:14], True, (240,240,250))
            surf.blit(t, (6,y))
            y += 14
        return surf
