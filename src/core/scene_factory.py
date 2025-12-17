from __future__ import annotations
from typing import TYPE_CHECKING
from core.scene_ids import SceneId
if TYPE_CHECKING:
    from core.game import Game
    from scenes.base_scene import Scene

def build_scene(scene_id: SceneId, game: "Game") -> "Scene":
    if scene_id == SceneId.MENU:
        from scenes.menu_scene import MenuScene
        return MenuScene(game)
    if scene_id == SceneId.GAME:
        from scenes.game_scene import GameScene
        return GameScene(game)
    raise ValueError(scene_id)
