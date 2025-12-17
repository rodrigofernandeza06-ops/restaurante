from __future__ import annotations
import pygame
from systems.options import Options

class AudioManager:
    def __init__(self) -> None:
        self.ready = False
        self.current_track: str | None = None

    def init(self) -> None:
        try:
            pygame.mixer.init()
            self.ready = True
        except Exception:
            self.ready = False

    def apply_options(self, opt: Options) -> None:
        if not self.ready:
            return
        pygame.mixer.music.set_volume(float(opt.music_volume) if opt.music_enabled else 0.0)

    def play_music(self, filepath: str, loop: bool = True) -> None:
        if not self.ready:
            return
        if self.current_track == filepath:
            return
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_track = filepath
        except Exception:
            self.current_track = None

    def stop_music(self) -> None:
        if not self.ready:
            return
        pygame.mixer.music.stop()
        self.current_track = None
