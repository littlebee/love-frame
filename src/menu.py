import pygame
from pygame.locals import MOUSEBUTTONDOWN

import lib.colors as colors
from lib.renderables import Renderables

from components.fader import Fader
from components.text import Text


class Menu(object):

    def __init__(self, screen, on_closing=None):
        self.screen = screen
        self.on_closing = on_closing
        self.has_closed = False

        self.fader = Fader(screen, on_close=self.handle_fader_close)
        self.renderables = Renderables()
        self.renderables.append([
            Text(self.fader.surface, "Press the big green button",
                 56, (20, 30), colors.GREEN),
            Text(self.fader.surface, "...below to leave a loving message",
                 36, (40, 75), colors.ALMOST_BLACK),

            # fader must be last
            self.fader,
        ])

    def close(self):
        self.fader.close()
        self.on_closing and self.on_closing()

    def handle_fader_close(self):
        self.has_closed = True

    def handle_pyg_event(self, event):
        self.renderables.handle_pyg_event(event)

        if event.type == MOUSEBUTTONDOWN:
            self.close()
            return True  # stop propagation

        return False

    def render(self):
        if self.has_closed:
            return False

        # this is full screen window
        self.fader.surface.fill(colors.OFF_WHITE)
        self.renderables.render()

        return True
