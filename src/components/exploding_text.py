import pygame
import time

from lib.colors import Colors
import lib.constants as const
from components.text import Text

STARTING_FONT_SIZE = 50
SCALING_FACTOR = 2.5

class ExplodingText(object):

    def __init__(
        self,
        surface,
        # Text args
        value,
        font_size=32,
        color=Colors.RED,

        # delay before exploding in seconds
        delay=0,
        # duration of explosion animation in seconds
        duration = 1,
    ):
        self.surface = surface
        self.value = value
        self.color = color
        self.delay = delay
        self.duration = duration

        self.started_at = time.time()

        self.is_closing = False
        self.has_closed = False

        self.started_at = time.time()

        # TODO : I couldn't find a preinstalled font that mac and rpi had in common :/
        #   Just let it choose one for now
        self.font = pygame.font.Font(None, font_size)

    def close(self):
        self.is_closing = True

    def render(self, t):
        if self.has_closed:
            return False

        elapsed = t - self.started_at

        if  elapsed > self.delay + self.duration:
            self.has_closed = True
            return False

        if elapsed > self.delay:
            text, text_rect = self._scale_text(elapsed)
        else:
            text = self.font.render(self.value, True, self.color, None)
            text_rect = text.get_rect()

        surface_w, surface_h = self.surface.get_size()
        # centered of the surface passed on construct
        text_rect.center = (surface_w // 2, surface_h // 2)

        self.surface.blit(text, text_rect)
        return True

    def _scale_text(self, elapsed):
        fade_elapsed = elapsed - self.delay

        scale = 1 + (SCALING_FACTOR * fade_elapsed);
        alpha = int(255 - (self.duration / fade_elapsed))

        # Alpha fade using .set_alpha() like below or adjusting it in the
        # color doesn't work on Raspian Buster + pygame 2.1.2 (SDL 2.0.9, Python 3.7.3)
        #
        # This is a weak approx because the black letters still show :/
        r, g, b = self.color
        color = (
            r - max(0, min(255, int(r - (r / self.duration * (self.duration - elapsed))))),
            g - max(0, min(255, int(g - (g / self.duration * (self.duration - elapsed))))),
            b - max(0, min(255, int(b - (b / self.duration * (self.duration - elapsed))))),
        )

        # print(f"scaling text {scale} {alpha} {color} {self.color}")

        text = self.font.render(self.value, True, color, None)
        text.set_alpha(alpha)
        text_rect = text.get_rect()

        new_size = (
            int(text_rect.width * scale),
            int(text_rect.height * scale),
        )

        scaled = pygame.transform.scale(text, new_size)
        scaled_rect = scaled.get_rect()  # this is scaled rect

        return scaled, scaled_rect