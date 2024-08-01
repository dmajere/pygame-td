import pygame
from lib.field import Field
from lib.tiles import Tile
from lib.util import Coordinate
from lib.button import Button
from typing import Tuple, Callable


class Hud:
    def __init__(self, size: Tuple[int, int], spawn_func: Callable) -> None:
        self.width, self.height = size
        self.font = pygame.font.Font(None, 50)

        self.surface = pygame.Surface(size)
        self.surface.fill("white")
        self.spawn_button = Button(
            "yellow",
            on_click=spawn_func,
            margin=2,
            text="spawn",
            text_font=self.font,
        )
        self.spawn_button.draw(
            self.surface, (self.width - self.spawn_button.rect.width // 2 - 10, 50)
        )

    def draw(self, surface: pygame.Surface, pos: Coordinate) -> None:
        surface.blit(self.surface, pos)


class Screen:
    def __init__(self, width: int, height: int, spawn: Callable) -> None:
        self.screen_width = width
        self.screen_height = height
        self.hud_height: int = 3 * Tile.HEIGHT

        self.field = Field(self.screen_width, self.screen_height - self.hud_height)
        self.hud = Hud((self.screen_width, self.hud_height), spawn)

    def draw(self, surface: pygame.Surface) -> None:
        self.field.draw(surface, (0, 0))
        self.hud.draw(surface, (0, self.screen_height - self.hud_height))
