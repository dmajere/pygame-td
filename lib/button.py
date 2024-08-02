import pygame
from typing import Callable
from lib.util import Color, Coordinate, Text


class Button:
    def __init__(
        self,
        color: Color,
        on_click: Callable = None,
        on_hover: Callable = None,
        width: int = None,
        height: int = None,
        text: Text = None,
        text_margin: int = 0,
        border_width: int = None,
        border_radius: int = None,
        border_color: Color = (0, 0, 0),
        hover_color: Color = None,
        hover_border_color: Color = None,
        hover_border_width: int = None,
    ) -> None:
        self.color = color

        self.border_width = (
            border_width if border_width is not None and border_width >= 0 else 0
        )
        self.border_radius = (
            border_radius if border_radius is not None and border_radius > 0 else -1
        )
        self.border_color = border_color

        self.hover_color = hover_color
        self.hover_border_color = hover_border_color
        self.hover_border_width = (
            hover_border_width
            if hover_border_width is not None and hover_border_width >= 0
            else 0
        )

        self.active = True
        self.active_color = self.color
        self.active_border_color = self.border_color
        self.active_border_width = self.border_width

        self.width = width
        self.height = height
        self.text_margin = text_margin
        self.text = text

        self.on_click = on_click
        self.on_hover = on_hover

        self.rect = self._get_rect()

    def _get_rect(self) -> pygame.rect.Rect:
        if self.width and self.height:
            width, height = self.width, self.height
        elif self.text:
            width, height = (
                self.text.rect.width + self.text_margin,
                self.text.rect.height + self.text_margin,
            )
        else:
            raise Exception(
                "Either width and height or margin and text must be specified"
            )
        if self.active_border_width:
            width, height = (
                width + self.active_border_width,
                height + self.active_border_width,
            )
        return pygame.rect.Rect(0, 0, width, height)

    def draw(self, surface: pygame.Surface, c: Coordinate) -> None:
        self.rect.center = c
        self.text.rect.center = c

        pygame.draw.rect(
            surface, self.active_color, self.rect, border_radius=self.border_radius
        )
        if self.active_border_width > 0:
            pygame.draw.rect(
                surface,
                self.active_border_color,
                self.rect,
                width=self.active_border_width,
                border_radius=self.border_radius,
            )
        pygame.draw.rect(surface, self.active_color, self.text.rect, -1)
        surface.blit(self.text.image, self.text.rect)

    def update(self, _: int = 1) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.hover_color:
                self.active_color = self.hover_color
            if self.hover_border_color:
                self.active_border_color = self.hover_border_color
            if self.hover_border_width:
                self.active_border_width = self.hover_border_width
            if self.on_hover:
                self.on_hover()

            left, _, _ = pygame.mouse.get_pressed()
            if left and self.on_click:
                self.on_click()
        else:
            self.active_color = self.color
            self.active_border_color = self.border_color
            self.active_border_width = self.border_width
