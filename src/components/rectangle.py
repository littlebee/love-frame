import pygame
from pygame.locals import MOUSEBUTTONDOWN

from lib.colors import Colors, normalize_alpha

class Rectangle(object):
    """
        Primitive component that just renders a circle at the coords provide.

        Does not self destruct
    """

    def __init__(
        self,
        surface,
        # (left, top, w, h)
        rect,
        # set color=None for outline only
        color=Colors.GREY,
        alpha=255,
        border_width=0,
        border_radius=0,
        border_color=0,
    ):
        self.surface = surface
        self.set_color(color, alpha)
        self.rect = pygame.Rect(rect)
        self.border_width = border_width
        self.border_radius = border_radius
        self.border_color = border_color


        self.has_closed = False

    def set_color(self, color, alpha=255):
        self.color = pygame.Color(color) if color else None
        if self.color:
            self.color.a = normalize_alpha(alpha)

    def set_alpha(self, alpha):
        if self.color:
            self.color.a = normalize_alpha(alpha)

    def set_width(self, width):
        self.rect.width = width

    def close(self):
        self.has_closed = True

    def render(self, t):
        if self.has_closed:
            return False

        if self.color != None:
            # border_width 0 tells draw.rect to fill
            pygame.draw.rect(
                self.surface,
                self.color,
                self.rect,
                0,
                self.border_radius,
            )

        if self.border_width > 0:
            # ...now draw the border in border color
            pygame.draw.rect(
                self.surface,
                self.border_color,
                self.rect,
                self.border_width,
                self.border_radius,
            )

        return True

