import pygame
from lib.util import Color, Coordinate
from lib.tower import Tower


class Tile(pygame.sprite.Sprite):
    WIDTH: int = 16
    HEIGHT: int = 16
    COLOR: Color = "white"

    def __init__(self) -> None:
        super(Tile, self).__init__()
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(self.COLOR)
        self.border = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        pygame.draw.rect(self.image, "gray", self.border, 1)
        self.rect = self.image.get_frect()

        self.used = False


class Field:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cols = self.width // Tile.WIDTH
        self.rows = self.height // Tile.HEIGHT

        self.surface = pygame.Surface((self.cols * Tile.WIDTH, self.rows * Tile.HEIGHT))
        self.tiles = []

        self.tile_sprites = pygame.sprite.Group()
        self.tower_sprites = pygame.sprite.Group()

        for c in range(self.cols):
            self.tiles.append([])
            for r in range(self.rows):
                tile = Tile()
                tile.rect.topleft = (c * Tile.WIDTH, r * Tile.HEIGHT)
                self.tiles[c].append(tile)
                self.tile_sprites.add(tile)

    def build(self, pos: Coordinate, tower: Tower) -> bool:
        tile = (pos[0] // Tile.WIDTH, pos[1] // Tile.HEIGHT)
        if self.tiles[tile[0]][tile[1]].used:
            return False
        self.tiles[tile[0]][tile[1]].used = True
        tower.rect.topleft = (tile[0] * Tile.WIDTH, tile[1] * Tile.HEIGHT)
        tower.build()

        self.tower_sprites.add(tower)
        return True

    def get_tile_topleft(self, pos: Coordinate) -> Coordinate:
        tile = (pos[0] // Tile.WIDTH, pos[1] // Tile.HEIGHT)
        return (tile[0] * Tile.WIDTH, tile[1] * Tile.HEIGHT)

    def draw(self, surface: pygame.Surface, position: Coordinate) -> None:
        self.tile_sprites.draw(self.surface)
        self.tower_sprites.draw(self.surface)

        surface.blit(self.surface, position)
