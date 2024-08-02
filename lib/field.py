from queue import Queue
import pygame
from typing import Tuple, Optional, List
from lib.tiles import Tile, Spawn, Goal
from lib.util import Coordinate
from lib.tower import Tower
from lib.pathfind import PathFinder


class Field:
    def __init__(
        self,
        width: int,
        height: int,
        spawn: Optional[Tuple[int, int]] = None,
        goal: Optional[Tuple[int, int]] = None,
    ) -> None:
        self.width = width
        self.height = height
        self.cols = self.width // Tile.WIDTH
        self.rows = self.height // Tile.HEIGHT

        self.surface = pygame.Surface((self.cols * Tile.WIDTH, self.rows * Tile.HEIGHT))
        self.tiles = []

        self.tile_sprites = pygame.sprite.Group()
        self.tower_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.spawn_sprites = pygame.sprite.Group()
        self.monster_sprites = pygame.sprite.Group()

        spawn = spawn or (0, 0)
        goal = goal or (self.cols - 1, self.rows - 1)

        for c in range(self.cols):
            self.tiles.append([])
            for r in range(self.rows):
                if (c, r) == spawn:
                    tile = Spawn(self.monster_sprites)
                    self.spawn_sprites.add(tile)
                elif (c, r) == goal:
                    tile = Goal()
                else:
                    tile = Tile()
                tile.rect.topleft = (c * Tile.WIDTH, r * Tile.HEIGHT)
                self.tiles[c].append(tile)
                self.tile_sprites.add(tile)

        self.pathfinder = PathFinder(self.tiles, spawn, goal)

    def build(self, pos: Coordinate, tower: Tower) -> bool:
        tile = self.get_tile(pos)
        if not tile:
            return False
        if self.tiles[tile[0]][tile[1]].used:
            return False
        self.tiles[tile[0]][tile[1]].used = True
        tower.rect.topleft = (tile[0] * Tile.WIDTH, tile[1] * Tile.HEIGHT)
        tower.build()

        self.tower_sprites.add(tower)
        return True

    def get_next_path(self):
        self.pathfinder.set_tile_weights()
        return self.pathfinder.get_path()

    def get_tile(self, pos: Coordinate) -> Optional[Tuple[int, int]]:
        x = pos[0] // Tile.WIDTH
        y = pos[1] // Tile.HEIGHT
        if all((x >= 0, x < len(self.tiles), y >= 0, y < len(self.tiles[0]))):
            return (x, y)
        else:
            return None

    def get_tile_topleft(self, pos: Coordinate) -> Optional[Coordinate]:
        tile = self.get_tile(pos)
        if not tile:
            return None
        return (tile[0] * Tile.WIDTH, tile[1] * Tile.HEIGHT)

    def set_monster_spawn(self, monsters, path) -> None:
        for sprite in self.spawn_sprites.sprites():
            sprite.set(monsters, path)

    def draw(self, surface: pygame.Surface, position: Coordinate) -> None:
        self.tile_sprites.draw(self.surface)
        self.tower_sprites.draw(self.surface)
        self.monster_sprites.draw(self.surface)
        self.bullet_sprites.draw(self.surface)

        surface.blit(self.surface, position)

    def update(self, dt: float = 1.0) -> None:
        self.tile_sprites.update(dt)
        self.spawn_sprites.update(dt)

        self.monster_sprites.update(dt)
        self.bullet_sprites.update(dt)
