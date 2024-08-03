import sys
import pygame
from lib.util import Color
from typing import Dict, Callable
from lib.timer import Timer
from queue import Queue


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

    def __init__(
        self, monster_sprites: pygame.sprite.Group, monster_on_reach: Callable
    ) -> None:
        super().__init__()
        self.monster_sprites = monster_sprites
        self.monster_on_reach = monster_on_reach
        self.spawn_timer = Timer(1200)
        self.spawn_queue = Queue()

    def spawn(self, monsters: Dict[type, int], path) -> None:
        if not self.next_spawn:
            self.next_spawn = monsters
            self.path = path

    def update(self, _: float = 1.0) -> None:
        super().__init__()
        self.spawn_timer.update()
        if self.next_spawn:
            for clz, num in self.next_spawn.items():
                for _ in range(num):
                    self.spawn_queue.put(
                        clz(self.rect.center, self.path, self.monster_on_reach)
                    )
            self.next_spawn = None
        elif not self.spawn_queue.empty() and not self.spawn_timer.active:
            self.monster_sprites.add(self.spawn_queue.get())
            self.spawn_timer.activate()


class Goal(Tile):
    COLOR: Color = "green"
    used = True
    weight = 0
    health = 100
