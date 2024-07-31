from lib.util import Coordinate
from lib.field import Field, Tile


class PathFidner:
    def __init__(self, field: Field, spawn: Coordinate, goal: Coordinate) -> None:
        self.field = field
        self.spawn_tile = (spawn[0] // Tile.WIDTH, spawn[1] // Tile.HEIGHT)
        self.goal = goal

    def get_direction(self, pos: Coordinate) -> None:
        pass
