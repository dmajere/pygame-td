from lib.util import Coordinate
from typing import Tuple, List
from queue import PriorityQueue
import sys


class PathFinder:
    def __init__(self, tiles) -> None:
        self.tiles = tiles
        self.mem = {}

    def get_adjacent_tiles(self, tile: Tuple[int, int]) -> List[Tuple[int, int]]:
        i, j = tile
        return (
            (a, b)
            for a, b in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
            if 0 <= a < len(self.tiles)
            if 0 <= b < len(self.tiles[0])
            if self.get_tile((a, b)).weight != sys.maxsize
        )

    def get_tile(self, pos):
        return self.tiles[pos[0]][pos[1]]

    def get_path(self, start, goal):
        shortest_path = self.a_star_graph_search(
            start=start,
            goal=goal,
        )
        return shortest_path

    def a_star_graph_search(
        self,
        start,
        goal,
    ):
        visited = set()
        came_from = dict()
        distance = {start: 0}
        frontier = PriorityQueue()
        frontier.put((0, start))
        heuristic = self.get_heuristic()

        while not frontier.empty():
            node = frontier.get()[1]
            if node in visited:
                continue
            if node == goal:
                return self.reconstruct_path(came_from, start, node)
            visited.add(node)
            for successor in self.get_adjacent_tiles(node):
                frontier.put((distance[node] + 1 + heuristic(successor), successor))
                if (
                    successor not in distance
                    or distance[node] + 1 < distance[successor]
                ):
                    distance[successor] = distance[node] + 1
                    came_from[successor] = node
        return None

    def reconstruct_path(self, came_from, start, end):
        """
        >>> came_from = {'b': 'a', 'c': 'a', 'd': 'c', 'e': 'd', 'f': 'd'}
        >>> reconstruct_path(came_from, 'a', 'e')
        ['a', 'c', 'd', 'e']
        """
        reverse_path = [self.get_tile(end).rect.center]
        while end != start:
            end = came_from[end]
            reverse_path.append(self.get_tile(end).rect.center)
        return list(reversed(reverse_path))

    def get_heuristic(self):
        M, N = len(self.tiles), len(self.tiles[0])
        (a, b) = goal_cell = (M - 1, N - 1)

        def get_clear_path_distance_from_goal(cell):
            (i, j) = cell
            return max(abs(a - i), abs(b - j))

        return get_clear_path_distance_from_goal
