from enum import Enum
import time

import pygame
from pygame.locals import MOUSEBUTTONDOWN

from lib.colors import Colors

from components.text import Text
from components.mutable_text import MutableText

FLASH_DURATION = 1

class Timer(object):
    """
        Renders a timer like 0:00:00 that increments over time.

        Component does not self destruct.
    """

    def __init__(
        self,
        surface,
        pos,
        stop_after=0, # max in seconds to go up to
        font_size=36,
        fg_color=Colors.GREY,
        bg_color=None,
        show_hours=True,
        show_minutes=True,
        # show timer that counts down from stop_after
        reverse=False,
        # call backs
        on_stop=None
    ):
        self.surface = surface
        self.stop_after = stop_after
        self.show_hours = show_hours
        self.show_minutes = show_minutes
        self.reverse = reverse
        self.on_stop = on_stop

        self.has_closed = False
        self.fade_direction = 1;

        self.text = MutableText(self.surface, "00:00:00.0", font_size, pos, fg_color, bg_color)

        self.started_at = time.time()

    def close(self):
        self.has_closed = True
        self.text.close()

        if callable(self.on_stop):
            self.on_stop();

    def render(self, t):
        if self.has_closed:
            return False

        duration = t - self.started_at
        if duration > self.stop_after:
            self.close()

        self.text.set_value(self.get_display_value(duration))
        self.text.render(t)

        return True


    def get_display_value(self, duration):
        hour, minute, second = self.parse_seconds(duration)

        textValue = ""
        if self.show_hours:
            textValue += f"{hour:02d}:"
        if self.show_minutes:
            textValue += f"{minute:02d}:"
        textValue += f"{second:02.1f}"

        return textValue


    def parse_seconds(self, duration):
        seconds = self.stop_after - duration if self.reverse else duration
        hour = int(seconds / 3600)
        remaining = seconds - hour * 3600
        minute = int(remaining / 60)
        second = remaining - minute * 60

        return [hour, minute, second]