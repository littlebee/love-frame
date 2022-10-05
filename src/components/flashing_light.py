from enum import Enum
import time

import pygame
from pygame.locals import MOUSEBUTTONDOWN

from lib.colors import Colors
from lib.renderables import Renderables

from components.circle import Circle

FLASH_DURATION = 1

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
        self.fade_direction = 1;

        self.parent_surface = parent_surface

        # adding our own transparent surface needed to support alpha
        surface_size = (radius*2, radius*2)
        self.surface = pygame.Surface(surface_size, pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        self.circle = Circle(self.surface, radius, (radius, radius), color)
        self.render_rect = self.surface.get_rect()
        self.render_rect.center = center

        self.fade_started_at = time.time()

    def close(self):
        self.has_closed = True
        self.circle.close()

    def render(self, t):
        if self.has_closed:
            return False

        duration = t - self.fade_started_at
        if duration > FLASH_DURATION:
            self.fade_direction *= -1
            self.fade_started_at = t
            duration = 0

        alpha = duration * (255 / FLASH_DURATION)
        if self.fade_direction < 0:
            alpha = 255 - alpha

        self.circle.set_alpha(alpha)
        self.circle.render(t)
        self.parent_surface.blit(self.surface, self.render_rect)

        return True

