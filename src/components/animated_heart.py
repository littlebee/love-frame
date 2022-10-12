import pygame
import time

from lib.colors import Colors
from lib.sequenced_renderables import SequencedRenderables
from lib.src_files import src_file

from components.rectangle import Rectangle
from components.image import Image

FADE_IN_DURATION = 1
START_BLACKHEART_AT = 2

RED_HEART_FILE = src_file('red_heart.png')
BLACK_HEART_FILE = src_file('black_heart.png')


class AnimatedHeart(object):

    def __init__(self, parent_surface, on_close=None):
        self.parent_surface = parent_surface
        self.on_close = on_close

        self.started_at = time.time()
        self.has_closed = False

        self.w, self.h = parent_surface.get_size()
        self.surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        surface_rect = (0, 0, self.w, self.h)

        self.backdrop = Rectangle(self.surface, surface_rect,
            color=Colors.ALMOST_BLACK,
            alpha=5,
        )

        init_size = (200, 200)
        self.red_heart = Image(self.surface, (0, 0), RED_HEART_FILE, init_size)
        self.red_heart.center()

        self.red_heart = Image(self.surface, (0, 0), BLACK_HEART_FILE, init_size)
        self.black_heart.center()

        self.renderables = SequencedRenderables()
        self.renderables.append([
            # our backdrop which fades in
            [0, 0, lambda : self.backdrop],
            [FADE_IN_DURATION, 0, lambda: self.red_heart],
            [START_BLACKHEART_AT, 0, lambda: self.black_heart],
        ])

    def close(self):
        if not self.has_closed:
            self.has_closed = True
            callable(self.on_close) and self.on_close()
            self.renderables.close()



    def render(self, t):
        if self.has_closed:
            return False

        duration = t - self.started_at
        if duration < FADE_IN_DURATION:
            self.backdrop.set_alpha(255 / FADE_IN_DURATION * duration)
        else:
            self.backdrop.set_alpha(255)

        if( duration > START_BLACKHEART_AT ):
            heart_duration = duration - START_BLACKHEART_AT

            self.red_heart.scale(1 + heart_duration * 0.2)
            self.red_heart.center()

            self.black_heart.scale(1 + heart_duration * 0.1)
            self.black_heart.center()

            if( self.black_heart.rect.w > self.w + 400 ):
                self.close()


        self.renderables.render(t)
        self.parent_surface.blit(self.surface, (0, 0))
        return True