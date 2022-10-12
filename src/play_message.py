import pygame
from pygame.locals import MOUSEBUTTONDOWN
import time

from lib.av_files import AvFiles
from lib.colors import Colors
from lib.renderables import Renderables

from components.button import Button, ButtonSize
from components.recorded_video import RecordedVideo
from components.message_preview_button import MessagePreviewButton, MPButtonTypes

from menu import MenuActions


# PlayMessage closes to gallery after 30 seconds without selecting
# anything else (15 seconds after playback stops)
AUTO_CLOSE_AFTER = 30

PREVIEW_SIZE = (180, 120)


class PlayMessage(object):

    def __init__(self, surface, name_key, on_closing=None):
        self.surface = surface
        self.name_key = name_key
        self.on_closing = on_closing

        self.has_closed = False
        self.started_at = time.time()

        self.av_files = AvFiles()
        self.av_files.point_to_name(name_key)

        self.av_file = av_file = self.av_files.current_av_file()
        prev_file = self.av_files.previous_av_file()
        next_file = self.av_files.next_av_file()

        self.video = RecordedVideo(self.surface, av_file.vid_file, av_file.aud_file,
            on_playback_complete=self.handle_playback_complete,
        )

        self.renderables = Renderables()
        self.renderables.append([
            self.video,
        ])

        if prev_file:
            self.renderables.append(
                MessagePreviewButton(self.surface, (40, 450),
                    button_type=MPButtonTypes.PREV,
                    av_file=prev_file,
                    size=PREVIEW_SIZE,
                    on_click=self.handle_previous_click
                )
            )

        if next_file:
            self.renderables.append(
                MessagePreviewButton(self.surface, (800, 450),
                    button_type=MPButtonTypes.NEXT,
                    av_file=next_file,
                    size=PREVIEW_SIZE,
                    on_click=self.handle_next_click
                )
            )



    def close(self, action=MenuActions.GALLERY, data=None):
        self.has_closed = True
        self.renderables.close()
        self.on_closing(action, data)


    def handle_pyg_event(self, event):
        event_handled = self.renderables.handle_pyg_event(event)

        if not event_handled and event.type == MOUSEBUTTONDOWN:
            self.close(MenuActions.GALLERY)
            return True

        return event_handled

    def handle_previous_click(self):
        av_name_key = self.av_files.previous_av_file().name
        self.close(MenuActions.PLAY_MESSAGE, av_name_key);

    def handle_next_click(self):
        av_name_key = self.av_files.next_av_file().name
        self.close(MenuActions.PLAY_MESSAGE, av_name_key);

    def handle_playback_complete(self):
        self.av_file.mark_as_viewed()


    def render(self, t):
        if self.has_closed:
            return False

        if t - self.started_at > AUTO_CLOSE_AFTER:
            self.close(MenuActions.GALLERY)

        # this is full screen window
        self.surface.fill(Colors.OFF_WHITE)
        self.renderables.render(t)

        return True
