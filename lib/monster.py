import pygame
from typing import Callable
from pygame.math import Vector2 as vector
from lib.util import Coordinate


class Monster(pygame.sprite.Sprite):
    SIZE = (15, 15)
    SPEED = 15
    HEALTH: float = 100

    def __init__(
        self, start: Coordinate, path: "Path", on_goal_reached: Callable
    ) -> None:
        super(Monster, self).__init__()
        self.path = path
        self.on_goal_reached = on_goal_reached
        self.current_tile = 0
        self.direction = vector(0, 0)

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

    def _min(self, a: vector, b: vector) -> vector:
        if a.x != b.x:
            return a if a.x < b.x else b
        return a if a.y < b.y else b

    def get_move_delta(self, dt: float) -> vector:
        return self.direction * self.SPEED * dt

    def take_damage(self, damage: float):
        self.HEALTH -= damage
        if self.HEALTH <= 0:
            self.kill()

    def update(self, dt: float) -> None:

        if self.current_tile == len(self.path) - 1:
            self.on_goal_reached()
            self.kill()

        cx, cy = self.rect.center
        cx, cy = int(cx), int(cy)

        px, py = self.path[self.current_tile]
        px, py = int(px), int(py)

        if cx == px and cy == py:
            self.current_tile += 1
            px, py = self.path[self.current_tile]
            px, py = int(px), int(py)
            self.direction = self.get_direction((cx, cy), (px, py))

        self.rect.center += self.get_move_delta(dt)
