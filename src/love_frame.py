#!/usr/bin/env python3
import cv2
from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import sys
import time

from lib.colors import  Colors
from lib.constants import RENDER_FPS
from lib.renderables import Renderables
from lib.pygame_utils import translate_touch_event
from lib.leds import initLeds, fill

from gallery import Gallery
from menu import Menu, MenuActions
from record_video import RecordVideo
from play_message import PlayMessage

pygame.init()
pygame.display.set_caption("Join the love frame")
screen = pygame.display.set_mode([1024, 600], pygame.NOFRAME)


class LoveFrame(object):

    def __init__(self):
        # ## Using a Surface causes video lag :(
        # self.surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.surface = screen

        self.clock = pygame.time.Clock()
        self.renderables = Renderables()

        initLeds()
        fill(Colors.MIDNIGHT_BLUE)

        self.renderGallery()


    def handle_menu_closing(self, action, data):
        if action == MenuActions.RECORD_VIDEO:
            self.renderRecordVideo()
        elif action == MenuActions.PLAY_MESSAGE:
            self.renderPlayMessage(data)
        else:
            self.renderGallery()


    def handle_play_message_closing(self, action, data):
        # message player can only direct back to playing the next / prev message
        # or return to gallery (for now)
        if action == MenuActions.PLAY_MESSAGE:
            self.renderPlayMessage(data)
        else:
            self.renderGallery()


    def renderGallery(self):
        gallery = Gallery(
            self.surface,
            on_closing=self.renderMenu
        )
        self.renderables.append(gallery)


    def renderMenu(self):
        menu = Menu(
            self.surface,
            on_closing=self.handle_menu_closing
        )
        self.renderables.append(menu)


    def renderRecordVideo(self):
        record_video = RecordVideo(self.surface, on_closing=self.renderGallery)
        self.renderables.append(record_video)


    def renderPlayMessage(self, name_key):
        play_message = PlayMessage(self.surface,
            name_key,
            on_closing=self.handle_play_message_closing
        )
        self.renderables.append(play_message)


    def render_loop(self):
        try:
            while True:
                for event in pygame.event.get():
                    # print(f"got event from pygame {event}")
                    isQuitKey = event.type == KEYDOWN and event.key == K_q
                    if event.type == pygame.QUIT or isQuitKey:
                        sys.exit(0)
                        break

                    translated_event = translate_touch_event(self.surface, event)
                    self.renderables.handle_pyg_event(translated_event)

                self.surface.fill((0, 0, 0))

                # the current timestamp is passed so that animated components can
                # have a reliable time sequence when running on slower SBCs like
                # the raspberry pi4
                self.renderables.render(time.time())

                # using a surface here increased live video lag
                # screen.blit(self.surface, (0, 0))

                pygame.display.update()
                self.clock.tick(RENDER_FPS)

        except (KeyboardInterrupt, SystemExit):
            self.renderables.close()
            pygame.quit()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    app = LoveFrame()
    app.render_loop()
