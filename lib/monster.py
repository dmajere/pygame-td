import pygame
from lib.util import Coordinate


class PathFinding:
    def get_direction(self, current_pos: Coordinate):
        pass


class Monster(pygame.sprite.Sprite):
    def __init__(
        self, start_pos: Coordinate, end_pos: Coordinate, pf: PathFinding
    ) -> None:
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.pf = pf

        self.speed = 1

    def update(self) -> None:
        direction = self.pf.get_direction(self.rect.center)
        self.rect.center += direction * self.speed
