from __future__ import annotations
import random
import pygame

from scenes.base_scene import BaseScene
from config.settings import COLORS, WINDOW, PLAYER
from core.scene_ids import SceneId
from entities.player import Player
from entities.station import Station, StationType
from entities.customer import Customer
from systems.orders import OrdersSystem
from systems.economy import EconomySystem
from systems.upgrade_shop import UpgradeShopSystem
from systems.level_progression import LevelProgression
from ui.hud import HUD
from utils.save_load import load_json, save_json
from utils.i18n import t

class _LevelRules:
    def __init__(self) -> None:
        self.patience_mult_bonus = 1.0

class _GameState:

    def __init__(self) -> None:
        self.spawn_interval_mult = 1.0

class GameScene(BaseScene):
    def __init__(self, game) -> None:
        super().__init__(game)
        cfg = load_json("config/game_config.json", default={})
        self.levels = LevelProgression(cfg.get("levels", []))
        self.recipes_by_level = cfg.get("recipes_by_level", {})
        self.econ_cfg = cfg.get("economy", {})
        self.upgrades_cfg = cfg.get("upgrades", [])

        self.orders = OrdersSystem(self._recipes_for_level(1))
        self.economy = EconomySystem(leave_fame_penalty=int(self.econ_cfg.get("leave_fame_penalty", 1)))
        self.shop = UpgradeShopSystem(self.upgrades_cfg)
        self.state = _GameState()
        self.level_rules = _LevelRules()
        self.hud = HUD()

        self.kitchen_rect = pygame.Rect(40, 70, WINDOW.width - 80, WINDOW.height - 140)
        self.wall_colliders = self._build_walls(18)

        self.floor_tile = self.game.assets.image("floor.png", size=(64,64))

        self.player = Player(self.kitchen_rect.centerx, self.kitchen_rect.bottom - 90, self.game.assets.image("player.png", size=PLAYER.sprite_size))
        self.customers: list[Customer] = []
        self._spawn_timer = 0.0
        self._customer_sprite = self.game.assets.image("customer.png", size=(44, 52))

        self.near_station: Station | None = None
        self.paused = False
        self.upgrades_open = False
        self.level_complete = False

        self.level = 1
        self.level_target = 200
        self.base_spawn_interval = 6.0
        self.patience_sec = 20.0
        self.max_queue = 1
        self.active_ingredients: list[str] = ["I1","I2","I3"]

        self._load_progress()
        self._apply_level_rules()
        self._rebuild_stations()
        self._reapply_upgrades()
        self._start_game_music()

    def _recipes_for_level(self, level: int) -> dict:
        return self.recipes_by_level.get(str(level), self.recipes_by_level.get("1", {}))

    def _load_progress(self) -> None:
        data = load_json("data/save.json", default={"money":0,"points":0,"fame":0,"unlocked_upgrades":[], "level":1})
        self.economy.load_from(data)
        self.shop.load_unlocked(data.get("unlocked_upgrades", {}))
        self.level = int(data.get("level", 1))
        self.player.set_message(f"Nivel {self.level}: meta {self.levels.points_target(self.level)} pts.", 2.0)

    def _save_progress(self) -> None:
        save_json("data/save.json", {**self.economy.to_dict(), "unlocked_upgrades": self.shop.unlocked_list(), "level": self.level})

    def on_exit(self) -> None:
        self._save_progress()

    def on_enter(self) -> None:
        self._start_game_music()

    def _start_game_music(self) -> None:
        opt = self.game.options
        self.game.audio.apply_options(opt)
        if opt.music_enabled:
            self.game.audio.play_music(str(self.game.assets.sfx_path(opt.game_music)), loop=True)

    def _apply_level_rules(self) -> None:
        diff = self.game.options.difficulty_params()
        self.level_target = self.levels.points_target(self.level)
        self.base_spawn_interval = self.levels.spawn_interval(self.level) / float(diff["spawn_mult"])
        self.patience_sec = self.levels.patience(self.level) * float(diff["patience_mult"]) * float(self.level_rules.patience_mult_bonus)
        self.max_queue = self.levels.max_queue(self.level)
        self.active_ingredients = self.levels.ingredients(self.level)
        rm, rp, rf = self.levels.rewards(self.level)
        self.economy.set_base_rewards(rm, rp, rf)
        self.orders.set_recipes(self._recipes_for_level(self.level))

    def _advance_level(self) -> None:
        self.level += 1
        self.level_complete = False
        self.customers.clear()
        self._spawn_timer = 0.0
        self.economy.points = 0
        self._apply_level_rules()
        self._rebuild_stations()
        self._reapply_upgrades()
        self._save_progress()
        self.player.set_message(f"Nivel {self.level}: meta {self.level_target} pts.", 2.0)

    def _reapply_upgrades(self) -> None:
        self.shop.apply_effects(economy=self.economy, game_state=self.state, player=self.player, level_rules=self.level_rules)

    def _build_walls(self, t: int) -> list[pygame.Rect]:
        k = self.kitchen_rect
        return [
            pygame.Rect(k.left - t, k.top - t, k.width + 2 * t, t),
            pygame.Rect(k.left - t, k.bottom, k.width + 2 * t, t),
            pygame.Rect(k.left - t, k.top, t, k.height),
            pygame.Rect(k.right, k.top, t, k.height),
        ]

    def _rebuild_stations(self) -> None:
        k = self.kitchen_rect
        stations: list[Station] = []
        x = k.left + 40
        y = k.top + 60
        w = 160
        h = 78
        gap = 12
        for idx, code in enumerate(self.active_ingredients):
            stations.append(Station(StationType.INGREDIENT, f"Ingrediente {code}", pygame.Rect(x, y + idx*(h+gap), w, h), True, payload=code))

        prep_x = k.right - 230
        if self.level >= 2:
            stations.append(Station(StationType.PREP, "Preparar 1", pygame.Rect(prep_x, k.top + 120, 180, 78), True))
            stations.append(Station(StationType.PREP, "Preparar 2", pygame.Rect(prep_x, k.top + 210, 180, 78), True))
            stations.append(Station(StationType.PREP, "Preparar 3", pygame.Rect(prep_x, k.top + 300, 180, 78), True))
        else:
            stations.append(Station(StationType.PREP, "Preparar", pygame.Rect(prep_x, k.top + 180, 180, 90), True))

        stations.append(Station(StationType.COUNTER, "Mostrador (Entregar)", pygame.Rect(k.centerx - 210, k.top + 16, 420, 70), True))
        stations.append(Station(StationType.WAITING, "Zona Espera Cliente", pygame.Rect(k.centerx - 220, k.bottom - 90, 440, 80), False))

        self.stations = stations
        self.station_colliders = [s.rect for s in self.stations if s.solid]

    def _waiting_zone(self) -> pygame.Rect:
        for s in self.stations:
            if s.station_type == StationType.WAITING:
                return s.rect
        return pygame.Rect(self.kitchen_rect.centerx - 220, self.kitchen_rect.bottom - 90, 440, 80)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if self.level_complete:
            if event.key == pygame.K_RETURN:
                self._advance_level()
            elif event.key == pygame.K_ESCAPE:
                self._save_progress()
                self.game.change_scene_id(SceneId.MENU)
            return

        if event.key == pygame.K_u:
            self.upgrades_open = not self.upgrades_open
            return

        if self.upgrades_open:
            if pygame.K_1 <= event.key <= pygame.K_9:
                idx = event.key - pygame.K_1
                ok, msg = self.shop.buy(idx, self.economy)
                self.player.set_message(msg, 2.0)
                if ok:
                    self._reapply_upgrades()
                    self._save_progress()
            return

        if event.key == pygame.K_ESCAPE:
            self.paused = not self.paused
            return

        if self.paused:
            if event.key == pygame.K_q:
                self._save_progress()
                self.game.change_scene_id(SceneId.MENU)
            return

        if event.key == pygame.K_r:
            if event.mod & pygame.KMOD_SHIFT:
                n = self.player.drop_all_items()
                self.player.set_message(t(self.game.options.language, "inv_drop_all") if n else t(self.game.options.language, "inv_empty"), 1.4)
            else:
                it = self.player.drop_last_item()
                self.player.set_message(f"Soltaste {it}." if it else t(self.game.options.language, "inv_empty"), 1.2)
            return

        if event.key == pygame.K_e:
            self._handle_interact()

    def _handle_interact(self) -> None:
        zone = self.player.interact_zone()
        candidates = [s for s in self.stations if zone.colliderect(s.rect)]
        if not candidates:
            self.player.set_message(t(self.game.options.language, "no_interact"), 1.2)
            return
        px, py = self.player.rect.center
        st = min(candidates, key=lambda s: (s.rect.centerx - px) ** 2 + (s.rect.centery - py) ** 2)

        if st.station_type == StationType.INGREDIENT and st.payload:
            ok = self.player.try_add_item(st.payload)
            self.player.set_message(f"Recogiste {st.payload}." if ok else "No puedes cargar más.", 1.2)
        elif st.station_type == StationType.PREP:
            self._try_prepare()
        elif st.station_type == StationType.COUNTER:
            self._try_deliver()

    def _try_prepare(self) -> None:
        if not self.player.can_prepare():
            self.player.set_message("Ya tienes un plato listo.", 1.4)
            return
        match = self.orders.find_match(self.player.inventory)
        if match is None:
            self.player.set_message(t(self.game.options.language, "need_ing"), 1.4)
            return
        if self.orders.consume_for(self.player.inventory, match):
            self.player.set_plate(match)
            self.player.set_message(f"Plato listo: {match}.", 1.4)

    def _try_deliver(self) -> None:
        if not self.customers:
            self.player.set_message(t(self.game.options.language, "no_customer"), 1.2)
            return
        if self.player.current_plate is None:
            self.player.set_message(t(self.game.options.language, "no_plate"), 1.2)
            return
        target = self.customers[0]
        if self.player.current_plate != target.order_id:
            self.player.set_message(f"{t(self.game.options.language,'wrong_order')} ({target.order_id})", 1.8)
            return

        self.economy.reward_sale()
        self.player.set_message(t(self.game.options.language,'correct'), 1.4)
        self.player.clear_plate()
        self.customers.pop(0)
        self._save_progress()

        if self.economy.points >= self.level_target:
            self.level_complete = True
            self._save_progress()

    def _effective_spawn_interval(self) -> float:
        return max(1.0, float(self.base_spawn_interval) * float(self.state.spawn_interval_mult))

    def _spawn_customer_if_needed(self, dt: float) -> None:
        if len(self.customers) >= self.max_queue:
            return
        self._spawn_timer += dt
        if self._spawn_timer < self._effective_spawn_interval():
            return
        self._spawn_timer = 0.0

        ids = self.orders.recipe_ids() or ["PlatoA"]
        order_id = random.choice(ids)
        z = self._waiting_zone()
        start_x = z.centerx - (self.max_queue-1)*60//2
        slot_i = len(self.customers)
        cx = start_x + slot_i*60
        c_rect = pygame.Rect(cx - 18, z.centery - 26, 36, 52)
        self.customers.append(Customer(c_rect, order_id, self.patience_sec, self._customer_sprite))
        self.player.set_message(f"{t(self.game.options.language,'arrived')}: {order_id}.", 1.2)

    def update(self, dt: float) -> None:
        if self.paused or self.upgrades_open or self.level_complete:
            return
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys, self.wall_colliders + self.station_colliders)

        self._spawn_customer_if_needed(dt)

        if self.customers:
            for c in list(self.customers):
                c.update(dt)
            if self.customers and self.customers[0].is_gone():
                self.customers.pop(0)
                self.economy.customer_left()
                self.player.set_message("El cliente se fue... (-fama)", 1.6)
                self._save_progress()

        zone = self.player.interact_zone()
        self.near_station = next((s for s in self.stations if zone.colliderect(s.rect)), None)

    def _upgrades_lines(self) -> list[str]:
        """Líneas del panel de upgrades (U)."""
        # Usar getattr para que nunca crashee aunque cambies módulos
        shop = getattr(self, "shop", None)
        economy = getattr(self, "economy", None)

        if shop is None or economy is None:
            return ["Upgrades no disponibles."]

        lines: list[str] = []
        upgrades = getattr(shop, "upgrades", [])
        for i, up in enumerate(upgrades[:9]):
            up_id = getattr(up, "id", f"up{i}")
            name = getattr(up, "name", up_id)
            desc = getattr(up, "desc", "")
            max_level = int(getattr(up, "max_level", 1))
            lvl = int(getattr(shop, "level_of", lambda _id: 0)(up_id))

            if lvl >= max_level:
                tag = f"[MAX {lvl}/{max_level}]"
            else:
                cost = int(getattr(shop, "next_cost", lambda _u: 0)(up))
                tag = f"(nivel {lvl}/{max_level} | costo {cost})"

            lines.append(f"{i+1}. {name} {tag} — {desc}")

        # Resumen de efectos (failsafe)
        state = getattr(self, "state", None)
        player = getattr(self, "player", None)
        level_rules = getattr(self, "level_rules", None)

        money_bonus = int(getattr(economy, "money_bonus_flat", 0))
        fame_bonus = int(getattr(economy, "fame_bonus_flat", 0))
        spawn_mult = float(getattr(state, "spawn_interval_mult", 1.0)) if state else 1.0
        inv = int(getattr(player, "max_inventory", 3)) if player else 3
        patience_mult = float(getattr(level_rules, "patience_mult_bonus", 1.0)) if level_rules else 1.0

        lines.append("")
        lines.append(
            f"Efectos: bonus dinero +{money_bonus} | bonus fama +{fame_bonus} | spawn x{spawn_mult:.2f} | inv {inv} | paciencia x{patience_mult:.2f}"
        )
        lines.append("Compra con teclas 1..9. U para cerrar.")
        return lines

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(COLORS.bg)

        k = self.kitchen_rect
        tw, th = self.floor_tile.get_size()
        for yy in range(k.y, k.y + k.h, th):
            for xx in range(k.x, k.x + k.w, tw):
                screen.blit(self.floor_tile, (xx, yy))

        pygame.draw.rect(screen, COLORS.outline, self.kitchen_rect, 2, border_radius=18)

        for s in self.stations:
            color = COLORS.panel if s.solid else (32, 32, 40)
            pygame.draw.rect(screen, color, s.rect, border_radius=10)
            pygame.draw.rect(screen, COLORS.outline, s.rect, 2, border_radius=10)
            getattr(self, '_draw_station_label', lambda *args, **kwargs: None)(screen, s)

        for c in self.customers:
            c.draw(screen)

        self.player.draw(screen)

        prompt = f"E: {self.near_station.name}" if self.near_station else None
        queue_orders = [c.order_id for c in self.customers]
        ratio = self.customers[0].patience_ratio() if self.customers else None
        upgrades_lines = self._upgrades_lines() if (self.upgrades_open and hasattr(self, '_upgrades_lines')) else None
        # Failsafe: nunca crashear por upgrades
        if self.upgrades_open and not upgrades_lines:
            upgrades_lines = ["(Sin datos de upgrades)"]


        self.hud.draw(
            screen,
            accent=self.game.options.accent_rgb(),
            level=self.level,
            level_target=self.level_target,
            money=self.economy.money,
            points=self.economy.points,
            fame=self.economy.fame,
            inventory=self.player.inventory,
            plate=self.player.current_plate,
            queue_orders=queue_orders,
            patience_ratio=ratio,
            message=self.player.last_message,
            message_active=self.player.message_timer > 0,
            interact_prompt=prompt,
            paused=self.paused,
            upgrades_open=self.upgrades_open,
            upgrades_lines=upgrades_lines,
            level_complete=self.level_complete,
        )

        self._apply_brightness_overlay(screen)

