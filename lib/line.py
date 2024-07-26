from lib.util import Coordinate, RED
import math
import pygame
from pygame.math import Vector2
from typing import Callable


class Line:
    _active: bool = False
    _start: Coordinate = None
    _end: Coordinate = None
    _max_distance: int = 25

    def __init__(
        self,
        start_cb: Callable[[Coordinate], None] = None,
        end_cb: Callable[[int, Vector2], None] = None,
    ) -> None:
        self._start_cb = start_cb
        self._end_cb = end_cb

    def start_line(self, dot: Coordinate) -> None:
        self._active = True
        self._start = dot
        self._end = dot
        if self._start_cb:
            self._start_cb(self._start)

    def end_line(self, dot: Coordinate) -> None:
        self._end = self._max(dot)
        self._active = False
        if self._end_cb:
            magnitude = self._magnitude(self._start, self._end)
            unit = self._unit(self._start, self._end, magnitude=magnitude)
            self._end_cb(magnitude, unit)

    def update_line(self, dot: Coordinate) -> None:
        if self._active:
            self._end = self._max(dot)

    def draw(self, surface: pygame.Surface) -> None:
        if self._active:
            pygame.draw.line(surface, RED, self._start, self._end, 1)

    def _magnitude(self, a: Coordinate, b: Coordinate) -> int:
        return math.sqrt(pow(b[0] - a[0], 2) + pow(b[1] - a[1], 2))

    def _unit(self, a: Coordinate, b: Coordinate, magnitude: int = None) -> Vector2:
        magnitude = magnitude or self._magnitude(a, b)
        return Vector2((b[0] - a[0]) / magnitude, (b[1] - a[1]) / magnitude)

    def _max(self, dot: Coordinate) -> Coordinate:
        magnitude = self._magnitude(dot, self._start)
        return (
            self._get_dot_on_line(
                self._start, dot, self._max_distance, magnitude=magnitude
            )
            if magnitude > self._max_distance
            else dot
        )

    def _get_dot_on_line(
        self, a: Coordinate, b: Coordinate, distance: int, magnitude: int = None
    ) -> Coordinate:
        magnitude = magnitude or self._magnitude(a, b)
        unit = self._unit(a, b, magnitude=magnitude)
        delta = unit * distance
        return (a[0] + delta.x, a[1] + delta.y)
