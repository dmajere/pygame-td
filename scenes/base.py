from abc import abstractmethod
import pygame
from lib.field import Field


class Scene:
    def __init__(self, width: int, height: int) -> None:
        self.field = Field(width, height)

    @abstractmethod
    def process_event(self, event: pygame.event.Event) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        self.field.draw(surface, (0, 0))
