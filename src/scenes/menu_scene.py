from __future__ import annotations
import pygame
import random
from scenes.base_scene import BaseScene
from config.settings import COLORS, WINDOW
from core.scene_ids import SceneId
from utils.i18n import t
from systems.options import ACCENTS

class MenuScene(BaseScene):
    def _show_toast(self, text: str, ms: int = 2000) -> None:
        import pygame
        self._toast = text
        self._toast_until = pygame.time.get_ticks() + ms

    def __init__(self, game) -> None:
        super().__init__(game)
        pygame.font.init()
        self.title_font = pygame.font.SysFont("segoeui", 44, bold=True)
        self.font = pygame.font.SysFont("segoeui", 22, bold=True)
        self.small = pygame.font.SysFont("segoeui", 18)

        self.mode = "main"  # main/options
        self.main_items = ["play", "options", "exit"]
        self.opt_items = ["language", "difficulty", "music", "volume", "brightness", "accent", "back"]
        self.sel = 0
        self._exit_armed = False
        self._exit_armed_until = 0.0  # tiempo límite para confirmar salir
        self._toast = ""  # mensaje corto en menú
        self._toast_until = 0.0
        self._music_files = {"menu": ["menu_0.wav", "menu_1.wav"], "game": ["game_0.wav", "game_1.wav"]}

        if self.game.options.menu_music not in self._music_files["menu"]:
            self.game.options.menu_music = random.choice(self._music_files["menu"])
        if self.game.options.game_music not in self._music_files["game"]:
            self.game.options.game_music = random.choice(self._music_files["game"])
        self.game.options.save()

    def on_enter(self) -> None:
        opt = self.game.options
        self.game.audio.apply_options(opt)
        if opt.music_enabled:
            self.game.audio.play_music(str(self.game.assets.sfx_path(opt.menu_music)), loop=True)

    def _set_toast(self, msg: str, sec: float = 1.6) -> None:
        self._toast = msg
        self._toast_until = pygame.time.get_ticks() / 1000.0 + sec


    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if self.mode == "main":
            if event.key == pygame.K_UP:
                self.sel = (self.sel - 1) % len(self.main_items)
                self._exit_armed = False
            elif event.key == pygame.K_DOWN:
                self.sel = (self.sel + 1) % len(self.main_items)
                self._exit_armed = False
            elif event.key == pygame.K_RETURN:
                item = self.main_items[self.sel]
                if item == "play":
                    self.game.change_scene_id(SceneId.GAME)
                elif item == "options":
                    self.mode = "options"; self.sel = 0
                elif item == "exit":
                    now = pygame.time.get_ticks() / 1000.0
                    if (not self._exit_armed) or (now > self._exit_armed_until):
                        self._exit_armed = True
                        self._exit_armed_until = now + 2.0
                        self._set_toast("Presiona ENTER otra vez para SALIR")
                    else:
                        self.game.quit()
            elif event.key == pygame.K_ESCAPE:
                now = pygame.time.get_ticks() / 1000.0
                if (not self._exit_armed) or (now > self._exit_armed_until):
                    self._exit_armed = True
                    self._exit_armed_until = now + 2.0
                    self._set_toast("Presiona ESC otra vez para SALIR")
                else:
                    self.game.quit()
            return

        if event.key == pygame.K_ESCAPE:
            self._save_options(); self.mode = "main"; self.sel = 0; self._exit_armed = False; return
        if event.key == pygame.K_UP:
            self.sel = (self.sel - 1) % len(self.opt_items); return
        if event.key == pygame.K_DOWN:
            self.sel = (self.sel + 1) % len(self.opt_items); return

        key = self.opt_items[self.sel]
        if key == "back" and event.key == pygame.K_RETURN:
            self._save_options(); self.mode = "main"; self.sel = 0; self._exit_armed = False; return

        if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN):
            self._adjust_option(key, event.key); self._save_options(); return

    def _adjust_option(self, key: str, pressed: int) -> None:
        opt = self.game.options

        def next_in(lst, cur, step):
            if cur not in lst:
                return lst[0]
            i = lst.index(cur)
            return lst[(i + step) % len(lst)]

        step = 1 if pressed in (pygame.K_RIGHT, pygame.K_RETURN) else -1

        if key == "language":
            opt.language = next_in(["es","en"], opt.language, step)
        elif key == "difficulty":
            opt.difficulty = next_in(["easy","normal","hard"], opt.difficulty, step)
        elif key == "music":
            opt.music_enabled = not opt.music_enabled
        elif key == "volume":
            opt.music_volume = max(0.0, min(1.0, float(opt.music_volume) + (0.05 * step)))
        elif key == "brightness":
            opt.brightness = max(0.60, min(1.0, float(opt.brightness) + (0.05 * step)))
        elif key == "accent":
            opt.accent = next_in(list(ACCENTS.keys()), opt.accent, step)

        self.game.audio.apply_options(opt)
        if opt.music_enabled:
            self.game.audio.play_music(str(self.game.assets.sfx_path(opt.menu_music)), loop=True)
        else:
            self.game.audio.stop_music()

    def _save_options(self) -> None:
        self.game.options.save()

    def draw(self, screen: pygame.Surface) -> None:
        opt = self.game.options
        lang = opt.language
        accent = opt.accent_rgb()

        # Fondo de portada (si falta, usa placeholder y NO crashea)
        bg = self.game.assets.image("menu_bg.png", size=(WINDOW.width, WINDOW.height))
        screen.blit(bg, (0, 0))
        # Overlay para legibilidad
        ov = pygame.Surface((WINDOW.width, WINDOW.height), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 70))
        screen.blit(ov, (0, 0))
        title = self.title_font.render(t(lang, "title"), True, COLORS.text)
        cx = WINDOW.width // 2
        screen.blit(title, (cx - title.get_width() // 2, 110))

        if self.mode == "main":
            y = 220
            for i, k in enumerate(self.main_items):
                label = t(lang, f"menu_{k}")
                col = accent if i == self.sel else COLORS.text
                txt = self.font.render(label, True, col)
                screen.blit(txt, (cx - txt.get_width() // 2, y))
                y += 46
            hint = self.small.render("↑↓ ENTER  |  ESC", True, COLORS.muted)
            screen.blit(hint, (cx - hint.get_width() // 2, 420))
        else:
            box = pygame.Rect(cx - 340, 190, 680, 300)
            pygame.draw.rect(screen, COLORS.panel, box, border_radius=18)
            pygame.draw.rect(screen, COLORS.outline, box, 2, border_radius=18)
            head = self.font.render(t(lang, "options_title"), True, COLORS.text)
            screen.blit(head, (box.x + 20, box.y + 16))

            def opt_line(k):
                if k == "language":
                    return f"{t(lang,'opt_language')}: {opt.language.upper()}"
                if k == "difficulty":
                    return f"{t(lang,'opt_difficulty')}: {opt.difficulty.upper()}"
                if k == "music":
                    return f"{t(lang,'opt_music')}: {'ON' if opt.music_enabled else 'OFF'}"
                if k == "volume":
                    return f"{t(lang,'opt_volume')}: {int(opt.music_volume*100)}%"
                if k == "brightness":
                    return f"{t(lang,'opt_brightness')}: {int(opt.brightness*100)}%"
                if k == "accent":
                    return f"{t(lang,'opt_accent')}: {opt.accent.upper()}"
                if k == "back":
                    return t(lang, "opt_back")
                return k

            y = box.y + 70
            for i, k in enumerate(self.opt_items):
                col = accent if i == self.sel else COLORS.text
                line = self.small.render(opt_line(k), True, col)
                screen.blit(line, (box.x + 24, y))
                y += 32

            hint = self.small.render("↑↓  ←→  ENTER  |  ESC", True, COLORS.muted)
            screen.blit(hint, (cx - hint.get_width() // 2, 510 - 34))

        self._apply_brightness_overlay(screen)
# Toast (mensaje corto)
now = pygame.time.get_ticks() / 1000.0
