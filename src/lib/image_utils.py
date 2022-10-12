
import numpy as np
import pygame


def opencv_to_pyg(opencv_image):
    """
        Convert OpenCV images for Pygame.

        source: https://blanktar.jp/blog/2016/01/pygame-draw-opencv-image.html
    """
    # Since OpenCV is BGR and pygame is RGB, it is necessary to convert it.
    opencv_image = opencv_image[:, :, ::-1]
    # OpenCV(height,width,Number of colors), Pygame(width, height)So this is also converted.
    shape = opencv_image.shape[1::-1]
    pygame_image = pygame.image.frombuffer(
        opencv_image.tobytes(), shape, 'RGB')

    return pygame_image


def get_dominant_color(opencv_image):
    """
        Returns the dominant color for a given open cv image

        source: https://stackoverflow.com/questions/50899692/most-dominant-color-in-rgb-image-opencv-numpy-python
    """
    a2D = opencv_image.reshape(-1, opencv_image.shape[-1])
    col_range = (256, 256, 256)  # generically : a2D.max(0)+1
    a1D = np.ravel_multi_index(a2D.T, col_range)
    max_bin = np.bincount(a1D).argmax()
    color = np.unravel_index(max_bin, col_range)

    # return color as rgb (opencv is bgr)
    return color[::-1]


def scale_pygimage_to_screen(screen, pyg_image):
    """
        Scales pygame image to fit on screen while maintaining aspect ratio.

        returns new scaled image
    """
    screen_w, screen_h = screen.get_size()
    img_w, img_h = pyg_image.get_size()

    diff_w = img_w - screen_w
    diff_h = img_h - screen_h

    new_w = screen_w
    new_h = screen_h

    if diff_w > 0 and diff_w > diff_h:
        new_h = int(img_h * (screen_w / img_w))
    else:
        new_w = int(img_w * (screen_h / img_h))

    return pygame.transform.scale(pyg_image, (new_w, new_h))


def center_pygimage_on_screen(screen, pyg_image):
    """
        Returns (x,y) coordinates to center image on the screen
    """
    screen_w, screen_h = screen.get_size()
    img_w, img_h = pyg_image.get_size()

    x, y = (0, 0)
    if img_w < screen_w:
        x = (screen_w - img_w) / 2
    if img_h < screen_h:
        y = (screen_h - img_h) / 2

    return (x, y)
