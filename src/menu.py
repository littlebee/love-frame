import pygame
from pygame.locals import MOUSEBUTTONDOWN

from lib.colors import Colors
from lib.renderables import Renderables

from components.fader import Fader
from components.text import Text
from components.button import Button, ButtonSize


class Menu(object):

    def __init__(self, screen, on_closing=None):
        self.screen = screen
        self.on_closing = on_closing
        self.has_closed = False

        self.fader = Fader(screen,
                           fade_out_duration=0,
                           on_close=self.handle_fader_close)
        self.renderables = Renderables()
        self.renderables.append([
            Text(self.fader.surface, "Press the big green button",
                 56, (20, 30), Colors.GREEN),
            Text(self.fader.surface, "...below to leave a loving message",
                 36, (40, 75), Colors.ALMOST_BLACK),
            Button(self.fader.surface, "Record",
                   pos=(700, 300),
                   size=ButtonSize.LARGE,
                   bg_color=Colors.GREEN,
                   fg_color=Colors.ALMOST_BLACK,
                   on_click=self.handle_record_click
                   ),
            # fader must be last
            self.fader,
        ])

    def close(self, action):
        self.fader.close()
        hasattr(self, "on_closing") and self.on_closing(action)

    def handle_record_click(self):
        self.close("record")

    def handle_fader_close(self):
        self.has_closed = True

    def handle_pyg_event(self, event):
        return self.renderables.handle_pyg_event(event)

    def render(self):
        if self.has_closed:
            return False

        # this is full screen window
        self.fader.surface.fill(Colors.OFF_WHITE)
        self.renderables.render()

        return True
