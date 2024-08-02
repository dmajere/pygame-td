import pygame
from lib.field import Field
from lib.tiles import Tile
from lib.util import Coordinate, Text, RED, BLACK
from lib.button import Button
from typing import Tuple, Callable


class Hud:
    def __init__(self, spawn_func: Callable) -> None:
        self.font = pygame.font.Font(None, 50)

        spawn_text = Text(
            "Spawn",
            self.font,
            text_color=(51, 51, 51),
        )

        self.spawn_button = Button(
            (255, 235, 153),
            on_click=spawn_func,
            text=spawn_text,
            text_margin=5,
            border_radius=5,
        )

    def draw(
        self, surface: pygame.Surface, size: Tuple[int, int], pos: Coordinate
    ) -> None:
        self.spawn_button.draw(
            surface, (size[0] - self.spawn_button.rect.width // 2 - 10, pos[1] + 50)
        )

    def update(self, dt: int = 1) -> None:
        self.spawn_button.update(dt)


class Screen:
    def __init__(self, width: int, height: int, spawn: Callable) -> None:
        self.screen_width = width
        self.screen_height = height
        self.hud_height: int = 3 * Tile.HEIGHT

        self.field = Field(self.screen_width, self.screen_height - self.hud_height)
        self.hud = Hud(spawn)

    def draw(self, surface: pygame.Surface) -> None:
        self.field.draw(surface, (0, 0))
        self.hud.draw(
            surface,
            (self.screen_width, self.hud_height),
            (0, self.screen_height - self.hud_height),
        )

    def update(self, dt: float = 1.0) -> None:
        self.hud.update(dt)
        return
        self.field.update(dt)
