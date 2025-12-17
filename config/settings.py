from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class WindowConfig:
    title: str = "Restaurante Tycoon — MVP"
    width: int = 960
    height: int = 540
    fps: int = 60

@dataclass(frozen=True)
class Colors:
    bg = (24, 24, 28)
    panel = (35, 35, 42)
    text = (235, 235, 245)
    muted = (170, 170, 185)
    accent = (255, 200, 40)
    danger = (220, 70, 70)
    ok = (70, 200, 120)
    outline = (80, 80, 95)
    bar_bg = (22, 22, 26)

@dataclass(frozen=True)
class PlayerConfig:
    speed_px_s: float = 230.0
    sprite_size: tuple[int, int] = (44, 44)
    interact_range_px: int = 26

WINDOW = WindowConfig()
COLORS = Colors()
PLAYER = PlayerConfig()

ASSETS_DIR = Path("assets")
IMAGES_DIR = ASSETS_DIR / "images"
SFX_DIR = ASSETS_DIR / "sfx"
