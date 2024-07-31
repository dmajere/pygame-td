from lib.util import Coordinate
from pygame.math import Vector2 as vector
from lib.field import Field, Tile


class PathFidner:
    def __init__(self, field: Field, spawn: Coordinate, goal: Coordinate) -> None:
        self.field = field
        self.spawn_tile = self.field.get_tile(spawn)
        self.goal_tile = self.field.get_tile(goal)
        self.field.tiles[self.goal_tile[0]][self.goal_tile[1]].weight = 0

    def calculate_path(self):
        pass

    def get_next(self, pos: Coordinate) -> Coordinate:
        current_tile = self.filed.get_tile(pos)
        # get next tile
        # return next_tile.rect.center
