import pygame
from typing import Callable
from pygame.math import Vector2 as vector
from lib.util import Coordinate


class Monster(pygame.sprite.Sprite):
    SIZE = (15, 15)
    SPEED = 1

    def __init__(
        self, start: Coordinate, path: "Path", on_goal_reached: Callable
    ) -> None:
        super(Monster, self).__init__()
        self.path = path
        self.on_goal_reached = on_goal_reached
        self.current_tile = 0
        self.direction = (0, 0)

        self.image = pygame.Surface(self.SIZE)
        self.image.fill("black")
        self.rect = self.image.get_frect(center=start)

    def get_direction(self, a: Coordinate, b: Coordinate) -> vector:
        diff = vector(b) - vector(a)
        norm = vector(abs(diff[0]), abs(diff[1]))
        return vector(
            diff[0] // norm[0] if diff[0] != 0 else diff[0],
            diff[1] // norm[1] if diff[1] != 0 else diff[1],
        )

    def update(self, dt: float) -> None:
        if self.current_tile == len(self.path) - 1:
            self.on_goal_reached()
            self.kill()

        if self.rect.center == self.path[self.current_tile]:
            self.current_tile += 1
            self.direction = self.get_direction(
                self.rect.center, self.path[self.current_tile]
            )
        self.rect.center += self.direction * self.SPEED * dt
