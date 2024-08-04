import sys
import pygame
from typing import Tuple, Optional
from lib.tiles import Tile, Spawn, Goal
from lib.util import Coordinate
from lib.tower import Tower
from lib.pathfind import PathFinder
from lib.builder import Builder


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

        self.builder = Builder(self, 100)
        self.tile_sprites = pygame.sprite.Group()
        self.tower_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.spawn_sprites = pygame.sprite.Group()
        self.monster_sprites = pygame.sprite.Group()

        for c in range(self.cols):
            self.tiles.append([])
            for r in range(self.rows):
                self.tiles[c].append(None)

        self.goal_pos = goal or (self.cols - 1, self.rows - 1)
        self.goal_tile = Goal()
        self.tiles[self.goal_pos[0]][self.goal_pos[1]] = self.goal_tile

        self.spawn_pos = spawn or (0, 0)

        def damage(monster):
            self.goal_tile.health -= monster.DAMAGE

        def death(monster):
            self.builder.money += monster.REWARD

        self.spawn_tile = Spawn(self.monster_sprites, damage, death)
        self.tiles[self.spawn_pos[0]][self.spawn_pos[1]] = self.spawn_tile
        self.spawn_sprites.add(self.spawn_tile)

        for c in range(self.cols):
            for r in range(self.rows):
                if self.tiles[c][r] == None:
                    self.tiles[c][r] = Tile()
                self.tiles[c][r].rect.topleft = (c * Tile.WIDTH, r * Tile.HEIGHT)
                self.tile_sprites.add(self.tiles[c][r])

        self.pathfinder = PathFinder(self.tiles)

    def build(self, pos: Coordinate, tower: Tower) -> bool:
        tile_pos = self.get_tile(pos)
        if not tile_pos:
            return False
        tile = self.tiles[tile_pos[0]][tile_pos[1]]
        if tile.used:
            return False
        tile.weight = sys.maxsize
        if not self.get_next_path():
            tile.weight = None
            return False
        tile.used = True
        tower.build((tile_pos[0] * Tile.WIDTH, tile_pos[1] * Tile.HEIGHT))

        self.tower_sprites.add(tower)
        return True

    def get_next_path(self):
        return self.pathfinder.get_path(self.spawn_pos, self.goal_pos)

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

    def draw(self, surface: pygame.Surface, position: Coordinate) -> None:
        self.tile_sprites.draw(self.surface)
        self.tower_sprites.draw(self.surface)
        self.monster_sprites.draw(self.surface)
        self.bullet_sprites.draw(self.surface)
        self.builder.draw(self.surface)

        surface.blit(self.surface, position)

    def update(self, dt: float = 1.0) -> None:
        self.builder.update(dt)
        self.tile_sprites.update(dt)
        self.spawn_sprites.update(dt)
        self.monster_sprites.update(dt)
        self.bullet_sprites.update(self.monster_sprites, dt)
        self.tower_sprites.update(self.monster_sprites, dt)
