#!/usr/bin/env python3
from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import sys
import cv2

from lib.renderables import Renderables

from gallery import Gallery
from menu import Menu, MenuActions
from record_video import RecordVideo


pygame.init()
pygame.display.set_caption("Join the love frame")
screen = pygame.display.set_mode([1024, 600], pygame.NOFRAME)


class LoveFrame(object):

    def __init__(self):
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
            screen,
            on_closing=self.renderMenu
        )
        self.renderables.append(gallery)

    def renderMenu(self):
        menu = Menu(
            screen,
            on_closing=self.handle_menu_closing
        )
        self.renderables.append(menu)

    def renderRecordVideo(self):
        record_video = RecordVideo(screen, on_closing=self.renderGallery)
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

                screen.fill((0, 0, 0))
                self.renderables.render()
                pygame.display.update()
                self.clock.tick(30)

        except (KeyboardInterrupt, SystemExit):
            pygame.quit()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    app = LoveFrame()
    app.render_loop()
