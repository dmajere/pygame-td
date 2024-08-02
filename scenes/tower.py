import pygame
from lib.tower import Tower
from scenes.base import Scene
from lib.util import Coordinate
from lib.builder import Builder


class TowerScene(Scene):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

    def process_event(self, event: pygame.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.screen.builder.building:
                pos = pygame.mouse.get_pos()
                [
                    tower.shoot(pos)
                    for tower in self.screen.field.tower_sprites.sprites()
                ]

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
