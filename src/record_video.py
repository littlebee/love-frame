import pygame
from pygame.locals import MOUSEBUTTONDOWN

import lib.leds as leds
from lib.av_files import use_av_files
from lib.colors import Colors
from lib.sequenced_renderables import SequencedRenderables

from components.horz_panel import HorzPanel
from components.text import Text
from components.button import Button, ButtonSize
from components.live_video import LiveVideo, RAW_AUDIO_FILE, RAW_VIDEO_FILE
from components.exploding_text import ExplodingText
from components.recording_overlay import RecordingOverlay
from components.recorded_video import RecordedVideo
from components.timed_progress import TimedProgress
from components.button import Button, ButtonSize
from components.timer import Timer
from components.animated_heart import AnimatedHeart

# seconds until recording starts
LEAD_IN_TIME = 4
# default recording length in seconds
RECORDING_DURATION = 15
# seconds it takes to save
SAVING_DURATION = 15
# review starts after the above
REVIEW_STARTS = LEAD_IN_TIME + RECORDING_DURATION + SAVING_DURATION

# seconds until autosave at end of review
AUTOSAVE_AFTER = 20

class RecordVideo(object):

    def __init__(self, screen, on_closing=None):
        self.on_closing = on_closing
        self.has_closed = False
        self.has_saved = False
        self.av_files = use_av_files()

        self.surface = screen
        self.live_video = LiveVideo(self.surface)

        self.renderables = SequencedRenderables()
        self.renderables.append([
            [0, REVIEW_STARTS, lambda: self.live_video],
            [0, LEAD_IN_TIME, lambda: [
                HorzPanel(self.surface, top=0, height=140),
                Text(self.surface, f"Great!  Let's record a {RECORDING_DURATION} second video...",
                     56, (50, 50), Colors.ALMOST_BLACK
                ),
                HorzPanel(self.surface, top=450, height=150),
                Text(self.surface, "...and don't forget to speak up.",
                     36, (600, 500), Colors.ALMOST_BLACK
                ),
            ]],

            [0, 0, lambda: leds.bright_white()],

            [1, 0, lambda:
              ExplodingText(self.surface, "3", font_size=70, color=Colors.RED, duration=1.15)
            ],
            [2, 0, lambda:
              ExplodingText(self.surface, "2", font_size=70, color=Colors.RED, duration=1.15)
            ],
            [3, 0, lambda:
              ExplodingText(self.surface, "1", font_size=70, color=Colors.RED, duration=1.15)
            ],

            [LEAD_IN_TIME, RECORDING_DURATION, lambda :
                RecordingOverlay(self.surface, RECORDING_DURATION)
            ],

            # Sequenced renderables can also just be functions not returning a renderable
            [LEAD_IN_TIME, 0, self._start_recording],

            [LEAD_IN_TIME+RECORDING_DURATION, SAVING_DURATION, lambda : [
                TimedProgress(self.surface, duration=SAVING_DURATION),
                leds.fade_to(Colors.MIDNIGHT_BLUE)
            ]],

            [REVIEW_STARTS, 0, lambda:
                RecordedVideo(self.surface, RAW_VIDEO_FILE, RAW_AUDIO_FILE)
            ],

            [REVIEW_STARTS + 8, 0, lambda: [
                HorzPanel(self.surface, top=0, height=140),
                Text(self.surface, "Looks Great! They're going to love it.",
                     56, (50, 50), Colors.ALMOST_BLACK),
                HorzPanel(self.surface, top=400, height=200),
                Button(self.surface, "Keep it!",
                   pos=(800, 405),
                   size=ButtonSize.MEDIUM,
                   bg_color=Colors.GREEN,
                   fg_color=Colors.ALMOST_BLACK,
                   on_click=self.handle_save_click,
                ),
                Text(self.surface, "Auto-keep in", 24, (830, 520)),
                Timer(self.surface, (933, 520),
                      font_size=24,
                      reverse=True,
                      stop_after=AUTOSAVE_AFTER,
                      on_stop=self.handle_save_click,
                      show_hours=False,
                      show_minutes=False,
                ),
            ]],
            [REVIEW_STARTS + 9, 0, lambda:
                Button(self.surface, "Discard",
                       pos=(620, 455),
                       size=ButtonSize.SMALL,
                       bg_color=Colors.RED,
                       fg_color=Colors.OFF_WHITE,
                       on_click=self.handle_discard_click,
                       )


            ]
        ])

    def close(self):
        if not self.has_closed:
            self.live_video.close()
            self.has_closed = True

        hasattr(self, "on_closing") and self.on_closing()

    def handle_save_click(self):
        # it's possible that both the timer could expire just
        # after the user clicks the button
        if not self.has_saved:
            self.has_saved = True
            self.live_video.save()
            self.renderables.inject(
                AnimatedHeart(self.surface, on_close=self.close)
            )
            self.av_files.load_data()

    def handle_discard_click(self):
        # TODO : maybe add a sad trombone sound here
        self.close()

    def handle_pyg_event(self, event):
        return self.renderables.handle_pyg_event(event)

    def render(self, t):
        if self.has_closed:
            return False

        # this is full screen window
        self.surface.fill(Colors.ALMOST_BLACK)
        self.renderables.render(t)

        return True

    # called from sequence
    def _start_recording(self):
        self.live_video.record(RECORDING_DURATION)
