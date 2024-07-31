import pygame
from lib.tower import Tower
from scenes.base import Scene


class TowerScene(Scene):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.bullets = pygame.sprite.Group()
        self.tower = Tower(self.bullets)
        self.tower.rect.center = (width // 2, height // 2)
        self.towers = pygame.sprite.GroupSingle(self.tower)

    def process_event(self, event: pygame.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            self.tower.shoot(pos)

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        self.bullets.draw(surface)
        self.towers.draw(surface)

        self.bullets.update()
