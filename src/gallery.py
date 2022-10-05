import os
import random
import time
import threading

import cv2
import numpy as np
import pygame
from pygame.locals import MOUSEBUTTONDOWN

import lib.image_utils as img

PICTURES_PATH = "./data/gallery"
DISPLAY_SECONDS = 7


class Gallery(object):

    def __init__(self, screen, on_closing=None):
        self.on_closing = on_closing

        self.has_closed = False
        self.image = None
        self.image_coords = (0, 0)
        self.dominant_color = [0, 0, 0]
        self.last_image_at = 0

        self.surface = screen

    def close(self):
        self.on_closing and self.on_closing()
        self.has_closed = True

    def handle_pyg_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.close()
            return True  # stop propagation

        return False

    def render(self, t):
        if self.has_closed:
            return False

        if t - self.last_image_at > DISPLAY_SECONDS:
            self._get_next_image()

        if self.image != None:
            self.surface.fill(self.dominant_color)
            self.surface.blit(self.image, self.image_coords)

        return True

    def _get_next_image(self):
        # get a random picture of Betsy and Josh
        files = os.listdir(PICTURES_PATH)
        file = random.choice(files)
        file_path = f"{PICTURES_PATH}/{file}"
        cv_image = cv2.imread(file_path, cv2.IMREAD_COLOR)

        pyg_image = img.opencv_to_pyg(cv_image)
        pyg_image = img.scale_pygimage_to_screen(self.surface, pyg_image)
        img_coords = img.center_pygimage_on_screen(self.surface, pyg_image)

        # it takes a few hundred ms to compute the dominant color on
        # raspberry pi, so do that before setting the image
        self.dominant_color = img.get_dominant_color(cv_image)
        self.image = pyg_image
        self.image_coords = img_coords
        self.last_image_at = time.time()
