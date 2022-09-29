import cv2

from lib.image_utils import opencv_to_pyg


class LiveVideo(object):

    def __init__(self, screen):
        self.screen = screen
        # start the capture
        self.camera = cv2.VideoCapture(0)

    def __del__(self):
        self.camera.release()

    def render(self):
        ret, frame = self.camera.read()
        self.screen.blit(opencv_to_pyg(frame), (0, 0))
