from abc import abstractmethod
import pygame
from lib.field import Field


class Scene:
    def __init__(self, width: int, height: int, show_grid: bool = True) -> None:
        self.field = Field(width, height)
        self.show_grid = show_grid

    @abstractmethod
    def process_event(self, event: pygame.event.Event) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        if self.show_grid:
            self.field.draw(surface, (0, 0))
