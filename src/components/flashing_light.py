from enum import Enum

import pygame
from pygame.locals import MOUSEBUTTONDOWN

from lib.colors import Colors
from lib.renderables import Renderables

from components.circle import Circle

FLASH_DURATION_TICKS = 15

class FlashingLight(object):
    """
        Renders a flashing circle.

        Does not self destruct
    """

    def __init__(
        self,
        parent_surface,
        radius,
        center,
        color=(255,255,255),
    ):
        self.has_closed = False
        self.render_ticks = 0;
        self.fade_direction = 1;

        self.parent_surface = parent_surface

        # adding our own transparent surface needed to support alpha
        surface_size = (radius*2, radius*2)
        self.surface = pygame.Surface(surface_size, pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        self.circle = Circle(self.surface, radius, (radius, radius), color)
        self.render_rect = self.surface.get_rect()
        self.render_rect.center = center


    def close(self):
        self.has_closed = True
        self.circle.close()

    def render(self):
        if self.has_closed:
            return False

        self.render_ticks += 1

        if self.render_ticks > FLASH_DURATION_TICKS:
            self.fade_direction *= -1
            self.render_ticks = 0

        alpha = self.render_ticks * 255 / FLASH_DURATION_TICKS
        if self.fade_direction < 0:
            alpha = 255 - alpha

        self.circle.set_alpha(alpha)
        self.circle.render()
        self.parent_surface.blit(self.surface, self.render_rect)

        return True

