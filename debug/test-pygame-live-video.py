#!/usr/bin/env python3

from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import cv2
import sys

camera = cv2.VideoCapture(0)
pygame.init()
pygame.display.set_caption("debug/test-pygame-live-video")
screen = pygame.display.set_mode([1280, 720])


def convert_opencv_img_to_pygame(opencv_image):
    """
        Convert OpenCV images for Pygame.

        see https://blanktar.jp/blog/2016/01/pygame-draw-opencv-image.html
    """
    opencv_image = opencv_image[:, :, ::-
                                1]  # Since OpenCV is BGR and pygame is RGB, it is necessary to convert it.
    # OpenCV(height,width,Number of colors), Pygame(width, height)So this is also converted.
    shape = opencv_image.shape[1::-1]
    pygame_image = pygame.image.frombuffer(
        opencv_image.tobytes(), shape, 'RGB')

    return pygame_image


try:
    while True:
        screen.fill([0, 0, 0])

        ret, frame = camera.read()
        screen.blit(convert_opencv_img_to_pygame(frame), (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    sys.exit(0)

except (KeyboardInterrupt, SystemExit):
    pygame.quit()
    cv2.destroyAllWindows()
