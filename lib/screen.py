import pygame
from lib.field import Field
from lib.tiles import Tile
from lib.util import Coordinate, Text, RED, BLACK
from lib.button import Button
from lib.tower import Tower
from lib.builder import Builder
from typing import Tuple, Callable, Iterable


class Hud:
    def __init__(
        self,
        spawn_func: Callable,
        available_towers: Iterable[Tuple[Tower, Callable]],
        enabled_towers: Tuple[Tower],
    ) -> None:
        self.font = pygame.font.Font(None, 50)

        self.spawn_button = Button(
            (255, 235, 153),
            on_click=spawn_func,
            text=Text(
                "Spawn",
                self.font,
                text_color=(51, 51, 51),
            ),
            text_margin=5,
            border_radius=5,
        )

        self.tower_buttons = {}
        self.enabled_towers = enabled_towers
        for tower, tower_click in available_towers:
            self.tower_buttons[tower.__name__] = Button(
                tower.COLOR,
                on_click=tower_click,
                width=24,
                height=24,
                hover_color=BLACK,
            )

    def draw(
        self,
        surface: pygame.Surface,
        size: Tuple[int, int],
        pos: Coordinate,
    ) -> None:

        self.spawn_button.draw(
            surface, (size[0] - self.spawn_button.rect.width // 2 - 10, pos[1] + 50)
        )
        for idx, tower in enumerate(self.enabled_towers):
            row = idx // 6 + 1
            col = idx // 3 + 1
            x = pos[0] + 2 * col + 24 * col
            y = pos[1] + 2 * row + 24 * row
            self.tower_buttons[tower].draw(surface, (x, y))

    def update(self, dt: int = 1) -> None:
        self.spawn_button.update(dt)
        for enabled_tower in self.enabled_towers:
            self.tower_buttons[enabled_tower].update(dt)


class Screen:
    def __init__(self, width: int, height: int, spawn: Callable) -> None:
        self.screen_width = width
        self.screen_height = height
        self.hud_height: int = 3 * Tile.HEIGHT

        self.field = Field(self.screen_width, self.screen_height - self.hud_height)
        self.builder = Builder(self.field)

        enabled_towers = [Tower.__name__]
        available_towers = [
            (Tower, lambda: self.builder.start(Tower, self.field.bullet_sprites))
        ]
        self.hud = Hud(spawn, available_towers, enabled_towers)

    def draw(self, surface: pygame.Surface) -> None:
        self.hud.draw(
            surface,
            (self.screen_width, self.hud_height),
            (0, self.screen_height - self.hud_height),
        )
        self.field.draw(surface, (0, 0))
        self.builder.draw(surface)

    def update(self, dt: float = 1.0) -> None:
        self.hud.update(dt)
        self.field.update(dt)
        self.builder.update(dt)
