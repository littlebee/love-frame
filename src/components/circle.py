from enum import Enum

import pygame
from pygame.locals import MOUSEBUTTONDOWN

from lib.colors import Colors
from lib.renderables import Renderables

class Circle(object):
    """
        Primitive component that just renders a circle at the coords provide.
    """

    def __init__(
        self,
        surface,
        radius,
        center,
        color=(255,255,255),
        alpha=255
    ):
        self.surface = surface
        self.radius = radius
        self.center = center
        self.color = pygame.Color(color)
        self.color.a = alpha

        self.has_closed = False

    def set_color(self, color):
        self.color = pygame.Color(color)
        self.color.a = self.alpha

    def set_alpha(self, alpha):
        self.color.a = int(alpha)

    def close(self):
        self.has_closed = True

    def render(self):
        if self.has_closed:
            return False

        pygame.draw.circle(self.surface, self.color,
                           self.center, self.radius)

        return True

