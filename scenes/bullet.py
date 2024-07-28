import pygame
from lib.util import Coordinate
from lib.bullet import Bullet
from lib.line import Line
from lib.field import Field
from scenes.base import Scene

BULLET_SIZE = (10, 10)
BULLET_MASS = 1
FRICTION = 1


class BulletScene(Scene):
    bullet = None

    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        self.field = Field(width, height)

        self.bullets = pygame.sprite.Group()

        def _start_cb(pos: Coordinate) -> None:
            self.bullet = Bullet(BULLET_SIZE, pos, BULLET_MASS)
            self.bullets.add(self.bullet)

        def _end_cb(magnitude, unit):
            self.bullet.shoot(unit, magnitude, FRICTION)

        self.line = Line(
            start_cb=_start_cb,
            end_cb=_end_cb,
        )

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.line.start_line(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            self.line.end_line(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEMOTION:
            self.line.update_line(pygame.mouse.get_pos())

    def draw(self, surface: pygame.Surface) -> None:
        self.field.draw(surface, (0, 0))
        self.line.draw(surface)

        self.bullets.draw(surface)
        self.bullets.update()
