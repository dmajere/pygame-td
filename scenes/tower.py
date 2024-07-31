import pygame
from lib.tower import Tower
from scenes.base import Scene
from lib.util import Coordinate
from lib.field import Tile


class Builder:
    _object: pygame.sprite.Sprite = None
    _build_group = pygame.sprite.GroupSingle()

    def __init__(self, field) -> None:
        self.field = field

    def building(self) -> bool:
        return self._object is not None

    def start(self, clz, *args, **kwargs) -> None:
        self._object = clz(*args, **kwargs)
        self._build_group.add(self._object)

    def end(self) -> None:
        pos = pygame.mouse.get_pos()
        if self.field.build(pos, self._object):
            self._clean()

    def _clean(self):
        self._build_group.remove(self._object)
        self._object = None

    def cancel(self):
        self._clean()

    def draw(self, surface: pygame.Surface):
        if self._object:
            self._object.rect.topleft = self.field.get_tile_topleft(
                pygame.mouse.get_pos()
            )
            self._build_group.draw(surface)


class TowerScene(Scene):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.builder = Builder(self.field)

        self.bullets = pygame.sprite.Group()

        self.building = False

    def build_tower(self, pos: Coordinate):
        tower = Tower(self.bullets)
        if self.field.build(pos, tower):
            self.building = False

    def process_event(self, event: pygame.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.builder.building():
                self.builder.end()
            else:
                pos = pygame.mouse.get_pos()
                [tower.shoot(pos) for tower in self.field.tower_sprites.sprites()]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                self.builder.start(Tower, self.bullets)
            if event.key == pygame.K_ESCAPE:
                self.builder.cancel()

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        self.bullets.draw(surface)
        self.builder.draw(surface)

        self.bullets.update()
