from enum import Enum
import time

import pygame
from pygame.locals import MOUSEBUTTONDOWN

from lib.colors import Colors
from lib.renderables import Renderables

from components.rectangle import Rectangle

FLASH_DURATION = .5
DIMMING_DURATION = .5

class FlashingBar(object):
    """
        Renders a flashing bar like the four in a battery monitor.

        Does not self destruct
    """

    def __init__(
        self,
        parent_surface,
        rect,

        color=Colors.GREEN,
        flash_color=Colors.GREEN,
        dim_color=Colors.DARK_GREY,

        # duration in seconds
        flash_after = 1,
        dim_after = 5
    ):
        self.parent_surface = parent_surface
        self.color = color
        self.flash_color = flash_color
        self.dim_color = dim_color
        self.flash_after = flash_after
        self.dim_after = dim_after


        self.has_closed = False
        self.fade_direction = 1;
        self.dimming_started_at = None
        self.flash_started_at = None

        x, y, w, h = rect
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        self.render_rect = self.surface.get_rect()
        self.render_rect.topleft = (x, y)

        self.rectangle = Rectangle(self.surface, (0, 0, w, h), color)

        self.started_at = time.time()

    def close(self):
        self.has_closed = True
        self.rectangle.close()

    def render(self, t):
        if self.has_closed:
            return False

        duration = t - self.started_at

        if duration > self.dim_after + DIMMING_DURATION:
            self.rectangle.set_color(self.dim_color)
        elif duration > self.dim_after:
            if self.dimming_started_at == None:
                self.dimming_started_at = t

            dimming_duration = t - self.dimming_started_at
            alpha = int(255 - (dimming_duration * 255 / DIMMING_DURATION))
            self.rectangle.set_color(self.flash_color, alpha)
        elif duration > self.flash_after:
            if self.flash_started_at == None:
                self.flash_started_at = t
                self.fade_started_at = t

            fade_duration = t - self.fade_started_at
            if fade_duration > FLASH_DURATION:
                self.fade_direction *= -1
                self.fade_started_at = t
                fade_duration = 0

            alpha = int(fade_duration * (255 / FLASH_DURATION))
            if self.fade_direction < 0:
                alpha = 255 - alpha

            self.rectangle.set_color(self.flash_color, alpha)

        self.rectangle.render(t)
        self.parent_surface.blit(self.surface, self.render_rect)

        return True

