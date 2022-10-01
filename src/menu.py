import pygame
from pygame.locals import MOUSEBUTTONDOWN

from lib.colors import Colors
from lib.renderables import Renderables

from components.text import Text
from components.button import Button, ButtonSize


class MenuActions(object):
    GALLERY = 0
    RECORD_VIDEO = 1


class Menu(object):

    def __init__(self, screen, on_closing=None):
        self.on_closing = on_closing
        self.has_closed = False

        self.surface = screen

        self.renderables = Renderables()
        self.renderables.append([
            Text(self.surface, "Press the big green button",
                 56, (50, 60), Colors.GREEN),
            Text(self.surface, "...below to leave a loving message",
                 36, (90, 105), Colors.ALMOST_BLACK),
            Button(self.surface, "Record",
                   pos=(700, 300),
                   size=ButtonSize.LARGE,
                   bg_color=Colors.GREEN,
                   fg_color=Colors.ALMOST_BLACK,
                   on_click=self.handle_record_click
                   ),
        ])

    def close(self, action):
        self.has_closed = True

        hasattr(self, "on_closing") and self.on_closing(action)

    def handle_record_click(self):
        self.close(MenuActions.RECORD_VIDEO)

    def handle_pyg_event(self, event):
        return self.renderables.handle_pyg_event(event)

    def render(self):
        if self.has_closed:
            return False

        self.surface.fill(Colors.OFF_WHITE)
        self.renderables.render()

        return True
