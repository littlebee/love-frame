#!/usr/bin/env python3

from pygame.locals import MOUSEBUTTONDOWN, FINGERDOWN, KEYDOWN, K_ESCAPE, K_q
import pygame
import random
import sys
import time


pygame.init()
pygame.display.set_caption("Click surface to create fading bubbles")

SCREEN_SIZE = [1024, 600]

BUBBLE_RADIUS_MIN = 50
BUBBLE_RADIUS_MAX = 100

# using time is much better than ticks as a proxy for time
FADE_DURATION = 1  # 1s
LIVE_DURATION = 1


class FadingBubble(object):

    def __init__(self, screen, pos):
        self.radius = random.randint(BUBBLE_RADIUS_MIN, BUBBLE_RADIUS_MAX)
        self.center = pos  # centered in our surface

        self.started_at = time.time()

        self.screen = screen
        self.surface = pygame.Surface(
            screen.get_size(), pygame.SRCALPHA)

    def render(self, t):
        duration = t - self.started_at

        if duration > FADE_DURATION * 2 + LIVE_DURATION:
            return False

        alpha = 255
        radius = self.radius

        if duration < FADE_DURATION:
            alpha = duration * (255 / FADE_DURATION)
        elif duration > LIVE_DURATION + FADE_DURATION:
            fade_duration = (duration - (LIVE_DURATION + FADE_DURATION))
            alpha = 255 - fade_duration * (255 / FADE_DURATION)
            radius = self.radius + fade_duration * 400

        # self.surface.set_alpha(alpha)

        color = pygame.Color(255, 255, 255)
        color.a = int(alpha)

        pygame.draw.circle(self.surface, color,
                           self.center, radius, self.radius)

        self.screen.blit(self.surface, (0, 0))

        return True

class TestSurfaceFade(object):

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.renderables = []
        self.screen = pygame.display.set_mode(SCREEN_SIZE)

    def render_loop(self):
        try:
            while True:
                for event in pygame.event.get():
                    # print(f"got pygame event {event}")
                    isQuitKey = event.type == KEYDOWN and event.key == K_q
                    if event.type == pygame.QUIT or isQuitKey:
                        sys.exit(0)
                        break
                    elif event.type in [MOUSEBUTTONDOWN, FINGERDOWN]:
                        pos = None
                        if event.type == MOUSEBUTTONDOWN:
                            pos = event.pos
                        else:
                            w, h = SCREEN_SIZE
                            pos = (event.x * w, event.y * h)

                        self.renderables.append(
                            FadingBubble(self.screen, pos))

                self.screen.fill((0, 0, 0))

                to_remove = []
                for renderable in self.renderables:
                    if renderable.render(time.time()) == False:
                        to_remove.append(renderable)

                for renderable in to_remove:
                    self.renderables.remove(renderable)

                pygame.display.update()
                self.clock.tick(30)

        except (KeyboardInterrupt, SystemExit):
            pygame.quit()


if __name__ == "__main__":
    app = TestSurfaceFade()
    app.render_loop()
