import pygame

from scenes.base import Scene
from lib.monster import Monster


class PathScene(Scene):
    def __init__(self, width: int, height: int) -> None:
        super(PathScene, self).__init__(width, height)
        spawn = {
            Monster: 1,
        }
        self.field.set_monster_spawn(spawn, self.field.get_next_path())

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
