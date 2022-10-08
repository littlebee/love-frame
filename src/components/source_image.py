import pygame

SOURCE_IMAGES_DIR = "src/images"

class SourceImage(object):

    def __init__(self, surface, img_file, rect):
        self.surface = surface
        self.image = pygame.image.load(f"{SOURCE_IMAGES_DIR}/{img_file}").convert_alpha()
        self.rect = pygame.rect.Rect(rect)
        self.has_closed = False

    def close(self):
        self.has_closed = True

    def set_rect(self, new_rect):
        self.rect = pygame.rect.Rect(new_rect)

    def center(self):
        w, h = self.surface.get_size()
        self.rect.center = (w / 2, h / 2)

    def scale(self, scale_factor):
        self.rect.w = self.rect.w * scale_factor
        self.rect.h = self.rect.h * scale_factor

    def render(self, t):
        if self.has_closed:
            return False;

        scaled_image = pygame.transform.scale(self.image, (self.rect.w, self.rect.h))
        self.surface.blit(scaled_image, self.rect)

        return True;