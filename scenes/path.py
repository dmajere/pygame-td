import pygame

from scenes.base import Scene
from lib.monster import Monster


class PathScene(Scene):
    def __init__(self, width: int, height: int) -> None:
        super(PathScene, self).__init__(width, height)
        self.screen.monsters = [{Monster: r * 10} for r in range(1, 21)]
