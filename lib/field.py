import pygame
from lib.util import Color, Coordinate


class Tile(pygame.sprite.Sprite):
    WIDTH: int = 16
    HEIGHT: int = 16
    COLOR: Color = "white"

    def __init__(self) -> None:
        super(Tile, self).__init__()
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(self.COLOR)
        self.border = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        pygame.draw.rect(self.image, "black", self.border, 1)
        self.rect = self.image.get_frect()


class Field:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cols = self.width // Tile.WIDTH
        self.rows = self.height // Tile.HEIGHT

        self.surface = pygame.Surface((self.cols * Tile.WIDTH, self.rows * Tile.HEIGHT))
        self._field = []
        self._tile_group = pygame.sprite.Group()

        for c in range(self.cols):
            self._field.append([])
            for r in range(self.rows):
                tile = Tile()
                tile.rect.topleft = (c * Tile.WIDTH, r * Tile.HEIGHT)
                self._field[c].append(tile)
                self._tile_group.add(tile)

    def draw(self, surface: pygame.Surface, position: Coordinate) -> None:
        self._tile_group.draw(self.surface)
        surface.blit(self.surface, position)
        self._tile_group.update()
