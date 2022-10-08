import pygame


class HorzPanel(object):
    """
        Renders a translucent horizontal panel the width of the surface.  Used as back drop
        for text that renders over video.

        This component does not self destruct
    """

    def __init__(
        self,
        parent_surface,
        top=0,
        height=100,
    ):
        self.has_closed = False
        self.parent_surface = parent_surface
        parent_w, parent_h = parent_surface.get_size()

        surface_size = (parent_w, height)
        self.surface = pygame.Surface(surface_size, pygame.SRCALPHA, 32)

        # where we render in parent
        self.render_rect = pygame.Rect(0, top, parent_w, height)
        # where we draw the rectangle within our surface
        drawing_rect = pygame.Rect(0, 0, parent_w, height)

        color = pygame.Color(255, 255, 255)
        color.a = 98

        pygame.draw.rect(self.surface, color, drawing_rect)

    def close(self):
        self.has_closed = True

    def render(self, t):
        if self.has_closed:
            return False

        self.parent_surface.blit(self.surface, self.render_rect)

        return True
