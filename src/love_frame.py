#!/usr/bin/env python3
from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import sys
import cv2

from lib.constants import RENDER_FPS
from lib.renderables import Renderables

from gallery import Gallery
from menu import Menu, MenuActions
from record_video import RecordVideo

from components.live_video import LiveVideo


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

        self.renderGallery()

    def handle_menu_closing(self, action):
        if action == MenuActions.RECORD_VIDEO:
            self.renderRecordVideo()
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

    def render_loop(self):
        try:
            while True:
                for event in pygame.event.get():
                    isQuitKey = event.type == KEYDOWN and event.key == K_q
                    if event.type == pygame.QUIT or isQuitKey:
                        sys.exit(0)
                        break

                    self.renderables.handle_pyg_event(event)

                self.surface.fill((0, 0, 0))
                self.renderables.render()

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
