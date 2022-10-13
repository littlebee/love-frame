import os
from pathlib import Path
import pygame
from pygame.locals import MOUSEBUTTONDOWN


import lib.constants as c


NO_FILE_PATH = f"{c.SOURCE_IMAGES_DIR}/no_preview.png"

class Image(object):

    def __init__(self, surface, pos,
        file_path,
        size = None,
        crop_rect = None,
        on_click=None
    ):
        self.surface = surface
        self.pos = pos
        self.size = size
        self.crop_rect = crop_rect
        self.on_click = on_click

        file_exists = file_path != None and Path(file_path).is_file()
        if file_exists:
            self.image = pygame.image.load(file_path).convert_alpha()
        else:
            self.image = pygame.image.load(NO_FILE_PATH).convert_alpha()

        self.rect = pygame.rect.Rect(pos[0], pos[1], 0, 0)

        if crop_rect and size:
            self.rect.w = min(crop_rect[2], size[0])
            self.rect.h = min(crop_rect[3], size[1])
        elif crop_rect:
            self.rect.size = (crop_rect[2], crop_rect[3])
        elif size:
            self.rect.size = size
        else:
            self.rect.size = self.image.get_size()

        self.has_closed = False

    def center(self):
        sw, sh = self.surface.get_size()
        zw, zh = self.size if self.size else self.image.get_size()

        self.pos = (sw / 2 - zw / 2, sh / 2 - zh / 2)
        self.rect.center = (w / 2, h / 2)


    def scale(self, scale_factor):
        if size:
            w, h = size
            size = (w * scale_factor, h * scale_factor)

        self.rect.w = self.rect.w * scale_factor
        self.rect.h = self.rect.h * scale_factor


    def close(self):
        self.has_closed = True


    def render(self, t):
        if self.has_closed:
            return False;

        if self.size:
            w, h = self.size
            scaled_image = pygame.transform.scale(self.image, (w, h))
        else:
            scaled_image = self.image;

        if self.crop_rect:
            cropped_image = scaled_image.subsurface(self.crop_rect)
        else:
            cropped_image = scaled_image

        self.surface.blit(cropped_image, self.pos)

        return True;

    def handle_pyg_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            print(f"got event {event.pos} {self.rect}")
        if callable(self.on_click) and event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.on_click()
            return True

        return False
