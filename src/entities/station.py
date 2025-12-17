from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import pygame

class StationType(str, Enum):
    INGREDIENT="ingredient"
    PREP="prep"
    COUNTER="counter"
    WAITING="waiting"

@dataclass
class Station:
    station_type: StationType
    name: str
    rect: pygame.Rect
    solid: bool = True
    payload: str | None = None
