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
            # TODO: need to calculate target position properly,
            # right now its lagging
            self.shoot(target.rect.center + target.get_move_delta(dt))
            self.shoot_cooldown.activate()
