#!/usr/bin/env python3
from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import sys
import cv2

from gallery import Gallery


pygame.init()
pygame.display.set_caption("Join the love frame")
screen = pygame.display.set_mode([1024, 600], pygame.NOFRAME)

currentComponent = Gallery(screen)


try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    sys.exit(0)
                screen.fill([0, 0, 0])

        currentComponent.render()
        pygame.display.update()

except (KeyboardInterrupt, SystemExit):
    pygame.quit()
    cv2.destroyAllWindows()
