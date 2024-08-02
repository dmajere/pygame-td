import pygame
import math
from typing import Tuple, Iterable, Optional
from lib.util import Color, Coordinate, RED
from lib.bullet import Bullet
from pygame.math import Vector2 as vector
from lib.tiles import Tile
from lib.timer import Timer
from lib.monster import Monster


class Tower(pygame.sprite.Sprite):
    COLOR: Color = RED
    CONSTRUCTION_COLOR: Color = "pink"
    BULLET_SIZE: Tuple[int, int] = (4, 4)
    BULLET_MASS: float = 0.1
    BULLET_SPEED: float = 20.0
    VISION_DISTANCE = Tile.WIDTH * 3
    SHOOTING_RATE = 10

    def __init__(
        self,
        bullets: pygame.sprite.Group,
        size: Tuple[int, int] = (Tile.WIDTH, Tile.HEIGHT),
    ) -> None:
        super(Tower, self).__init__()

        self.image = pygame.Surface(size)
        self.image.fill(self.CONSTRUCTION_COLOR)

        self.border = pygame.rect.FRect((0, 0), size)
        pygame.draw.rect(self.image, "black", self.border, 1)

        self.rect = self.image.get_frect()
        self.bullets = bullets
        self.shoot_cooldown = Timer(1000 // self.SHOOTING_RATE)

    def build(self, pos: Coordinate) -> None:
        self.image.fill(self.COLOR)
        self.rect.topleft = pos

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

    def get_target_in_reach(self, monsters: Iterable[Monster]) -> Optional[Monster]:
        for monster in monsters:
            distance = self.get_target_distance(monster.rect.center)
            if distance <= self.VISION_DISTANCE:
                return monster

    def update(
        self,
        monster_sprites: Iterable[Monster],
        dt: float = 1.0,
    ) -> None:
        self.shoot_cooldown.update()
        target = self.get_target_in_reach(monster_sprites)
        if target and not self.shoot_cooldown.active:
            # For each visible target we try to calculate bullet interseciton point,
            # if there is no solution for it (target moving to fast to hit it).
            # Don't waste bullet try another target
            if aim := self.calculate_intersection(
                target.rect.center,
                target.direction,
                target.SPEED,
                self.rect.center,
                self.BULLET_SPEED,
                dt,
            ):
                self.shoot(aim)
                self.shoot_cooldown.activate()

    def calculate_intersection(
        self,
        target_start: Coordinate,
        target_direction: vector,
        target_speed: float,
        bullet_start: Coordinate,
        bullet_speed: float,
        dt: float,
    ) -> Optional[vector]:

        target_start = vector(target_start)
        target_direction = target_direction.normalize()
        bullet_start = vector(bullet_start)
        target_velocity = target_speed * target_direction
        relative_position = target_start - bullet_start

        # Solve for the time t
        a = target_velocity.length_squared() - bullet_speed**2
        b = 2 * relative_position.dot(target_velocity)
        c = relative_position.length_squared()

        # Solve the quadratic equation a*t^2 + b*t + c = 0
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            return None, "No solution, the bullet cannot intercept the target."

        # Calculate possible solutions for t
        t1 = (-b + discriminant**0.5) / (2 * a)
        t2 = (-b - discriminant**0.5) / (2 * a)
        t = max(t1, t2)
        if t < 0:
            return None, "No valid solution, the bullet cannot intercept the target."

        return target_start + target_velocity * t * dt
