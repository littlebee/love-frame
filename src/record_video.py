import pygame
from pygame.locals import MOUSEBUTTONDOWN

from lib.colors import Colors
from lib.sequenced_renderables import SequencedRenderables

from components.text import Text
from components.button import Button, ButtonSize
from components.live_video import LiveVideo
from components.exploding_text import ExplodingText

# seconds until recording starts
LEAD_IN_TIME = 4
# default recording length in seconds
RECORDING_DURATION = 15


class RecordVideo(object):

    def __init__(self, screen, on_closing=None):
        self.on_closing = on_closing
        self.has_closed = False

        self.surface = screen
        self.live_video = LiveVideo(self.surface)

        self.renderables = SequencedRenderables()
        self.renderables.append([
            [0, 0, lambda: self.live_video],
            [0, LEAD_IN_TIME, lambda:
                Text(self.surface, f"Great!  Let's record a {RECORDING_DURATION} second video...",
                     56, (50, 60), Colors.ALMOST_BLACK)
             ],
            [0, LEAD_IN_TIME, lambda:
                Text(self.surface, "...and don't forget to speak up.",
                     36, (600, 500), Colors.ALMOST_BLACK)
             ],

            [1, 0, lambda:
              ExplodingText(self.surface, "3", font_size=70, color=Colors.RED, duration=1.15)
            ],
            [2, 0, lambda:
              ExplodingText(self.surface, "2", font_size=70, color=Colors.RED, duration=1.15)
            ],
            [3, 0, lambda:
              ExplodingText(self.surface, "1", font_size=70, color=Colors.RED, duration=1.15)
            ],

            # [LEAD_IN_TIME, 0, self._start_recording],

            [LEAD_IN_TIME + RECORDING_DURATION, 0, lambda:
                Text(self.surface, f"Looks Great! They're going to love it.",
                     56, (50, 60), Colors.ALMOST_BLACK)
             ],

        ])

    def close(self):
        if not self.has_closed:
            self.live_video.close()
            self.has_closed = True

        hasattr(self, "on_closing") and self.on_closing()

    def handle_pyg_event(self, event):
        # TODO : remove this
        if event.type == MOUSEBUTTONDOWN:
            self.close()
            return True  # stop propagation

        return self.renderables.handle_pyg_event(event)

    def render(self):
        if self.has_closed:
            return False

        # this is full screen window
        self.surface.fill(Colors.OFF_WHITE)
        self.renderables.render()

        return True

    # called from sequence
    def _start_recording(self):
        self.live_video.record(RECORDING_DURATION)
