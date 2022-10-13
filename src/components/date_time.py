from datetime import datetime
import pygame

from lib.colors import Colors

from components.text import Text

DEFAULT_DT_FORMAT = "%b. %-d, %Y %-I:%-M %p"

class DateTime(object):
    """
        Renders an string representation of the pass epoch (time.time())

        This component does not self destruct
    """

    def __init__(
        self,
        surface,
        pos,
        epoch_seconds,
        fmt=DEFAULT_DT_FORMAT,
        font_size="36",
        color=Colors.GREY
    ):
        self.has_closed = False
        self.surface = surface

        dt = datetime.fromtimestamp(epoch_seconds)
        str_dt = dt.strftime(fmt)

        self.text = Text(surface, str_dt, font_size, pos, color)


    def close(self):
        self.has_closed = True


    def render(self, t):
        if self.has_closed:
            return False

        self.text.render(t)

        return True
