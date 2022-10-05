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
        font_size,
        pos,
        stop_after=0, # max in seconds to go up to
        fg_color=Colors.GREY,
        bg_color=None,
    ):
        self.surface = surface
        self.stop_after = stop_after

        self.has_closed = False
        self.fade_direction = 1;

        self.text = MutableText(self.surface, "00:00:00.0", font_size, pos, fg_color, bg_color)

        self.started_at = time.time()

    def close(self):
        self.has_closed = True
        self.circle.close()

    def render(self, t):
        if self.has_closed:
            return False

        duration = t - self.started_at
        if duration > self.stop_after:
            duration = self.stop_after

        hour, minute, second = self.parse_seconds(duration)
        self.text.set_value(f"{hour:02d}:{minute:02d}:{second:02.1f}")
        self.text.render(t)

        return True


    def parse_seconds(self, seconds):
        hour = int(seconds / 3600)
        remaining = seconds - hour * 3600
        minute = int(remaining / 60)
        second = remaining - minute * 60

        return [hour, minute, second]