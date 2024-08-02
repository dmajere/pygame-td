import sys
import pygame
from lib.util import Color
from typing import Dict


class Tile(pygame.sprite.Sprite):
    WIDTH: int = 32
    HEIGHT: int = 32
    COLOR: Color = "white"
    weight = None
    used = False

    def __init__(self) -> None:
        super(Tile, self).__init__()
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(self.COLOR)
        self.border = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        pygame.draw.rect(self.image, "gray", self.border, 1)
        self.rect = self.image.get_frect()


class Spawn(Tile):
    COLOR: Color = "black"
    weight = sys.maxsize
    next_spawn = None
    path = None
    used = True

    def __init__(self, monster_sprites: pygame.sprite.Group) -> None:
        super().__init__()
        self.monster_sprites = monster_sprites

    def set(self, monsters: Dict[type, int], path) -> None:
        self.next_spawn = monsters
        self.path = path

    def update(self, _: float = 1.0) -> None:
        super().__init__()
        if self.next_spawn:
            for clz, num in self.next_spawn.items():
                for _ in range(num):
                    self.monster_sprites.add(
                        clz(self.rect.center, self.path, lambda: print("Reached"))
                    )
            self.next_spawn = None


class Goal(Tile):
    COLOR: Color = "yellow"
    used = True
    weight = 0
