import pygame

from scenes.base import Scene
from lib.monster import Monster


class PathScene(Scene):
    def __init__(self, width: int, height: int) -> None:
        def spawn_func() -> None:
            spawn = {
                Monster: 1,
            }
            self.screen.field.set_monster_spawn(
                spawn, self.screen.field.get_next_path()
            )

        super(PathScene, self).__init__(width, height, spawn_func)

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
