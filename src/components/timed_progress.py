import pygame
import time

from lib.renderables import Renderables
from lib.colors import Colors

from components.rectangle import Rectangle
from components.text import Text

class TimedProgress(object):
    """
        Renders a full screen progress bar and text.

        This component self destructs after `duration`
    """

    def __init__(
        self,
        surface,
        title="Encoding AV",
        duration=10,
    ):
        self.has_closed = False
        self.surface = surface
        self.duration = duration

        self.progress = 0.0

        title_component = Text(surface, title, 64)
        title_component.center_on_screen(y_offset=-70)

        pw, ph = surface.get_size()
        self.progress_width = pw - 200
        outer_rect_rect = pygame.rect.Rect(100, ph // 2 + 50, self.progress_width, 100)

        progress_rect_rect = pygame.rect.Rect(
            outer_rect_rect.left + 5,
            outer_rect_rect.top + 5,
            0,
            outer_rect_rect.height - 10)

        self.progress_rect = Rectangle(surface, progress_rect_rect, Colors.BUTTON_BLUE)


        self.renderables = Renderables()
        self.renderables.append([
            title_component,
            Rectangle(surface, outer_rect_rect, color=None, border_width=5),
            self.progress_rect,
        ])

        self.started_at = time.time()


    def close(self):
        self.has_closed = True

    def render(self, t):
        if self.has_closed:
            return False

        elapsed = t - self.started_at
        if elapsed > self.duration:
            self.close()

        width = self.progress_width / self.duration * elapsed
        self.progress_rect.set_width(width)

        self.surface.fill(Colors.OFF_WHITE)
        self.renderables.render(t)

        return True
