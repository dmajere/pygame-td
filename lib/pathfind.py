from lib.util import Coordinate
from typing import Tuple, List
from queue import Queue


class PathFinder:
    queue = Queue()

    def __init__(self, tiles, spawn: Tuple[int, int], goal: Tuple[int, int]) -> None:
        self.tiles = tiles
        self.spawn_tile = spawn
        self.goal_tile = goal

    def get_adjacent_tiles(self, tile: Tuple[int, int]) -> List[Tuple[int, int]]:
        tiles = []
        if tile[0] > 0:
            tiles.append((tile[0] - 1, tile[1]))  # left
        if tile[0] < len(self.tiles) - 1:
            tiles.append((tile[0] + 1, tile[1]))  # right
        if tile[1] > 0:
            tiles.append((tile[0], tile[1] - 1))  # top
        if tile[1] < len(self.tiles[0]) - 1:
            tiles.append((tile[0], tile[1] + 1))  # bottom
        return tiles

    def set_tile_weights(self):
        tile = self.tiles[self.goal_tile[0]][self.goal_tile[1]]
        for t in self.get_adjacent_tiles(self.goal_tile):
            self.queue.put((tile.weight, t))

        while not self.queue.empty():
            parent_weight, pos = self.queue.get_nowait()
            tile = self.tiles[pos[0]][pos[1]]
            if tile.weight is None:
                tile.weight = parent_weight + 1
                for t in self.get_adjacent_tiles(pos):
                    self.queue.put((tile.weight, t))

    def get_tile(self, pos):
        return self.tiles[pos[0]][pos[1]]

    def get_path(self) -> List[Coordinate]:
        pos = self.spawn_tile
        current_tile = self.get_tile(pos)
        path = [current_tile.rect.center]

        while current_tile.weight != 0:
            for adj in self.get_adjacent_tiles(pos):
                next_tile = self.get_tile(adj)
                if next_tile.weight < current_tile.weight:
                    path.append(next_tile.rect.center)
                    pos = adj
                    current_tile = next_tile
                    break
        return path
