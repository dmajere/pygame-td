import pygame
from typing import Tuple, TypeVar, Union


T = TypeVar("T")
Coordinate = Tuple[int, int]
Pair = Tuple[T, T]

Color = Union[Tuple[int, int, int], str]

RED: Color = (255, 0, 0)
BLACK: Color = (0, 0, 0)


class Text(pygame.sprite.Sprite):
    def __init__(
        self,
        text: str,
        font: pygame.font.Font,
        text_color: Color = BLACK,
        background_color: Color = None,
    ) -> None:
        super().__init__()
        self.image = font.render(
            text, False, text_color, background_color
        ).convert_alpha()
        self.rect = self.image.get_rect()
