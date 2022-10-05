import pygame


class MutableText(object):
    """
        The MutableText object is for displaying text that changes.  It is less efficient
        than the standard Text component because it renders the font on each render loop.

        This component does not self destruct

        See also (./text.py) for a immutable version for use with static text.
    """


    def __init__(
        self,
        surface,
        value,
        font_size=32,
        position=(0, 0),
        fg_color=(127, 127, 127),
        bg_color=None
    ):
        self.surface = surface
        self.value = value
        self.position = position
        self.fg_color = fg_color
        self.bg_color = bg_color

        self.has_closed = False

        self.font = pygame.font.Font(None, font_size)


    def close(self):
        self.has_closed = True

    def set_value(self, value):
        self.value = value

    def render(self, t):
        if self.has_closed:
            return False

        text = self.font.render(self.value, True, self.fg_color, self.bg_color)
        textRect = text.get_rect()
        textRect.topleft = self.position
        self.surface.blit(text, textRect)

        return True
