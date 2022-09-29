from enum import Enum
import pygame

from lib.colors import Colors
from lib.renderables import Renderables

from components.fader import Fader
from components.button import Button


class FadeButton(object):
    """
        The FadeButton class is a button that fades in on creation and out
        when the button is clicked
    """

    def __init__(
        self,
        screen,
        label="",
        size=ButtonSize.MEDIUM,
        pos=(0, 0),
        fg_color=Colors.OFF_WHITE,
        bg_color=Colors.BUTTON_BLUE,
        fade_in_duration=0,
        fade_out_duration=0,

        # events

        # fn called when button was clicked.  called with no parameters; return ignored
        on_close=None
    ):
        self.screen = screen

        self.fader = Fader(screen,
                           pos=pos,
                           fade_in_duration=fade_in_duration,
                           fade_out_duration=fade_out_duration,
                           )
        self.renderables = Renderables()
        self.renderables.append([
            Text(self.fader.surface, label),

            self.fader,  # fader last
        ])

    def render(self):
        self.screen.blit(self.text, self.textRect)

    def handle_pyg_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.on_closing and self.on_closing()
            self.fader.close()

            return True  # stop propagation

        return False
