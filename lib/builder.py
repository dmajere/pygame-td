import pygame
from lib.util import Coordinate


class Builder:
    _object: pygame.sprite.Sprite = None
    _build_group = pygame.sprite.GroupSingle()

    def __init__(self, field, money: int) -> None:
        self.field = field
        self.money = money

    @property
    def building(self) -> bool:
        return self._object is not None

    def start(self, clz, *args, **kwargs) -> None:
        if self.money - clz.COST < 0:
            return
        self.money -= clz.COST
        self._object = clz(*args, **kwargs)
        self._build_group.add(self._object)

    def end(self, pos: Coordinate) -> None:
        if self.field.build(pos, self._object):
            self._clean()

    def _clean(self):
        self._build_group.remove(self._object)
        self._object = None

    def cancel(self):
        self._clean()

    def draw(self, surface: pygame.Surface):
        self._build_group.draw(surface)

    def update(self, _: float = 1.0) -> None:
        left, _, _ = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if self.building:
            if left:
                self.end(mouse_pos)
            elif keys[pygame.K_ESCAPE]:
                self.cancel()
            else:
                if topleft := self.field.get_tile_topleft(mouse_pos):
                    self._object.rect.topleft = topleft
