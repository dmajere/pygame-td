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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                self.screen.builder.start(Tower, self.screen.field.bullet_sprites)

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
