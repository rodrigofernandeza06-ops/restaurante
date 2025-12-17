from __future__ import annotations
import pygame
from config.settings import WINDOW
from core.scene_ids import SceneId
from core.scene_factory import build_scene
from core.assets import AssetManager
from core.audio import AudioManager
from utils.audio_gen import ensure_music_files
from systems.options import Options

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(WINDOW.title)
        self.screen = pygame.display.set_mode((WINDOW.width, WINDOW.height))
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.assets = AssetManager()
        self.audio = AudioManager()
        self.audio.init()

        ensure_music_files()
        self.options = Options.load()
        self.audio.apply_options(self.options)

        self.current_scene = build_scene(SceneId.MENU, self)

    def change_scene_id(self, scene_id: SceneId) -> None:
        self.current_scene.on_exit()
        self.current_scene = build_scene(scene_id, self)
        self.current_scene.on_enter()

    def quit(self) -> None:
        self.is_running = False

    def run(self) -> None:
        self.current_scene.on_enter()
        while self.is_running:
            dt = self.clock.tick(WINDOW.fps) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    break
                self.current_scene.handle_event(event)
            self.current_scene.update(dt)
            self.current_scene.draw(self.screen)
            pygame.display.flip()
        pygame.quit()
