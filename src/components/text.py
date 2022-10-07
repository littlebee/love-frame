import pygame


class Text(object):
    """
        The Text object is for displaying immutable, static text.

        This component does not self destruct

        See also (./mutable_text.py) for a mutable version
    """


    def __init__(
        self,
        screen,
        value,
        font_size=32,
        position=(0, 0),
        fg_color=(127, 127, 127),
        bg_color=None
    ):
        self.screen = screen
        self.has_closed = False

        # 1st parameter is the font file
        # which is present in pygame.
        # 2nd parameter is size of the font
        font = pygame.font.Font(None, font_size)

        # create a text surface object,
        # on which text is drawn on it.
        self.text = font.render(value, True,
                                fg_color, bg_color)

        # create a rectangular object for the
        # text surface object
        self.textRect = self.text.get_rect()
        self.textRect.topleft = position

    def center_on_screen(self, x_offset=0, y_offset=0):
        screen_w, screen_h = self.screen.get_size()
        # set the center of the rectangular object.
        self.textRect.center = (screen_w // 2 + x_offset, screen_h // 2 + y_offset)

    def close(self):
        self.has_closed = True

    def render(self, t):
        if self.has_closed:
            return False

        self.screen.blit(self.text, self.textRect)

        return True
