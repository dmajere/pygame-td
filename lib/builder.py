import pygame


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
