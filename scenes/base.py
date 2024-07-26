from abc import abstractmethod
import pygame


class Scene:
    @abstractmethod
    def process_event(self, event: pygame.event.Event) -> None:
        pass
