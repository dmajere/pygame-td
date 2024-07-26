import pygame
from pygame.math import Vector2
from lib.util import Coordinate


class Bullet(pygame.sprite.Sprite):
    def __init__(self, size: Coordinate, pos: Coordinate, mass: int) -> None:
        super(Bullet, self).__init__()

        self.image = pygame.Surface(size)
        self.image.fill("gray")
        self.border = pygame.rect.Rect((0, 0), size)
        pygame.draw.rect(self.image, "black", self.border, 1)
        self.rect = self.image.get_rect(center=pos)

        self.mass = mass
        self.velocity = 0
        self.acceleration = 0
        self.unit = Vector2(0, 0)

    def shoot(self, unit, momentum, friction: int):
        self.friction = friction
        self.unit = Vector2(unit)
        self.velocity = momentum // self.mass
        self.acceleration = friction // self.mass

    def update(self) -> None:
        if self.velocity < 0:
            self.on_max_distance()
            self.kill()

        delta = self.unit * self.velocity
        self.velocity -= self.acceleration
        pos = Vector2(self.rect.center) + delta
        self.rect.center = pos

    def on_max_distance(self) -> None:
        """Action on reaching max projectile distance"""
        pass
