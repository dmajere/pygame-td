import sys
import pygame
from lib.field import Field
from lib.tiles import Tile
from lib.util import Coordinate, Text, RED, BLACK
from lib.button import Button
from lib.tower import Tower
from lib.builder import Builder
from typing import Tuple, Callable, Iterable

# TODO: should we put this logic in builder?
# but then what to do with hud buttons? need to figure out ownership
# should Builder be owned by HUD? This would simplify tower button on_click methods
TOWER_BUILD_HOTKEYS = {
    Tower.__name__: pygame.K_b,
}


class Hud:
    def __init__(
        self,
        spawn_func: Callable,
        available_towers: Iterable[Tuple[Tower, Callable]],
        enabled_towers: Tuple[Tower],
    ) -> None:
        self.font = pygame.font.Font(None, 50)
        self.active = True
        self.round = 0
        self.health = None

        self.spawn_button = Button(
            color=(255, 235, 153),
            inactive_color="grey",
            on_click=spawn_func,
            text=Text(
                "Spawn",
                self.font,
                text_color=(51, 51, 51),
            ),
            text_margin=5,
            border_radius=5,
        )

        self.health_text = Text(f"Health: {self.health}", self.font, RED)

        self.tower_buttons = {}
        self.enabled_towers = enabled_towers
        for tower, tower_click in available_towers:
            self.tower_buttons[tower.__name__] = Button(
                tower.COLOR,
                inactive_color="grey",
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

        spawn_button_x = size[0] - self.spawn_button.rect.width // 2 - 10
        self.spawn_button.draw(surface, (spawn_button_x, pos[1] + 50))
        health_button_x = (
            spawn_button_x
            - self.health_text.rect.width // 2
            - self.spawn_button.rect.width // 2
            - 10
        )
        self.health_text.rect.center = (health_button_x, pos[1] + 50)
        surface.blit(self.health_text.image, self.health_text.rect)

        for idx, tower in enumerate(self.enabled_towers):
            row = idx // 6 + 1
            col = idx // 3 + 1
            x = pos[0] + 2 * col + 24 * col
            y = pos[1] + 2 * row + 24 * row
            self.tower_buttons[tower].draw(surface, (x, y))

    def set_active(self, state: bool) -> None:
        self.active = state

    def update(self, dt: int = 1) -> None:
        self.health_text.update(f"Health: {self.health}")

        self.spawn_button.active = self.active
        for button in self.tower_buttons.values():
            button.active = self.active

        self.spawn_button.update(dt)
        for enabled_tower in self.enabled_towers:
            self.tower_buttons[enabled_tower].update(dt)

        if self.active:
            keys = pygame.key.get_pressed()
            for tower, key in TOWER_BUILD_HOTKEYS.items():
                if tower in self.enabled_towers and keys[key]:
                    self.tower_buttons[tower].on_click()


class Screen:
    def __init__(self, width: int, height: int) -> None:
        self.screen_width = width
        self.screen_height = height
        self.hud_height: int = 3 * Tile.HEIGHT

        self.field = Field(self.screen_width, self.screen_height - self.hud_height)
        self.builder = Builder(self.field)

        enabled_towers = [Tower.__name__]
        available_towers = [
            (Tower, lambda: self.builder.start(Tower, self.field.bullet_sprites))
        ]

        self.monsters = []

        def _spawn_func():
            self.hud.round += 1
            path = self.field.get_next_path()
            for s in self.field.spawn_sprites.sprites():
                s.spawn(self.monsters[self.hud.round - 1], path)

        self.hud = Hud(_spawn_func, available_towers, enabled_towers)

    def draw(self, surface: pygame.Surface) -> None:
        self.field.draw(surface, (0, 0))
        self.hud.draw(
            surface,
            (self.screen_width, self.hud_height),
            (0, self.screen_height - self.hud_height),
        )
        self.hud.health = self.field.goal_tile.health
        self.builder.draw(surface)

    def update(self, dt: float = 1.0) -> None:
        if self.field.goal_tile.health <= 0:
            # TODO: do proper Game over screen
            sys.exit()

        hud_active = not bool(len(self.field.monster_sprites.sprites()))
        self.hud.set_active(hud_active)
        self.hud.health = self.field.goal_tile.health

        self.hud.update(dt)
        self.field.update(dt)
        self.builder.update(dt)
