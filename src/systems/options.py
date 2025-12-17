from __future__ import annotations
from dataclasses import dataclass
from utils.save_load import load_json, save_json

ACCENTS = {
    "yellow": (255, 200, 40),
    "red": (235, 90, 90),
    "blue": (90, 170, 255),
    "green": (80, 220, 150),
    "purple": (190, 120, 255),
}

DIFFICULTY = {
    "easy": {"spawn_mult": 1.15, "patience_mult": 1.15},
    "normal": {"spawn_mult": 1.0, "patience_mult": 1.0},
    "hard": {"spawn_mult": 0.85, "patience_mult": 0.85},
}

@dataclass
class Options:
    language: str = "es"
    difficulty: str = "normal"
    music_enabled: bool = True
    music_volume: float = 0.6
    brightness: float = 1.0
    accent: str = "yellow"
    menu_music: str = "menu_0.wav"
    game_music: str = "game_0.wav"

    @staticmethod
    def load() -> "Options":
        d = load_json("data/options.json", default={})
        o = Options()
        o.language = str(d.get("language", o.language))
        o.difficulty = str(d.get("difficulty", o.difficulty))
        o.music_enabled = bool(d.get("music_enabled", o.music_enabled))
        o.music_volume = float(d.get("music_volume", o.music_volume))
        o.brightness = float(d.get("brightness", o.brightness))
        o.accent = str(d.get("accent", o.accent))
        o.menu_music = str(d.get("menu_music", o.menu_music))
        o.game_music = str(d.get("game_music", o.game_music))
        o._sanitize()
        return o

    def save(self) -> None:
        save_json("data/options.json", {
            "language": self.language,
            "difficulty": self.difficulty,
            "music_enabled": self.music_enabled,
            "music_volume": float(self.music_volume),
            "brightness": float(self.brightness),
            "accent": self.accent,
            "menu_music": self.menu_music,
            "game_music": self.game_music,
        })

    def _sanitize(self) -> None:
        self.language = "en" if self.language.lower().startswith("en") else "es"
        self.difficulty = self.difficulty.lower()
        if self.difficulty not in DIFFICULTY:
            self.difficulty = "normal"
        self.music_volume = max(0.0, min(1.0, float(self.music_volume)))
        self.brightness = max(0.60, min(1.0, float(self.brightness)))
        if self.accent not in ACCENTS:
            self.accent = "yellow"

    def accent_rgb(self) -> tuple[int,int,int]:
        return ACCENTS.get(self.accent, ACCENTS["yellow"])

    def difficulty_params(self) -> dict:
        return DIFFICULTY.get(self.difficulty, DIFFICULTY["normal"])
