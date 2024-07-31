import pygame
import math
from typing import Tuple
from lib.util import Color, Coordinate
from lib.bullet import Bullet
from pygame.math import Vector2 as vector


class Tower(pygame.sprite.Sprite):
    COLOR: Color = "red"
    CONSTRUCTION_COLOR: Color = "pink"
    BULLET_SIZE: Tuple[int, int] = (4, 4)
    BULLET_MASS: float = 0.1
    BULLET_SPEED: float = 1.2

    def __init__(
        self, bullets: pygame.sprite.Group, size: Tuple[int, int] = (16, 16)
    ) -> None:
        super(Tower, self).__init__()

        self.image = pygame.Surface(size)
        self.image.fill(self.CONSTRUCTION_COLOR)

        self.border = pygame.rect.FRect((0, 0), size)
        pygame.draw.rect(self.image, "black", self.border, 1)

        self.rect = self.image.get_frect()
        self.bullets = bullets

    def build(self) -> None:
        self.image.fill(self.COLOR)

    def get_target_distance(self, target: Coordinate) -> int:
        return math.sqrt(
            pow(target[0] - self.rect.center[0], 2)
            + pow(target[1] - self.rect.center[1], 2)
        )

    def shoot(self, target: Coordinate) -> None:
        bullet = Bullet(self.BULLET_SIZE, self.rect.center, self.BULLET_MASS)
        self.bullets.add(bullet)
        distance = self.get_target_distance(target)
        direction = vector(
            (target[0] - self.rect.center[0]) / distance,
            (target[1] - self.rect.center[1]) / distance,
        )
        bullet.shoot(direction, self.BULLET_SPEED)
