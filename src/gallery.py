import os
import random
import time
import threading

import cv2
import numpy as np
import pygame

import lib.image_utils as img

PICTURES_PATH = "./data/gallery"
DISPLAY_SECONDS = 7


class Gallery(object):

    def __init__(self, screen):
        self.screen = screen
        self.image = None
        self.image_coords = (0, 0)
        self.dominant_color = [0, 0, 0]

        self.next_image_thread_running = True
        self.next_image_thread = threading.Thread(
            target=self._set_next_image_thread)
        self.next_image_thread.start()

    def __del__(self):
        self._kill_next_image_thread()
        # don't let self to destruct until next image thread has exited
        self.next_image_thread.join()

    def render(self):
        if self.image != None:
            self.screen.fill(self.dominant_color)
            self.screen.blit(self.image, self.image_coords)

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

            self.dominant_color = img.get_dominant_color(cv_image)
            self.image = pyg_image
            self.image_coords = img_coords

            time.sleep(DISPLAY_SECONDS)

    def _kill_next_image_thread(self):
        if self.next_image_thread_running == True:
            self.next_image_thread_running = False
