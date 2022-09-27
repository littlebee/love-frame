import os
import random
import time
import threading

import cv2
import numpy as np
import pygame
from pygame.locals import MOUSEBUTTONDOWN


import lib.image_utils as img
from components.fader import Fader

PICTURES_PATH = "./data/gallery"
DISPLAY_SECONDS = 7


class Gallery(object):

    def __init__(self, screen, on_closing=None):
        self.screen = screen
        self.on_closing = on_closing

        self.has_closed = False
        self.image = None
        self.image_coords = (0, 0)
        self.dominant_color = [0, 0, 0]

        self.fader = Fader(screen, on_close=self.handle_fader_close)

        self.next_image_thread_running = True
        self.next_image_thread = threading.Thread(
            target=self._set_next_image_thread)
        self.next_image_thread.start()

    def __del__(self):
        self._kill_next_image_thread()

    def handle_fader_close(self):
        self.has_closed = True
        self.next_image_thread.join()

    def handle_pyg_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self._kill_next_image_thread()
            self.on_closing and self.on_closing()
            self.fader.close()

            return True  # stop propagation

        return False

    def render(self):
        if self.has_closed:
            return False

        if self.image != None:
            self.fader.surface.fill(self.dominant_color)
            self.fader.surface.blit(self.image, self.image_coords)
            self.fader.render()

        return True

    def _set_next_image_thread(self):
        while self.next_image_thread_running:
            # get a random picture of Betsy and Josh
            files = os.listdir(PICTURES_PATH)
            file = random.choice(files)
            file_path = f"{PICTURES_PATH}/{file}"
            cv_image = cv2.imread(file_path, cv2.IMREAD_COLOR)

            pyg_image = img.opencv_to_pyg(cv_image)
            pyg_image = img.scale_pygimage_to_screen(self.screen, pyg_image)
            img_coords = img.center_pygimage_on_screen(self.screen, pyg_image)

            # it takes a few hundred ms to compute the dominant color on
            # raspberry pi, so do that before setting the image
            self.dominant_color = img.get_dominant_color(cv_image)
            self.image = pyg_image
            self.image_coords = img_coords

            time.sleep(DISPLAY_SECONDS)

    def _kill_next_image_thread(self):
        if self.next_image_thread_running == True:
            self.next_image_thread_running = False
