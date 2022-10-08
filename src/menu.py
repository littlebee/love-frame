import pygame
from pygame.locals import MOUSEBUTTONDOWN
import time

from lib.colors import Colors
from lib.renderables import Renderables

from components.text import Text
from components.button import Button, ButtonSize


class MenuActions(object):
    GALLERY = 0
    RECORD_VIDEO = 1

# menu closes to gallery after 30 seconds without selecting
# anything else
AUTO_CLOSE_AFTER = 30


class Menu(object):

    def __init__(self, surface, on_closing=None):
        self.surface = surface
        self.on_closing = on_closing

        self.has_closed = False
        self.started_at = time.time()

        self.renderables = Renderables()
        self.renderables.append([
            Text(self.surface, "Press the big green button",
                 56, (50, 60), Colors.GREEN
            ),
            Text(self.surface, "...below to leave a loving message",
                 36, (90, 105), Colors.ALMOST_BLACK
            ),
            Button(self.surface, "Record",
                   pos=(700, 300),
                   size=ButtonSize.LARGE,
                   bg_color=Colors.GREEN,
                   fg_color=Colors.ALMOST_BLACK,
                   on_click=self.handle_record_click
            ),
            Button(self.surface, "Gallery",
                   pos=(820, 100),
                   size=ButtonSize.SMALL,
                   bg_color=Colors.BUTTON_BLUE,
                   fg_color=Colors.GREY,
                   on_click=self.handle_gallery_click
            ),
        ])

    def close(self, action):
        self.has_closed = True
        self.on_closing(action)

    def handle_record_click(self):
        self.close(MenuActions.RECORD_VIDEO)

    def handle_gallery_click(self):
        self.close(MenuActions.GALLERY)

    def handle_pyg_event(self, event):
        return self.renderables.handle_pyg_event(event)

    def render(self, t):
        if self.has_closed:
            return False

        if t - self.started_at > AUTO_CLOSE_AFTER:
            self.close(MenuActions.GALLERY)

        # this is full screen window
        self.surface.fill(Colors.OFF_WHITE)
        self.renderables.render(t)

        return True
