#!/usr/bin/env python3

from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE, K_q
import pygame
import random
import sys


pygame.init()
pygame.display.set_caption("Press a keyboard key")

STARTING_FONT_SIZE = 50
SCALING_FACTOR = .2
TTL_TICKS = 45

class ExplodingText(object):

    def __init__(self, surface, value):
        self.surface = surface
        self.value = value

        self.render_ticks = 0
        self.has_closed = False

        self.font = pygame.font.Font(None, STARTING_FONT_SIZE)


    def render(self):
        if self.has_closed:
            return False

        self.render_ticks += 1
        # scale = 1.01;
        scale = 1 + (SCALING_FACTOR * self.render_ticks);
        alpha = int(255 - (255 / TTL_TICKS * self.render_ticks))

        if alpha <= 0:
            self.has_closed = True
            return False;

        text = self.font.render(self.value, True, (255, 255, 255), None)
        text.set_alpha(alpha)
        text_rect = text.get_rect()

        new_size = (
            int(text_rect.width * scale),
            int(text_rect.height * scale),
        )
        scaled = pygame.transform.scale(text, new_size)

        scaled_rect = scaled.get_rect()
        screen_w, screen_h = self.surface.get_size()
        # set the center of the rectangular object.
        scaled_rect.center = (screen_w // 2, screen_h // 2)

        self.surface.blit(scaled, scaled_rect)

        return True


class TestApp(object):

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.renderables = []
        self.screen = pygame.display.set_mode([1024, 600])
        self.surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

    def render_loop(self):
        try:
            while True:
                for event in pygame.event.get():
                    isQuitKey = event.type == KEYDOWN and event.key == K_q
                    if event.type == pygame.QUIT or isQuitKey:
                        sys.exit(0)
                        break
                    elif event.type == KEYDOWN:
                        self.renderables.append(
                            ExplodingText(self.surface, f"{event.key:c}")
                        )

                self.surface.fill((0, 0, 0))

                to_remove = []
                for renderable in self.renderables:
                    if renderable.render() == False:
                        to_remove.append(renderable)

                for renderable in to_remove:
                    self.renderables.remove(renderable)

                self.screen.blit(self.surface, (0, 0))
                pygame.display.update()
                self.clock.tick(30)

        except (KeyboardInterrupt, SystemExit):
            pygame.quit()


if __name__ == "__main__":
    app = TestApp()
    app.render_loop()
