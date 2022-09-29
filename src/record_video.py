import pygame
from pygame.locals import MOUSEBUTTONDOWN

from lib.colors import Colors
from lib.renderables import Renderables

from components.fader import Fader
from components.text import Text
from components.button import Button, ButtonSize
from components.live_video import LiveVideo


class RecordVideo(object):

    def __init__(self, screen, on_closing=None):
        self.screen = screen
        self.on_closing = on_closing
        self.has_closed = False

        self.fader = Fader(screen,
                           fade_out_duration=0,
                           on_close=self.handle_fader_close)
        self.renderables = Renderables()
        self.renderables.append([
            Text(self.fader.surface, "Great!  Let's record a 15 second video..",
                 56, (50, 60), Colors.OFF_WHITE),
            Text(self.fader.surface, "...and don't forget to speak up.",
                 36, (90, 105), Colors.ALMOST_BLACK),

            self.fader,

            # render live video outside of fader
            LiveVideo(screen),
        ])

    def close(self, action):
        self.fader.close()
        hasattr(self, "on_closing") and self.on_closing(action)

    def handle_record_click(self):
        self.close("record")

    def handle_fader_close(self):
        self.has_closed = True

    def handle_pyg_event(self, event):
        # return self.renderables.handle_pyg_event(event)

        if event.type == MOUSEBUTTONDOWN:
            self.on_closing and self.on_closing()
            self.fader.close()

            return True  # stop propagation

        return False

    def render(self):
        if self.has_closed:
            return False

        # this is full screen window
        self.fader.surface.fill(Colors.OFF_WHITE)
        self.renderables.render()

        return True
