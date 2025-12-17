from __future__ import annotations
import pygame
from config.settings import COLORS, WINDOW

class HUD:
    def __init__(self) -> None:
        pygame.font.init()
        self.font = pygame.font.SysFont("segoeui", 18)
        self.small = pygame.font.SysFont("segoeui", 16)
        self.big = pygame.font.SysFont("segoeui", 22, bold=True)
        self.h1 = pygame.font.SysFont("segoeui", 34, bold=True)

    def draw(self, screen: pygame.Surface, *,
             accent: tuple[int,int,int],
             level:int, level_target:int,
             money:int, points:int, fame:int,
             inventory:list[str], plate:str|None,
             queue_orders:list[str], patience_ratio:float|None,
             message:str, message_active:bool,
             interact_prompt:str|None,
             paused:bool,
             upgrades_open:bool,
             upgrades_lines:list[str]|None=None,
             level_complete:bool=False) -> None:
        top = pygame.Rect(0,0,WINDOW.width,54)
        pygame.draw.rect(screen, COLORS.panel, top)
        pygame.draw.line(screen, COLORS.outline, (0, top.bottom), (WINDOW.width, top.bottom), 2)

        left = self.big.render(f"Nivel {level}   Dinero: {money}   Fama: {fame}", True, COLORS.text)
        screen.blit(left, (16, 14))

        pts = self.big.render(f"Puntos: {points}/{level_target}", True, accent)
        screen.blit(pts, (WINDOW.width - pts.get_width() - 16, 14))

        if queue_orders:
            order_txt = self.font.render("Pedidos: " + ", ".join(queue_orders[:3]) + (f" (+{len(queue_orders)-3})" if len(queue_orders) > 3 else ""), True, COLORS.text)
            screen.blit(order_txt, (WINDOW.width - order_txt.get_width() - 16, 54 + 8))

            if patience_ratio is not None:
                bar_w, bar_h = 240, 10
                bx, by = WINDOW.width - bar_w - 16, 54 + 30
                pygame.draw.rect(screen, COLORS.bar_bg, pygame.Rect(bx,by,bar_w,bar_h), border_radius=6)
                fill = int(bar_w * max(0.0, min(1.0, patience_ratio)))
                pygame.draw.rect(screen, COLORS.ok if patience_ratio > 0.35 else COLORS.danger,
                                 pygame.Rect(bx,by,fill,bar_h), border_radius=6)
                pygame.draw.rect(screen, COLORS.outline, pygame.Rect(bx,by,bar_w,bar_h), 1, border_radius=6)

        bottom = pygame.Rect(0, WINDOW.height-64, WINDOW.width, 64)
        pygame.draw.rect(screen, COLORS.panel, bottom)
        pygame.draw.line(screen, COLORS.outline, (0,bottom.y), (WINDOW.width,bottom.y), 2)

        inv = ", ".join(inventory) if inventory else "(vacío)"
        screen.blit(self.font.render(f"Inventario: {inv}", True, COLORS.text), (16, bottom.y+8))
        screen.blit(self.font.render(f"Plato listo: {plate if plate else '(ninguno)'}", True, COLORS.text), (16, bottom.y+34))

        if message_active:
            screen.blit(self.font.render(message, True, accent), (360, bottom.y+34))
        if interact_prompt:
            p = self.font.render(interact_prompt, True, COLORS.muted)
            screen.blit(p, (WINDOW.width - p.get_width() - 16, bottom.y+22))

        if paused:
            ov = pygame.Surface((WINDOW.width, WINDOW.height), pygame.SRCALPHA)
            ov.fill((0,0,0,130))
            screen.blit(ov,(0,0))
            box = pygame.Rect(WINDOW.width//2-220, WINDOW.height//2-90, 440, 180)
            pygame.draw.rect(screen, COLORS.panel, box, border_radius=16)
            pygame.draw.rect(screen, COLORS.outline, box, 2, border_radius=16)
            screen.blit(self.h1.render("PAUSA", True, COLORS.text), (box.centerx-70, box.y+20))
            screen.blit(self.font.render("ESC: reanudar", True, COLORS.muted), (box.x+140, box.y+90))
            screen.blit(self.font.render("Q: volver al menú", True, COLORS.muted), (box.x+140, box.y+120))

        if upgrades_open:
            ov = pygame.Surface((WINDOW.width, WINDOW.height), pygame.SRCALPHA)
            ov.fill((0,0,0,150))
            screen.blit(ov,(0,0))
            box = pygame.Rect(WINDOW.width//2-320, WINDOW.height//2-180, 640, 360)
            pygame.draw.rect(screen, COLORS.panel, box, border_radius=16)
            pygame.draw.rect(screen, COLORS.outline, box, 2, border_radius=16)
            screen.blit(self.h1.render("UPGRADES (U)", True, COLORS.text), (box.x+18, box.y+16))
            y = box.y+68
            for line in (upgrades_lines or [])[:12]:
                col = COLORS.muted if "[COMPRADO]" in line else COLORS.text
                screen.blit(self.font.render(line, True, col), (box.x+18, y))
                y += 26
            screen.blit(self.small.render("Compra con teclas 1..9", True, COLORS.muted), (box.x+18, box.bottom-26))

        if level_complete:
            ov = pygame.Surface((WINDOW.width, WINDOW.height), pygame.SRCALPHA)
            ov.fill((0,0,0,170))
            screen.blit(ov,(0,0))
            box = pygame.Rect(WINDOW.width//2-260, WINDOW.height//2-110, 520, 220)
            pygame.draw.rect(screen, COLORS.panel, box, border_radius=18)
            pygame.draw.rect(screen, COLORS.outline, box, 2, border_radius=18)
            screen.blit(self.h1.render("¡NIVEL COMPLETADO!", True, accent), (box.centerx-190, box.y+34))
            screen.blit(self.font.render("ENTER: siguiente nivel", True, COLORS.text), (box.x+160, box.y+120))
            screen.blit(self.small.render("ESC: menú (se guarda)", True, COLORS.muted), (box.x+175, box.y+154))
