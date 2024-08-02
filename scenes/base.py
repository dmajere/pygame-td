from abc import abstractmethod
import pygame
from lib.screen import Screen


class Scene:
    def __init__(self, width: int, height: int, spawn=None) -> None:
        self.screen = Screen(width, height, spawn)

    @abstractmethod
    def process_event(self, event: pygame.event.Event) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        self.screen.draw(surface)

    def update(self, dt: float = 1.0) -> None:
        self.screen.update(dt)
