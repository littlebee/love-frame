import pygame

from lib.renderables import Renderables
from lib.colors import Colors

from components.text import Text
from components.flashing_light import FlashingLight
from components.timer import Timer
from components.battery import Battery

class RecordingOverlay(object):
    """
        Renders an overlay similar to an old school camcorder that is displayed
        when recording video message.

        This component does not self destruct
    """

    def __init__(
        self,
        surface,
        recording_duration=15,
    ):
        self.has_closed = False
        self.surface = surface

        self.renderables = Renderables()
        self.renderables.append([
            FlashingLight(surface, 10, (60, 67), Colors.RED),
            Text(surface, "Rec", 24, (75, 60), Colors.GREY),
            Timer(surface, (480, 500), stop_after=recording_duration),
            Battery(surface, duration=recording_duration),
        ])


    def close(self):
        self.has_closed = True

    def render(self, t):
        if self.has_closed:
            return False

        self.renderables.render(t)

        return True
