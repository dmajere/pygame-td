import pygame
from typing import Iterable
from pygame.math import Vector2
from lib.monster import Monster
from lib.util import Coordinate


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self,
        size: Coordinate,
        pos: Coordinate,
        mass: int,
        damage: int,
    ) -> None:
        super(Bullet, self).__init__()

        self.image = pygame.Surface(size)
        self.image.fill("gray")
        self.border = pygame.rect.Rect((0, 0), size)
        pygame.draw.rect(self.image, "black", self.border, 1)
        self.rect = self.image.get_frect(center=pos)
        self.friction: float = 0.1

        self.mass = mass
        self.damage = damage
        self.velocity = 0
        self.acceleration = 0
        self.unit = Vector2(0, 0)

    def shoot(self, unit, speed):
        self.unit = Vector2(unit)
        self.velocity = speed // self.mass
        self.acceleration = self.friction // self.mass

    def update(self, targets: Iterable[Monster], dt: float) -> None:
        for target in targets:
            if target.rect.colliderect(self.rect):
                target.take_damage(self.damage)
                self.kill()
        if self.velocity < 0:
            self.on_max_distance()
            self.kill()
        if self.path_tile_reached():
            self.on_path_tile_reached()

        delta = self.unit * self.velocity * dt
        self.velocity -= self.acceleration
        pos = Vector2(self.rect.center) + delta
        self.rect.center = pos

    def path_tile_reached(self) -> bool:
        "not implemented"
        return False

    def on_max_distance(self) -> None:
        """Action on reaching max projectile distance"""
        pass

    def on_path_tile_reached(self) -> None:
        """Action or behavior change on monster path tile reached"""
        pass
