import pygame


class Text(object):

    def __init__(
        self,
        screen,
        value,
        font_size=32,
        position=(0, 0),
        fg_color=(128, 128, 128),
        bg_color=None
    ):
        self.screen = screen

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

    def center_on_screen(self):
        screen_w, screen_h = self.screen.get_size()
        # set the center of the rectangular object.
        self.textRect.center = (screen_w // 2, screen_h // 2)

    def render(self):
        self.screen.blit(self.text, self.textRect)
