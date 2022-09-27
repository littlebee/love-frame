import pygame


FADE_DURATION = 200  # in game clock ticks


class Fader(object):
    """
        Fader creates surface for other renderables that can fade those
        components in and out.

        You MUST pass this class instance surface instead of screen to
        other renderables for Fader to have an effect on them.

        example:
          self.fader = Fader(screen, on_close=self.close)
          self.renderables.append([
              Text(fader.surface, "this is some text to render")
              # fader should be rendered after any other renderables using it's surface
              fader,
          ])

    """

    def __init__(self, screen, on_close=None):
        self.screen = screen
        self.on_close = on_close
        self.is_closing = False
        self.fade_ticks_remaining = FADE_DURATION

        self.surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    def close(self):
        self.fade_ticks_remaining = FADE_DURATION
        self.is_closing = True

    def fade_surface(self):
        alpha = 255

        if self.fade_ticks_remaining > 0:
            if self.is_closing:
                if self.fade_ticks_remaining <= 0:
                    self.has_closed = true
                    return False
                alpha = self.fade_ticks_remaining * (255 / FADE_DURATION)
            else:
                alpha = 255 - self.fade_ticks_remaining * (255 / FADE_DURATION)

            self.fade_ticks_remaining -= 1

        self.surface.set_alpha(alpha)

    def render(self):
        if self.is_closing and self.fade_ticks_remaining <= 0:
            self.on_close and self.on_close()
            return False

        self.fade_surface()

        self.screen.blit(self.surface, (0, 0))
