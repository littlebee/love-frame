from enum import Enum

import pygame
from pygame.locals import MOUSEBUTTONDOWN

from lib.colors import Colors
from lib.renderables import Renderables

from components.fader import Fader
from components.text import Text


class ButtonSize(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2


BUTTON_SHAPES = {
    ButtonSize.SMALL: {
        "radius": 35,
        "font_size": 18,
    },
    ButtonSize.MEDIUM: {
        "radius": 50,
        "font_size": 20,
    },
    ButtonSize.LARGE: {
        "radius": 125,
        "font_size": 48,
    },
}


class Button(object):
    """
        The Button class is a
    """

    def __init__(
        self,
        screen,
        label="",
        size=ButtonSize.MEDIUM,
        pos=(0, 0),
        fg_color=Colors.OFF_WHITE,
        bg_color=Colors.BUTTON_BLUE,

        # events

        # fn called when button was clicked.  called with no parameters; return ignored
        on_click=None
    ):
        self.screen = screen
        self.pos = pos
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.size = size
        self.on_click = on_click

        self.radius = BUTTON_SHAPES[size]["radius"]

        surface_size = (self.radius*2, self.radius*2)

        # adding our own transparent surface makes it easier to center things within
        self.surface = pygame.Surface(surface_size, pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()

        self.textComponent = Text(
            self.surface, label, BUTTON_SHAPES[size]["font_size"])
        self.textComponent.center_on_screen()

    def render(self):
        center = (self.radius, self.radius)
        pygame.draw.circle(self.surface, self.bg_color,
                           center, self.radius, self.radius)
        self.textComponent.render()
        self.screen.blit(self.surface, self.pos)

    def handle_pyg_event(self, event):
        if event.type == MOUSEBUTTONDOWN and self.point_intersects(event.pos):
            hasattr(self, "on_click") and self.on_click()
            return True  # stop propagation

        return False

    def point_intersects(self, pos):
        x, y = pos
        left, top = self.pos
        dia = BUTTON_SHAPES[self.size]["radius"] * 2

        return x > left and x < left + dia and y > top and y < top + dia
