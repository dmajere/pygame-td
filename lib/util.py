from typing import Tuple, TypeVar, Union


T = TypeVar("T")
Coordinate = Tuple[int, int]
Pair = Tuple[T, T]

Color = Union[Tuple[int, int, int], str]

RED: Color = (255, 0, 0)
