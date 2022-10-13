import pygame

from lib.renderables import Renderables
from lib.colors import Colors
from lib.av_files import AvFiles

from components.live_video import FRAME_SIZE
from components.image import Image
from components.message_preview_button import MessagePreviewButton, MPButtonTypes
from components.rectangle import Rectangle
from components.text import Text

PREVIEW_SIZE = (250, 200)

class NewMessages(object):
    """
        Renders the component in the menu that shows (new) messages.

        This component does not self destruct
    """

    def __init__(
        self,
        surface,
        on_preview_click=None
    ):
        self.has_closed = False
        self.surface = surface
        self.on_preview_click = on_preview_click

        self.av_files = AvFiles()
        self.renderables = None
        self.update_renderables()

    def update_renderables(self):
        self.renderables and self.renderables.close()
        self.current_av_file = self.av_files.current_av_file()
        self.prev_av_file = self.av_files.previous_av_file()
        self.next_av_file = self.av_files.next_av_file()

        count_str = "no"
        punctuation = "."
        color = Colors.LIGHT_GREY
        if self.av_files.unviewed_count > 0:
            count_str = str(self.av_files.unviewed_count)
            punctuation = "!"
            color = Colors.PURPLE

        title = f"You have {count_str} new messages{punctuation}"

        preview_w, preview_h = PREVIEW_SIZE
        left_crop_rect = 0, 0, preview_w / 2, preview_h
        right_crop_rect = preview_w / 2, 0, preview_w / 2, preview_h

        self.renderables = Renderables()
        self.renderables.append([
            Text(self.surface, title, 40, (100, 250), color),
        ])

        if self.current_av_file:
            self.renderables.append([
                MessagePreviewButton(self.surface, (150, 300),
                    av_file=self.current_av_file,
                    button_type=MPButtonTypes.PLAY,
                    size=PREVIEW_SIZE,
                    on_click=self.handle_preview_click,
                )
            ])
        else:
            self.renderables.append([
                Text(self.surface, "No Messages", 32, (195, 350), Colors.LIGHT_GREY),
                Text(self.surface, "Recorded Yet", 32, (195, 380), Colors.LIGHT_GREY),

            ])

        if self.prev_av_file:
            self.renderables.append(
                MessagePreviewButton(self.surface, (29, 300),
                    av_file=self.prev_av_file,
                    button_type=MPButtonTypes.PREV,
                    size=PREVIEW_SIZE,
                    half_sized=True,
                    on_click=self.handle_previous_click,
                )
            )


        if self.next_av_file:
            self.renderables.append(
                MessagePreviewButton(self.surface, (396, 300),
                    av_file=self.next_av_file,
                    button_type=MPButtonTypes.NEXT,
                    size=PREVIEW_SIZE,
                    half_sized=True,
                    on_click=self.handle_next_click,
                )
            )



    def close(self):
        self.has_closed = True


    def render(self, t):
        if self.has_closed:
            return False

        self.renderables.render(t)

        return True


    def handle_pyg_event(self, event):
        self.renderables.handle_pyg_event(event)


    def handle_preview_click(self):
        if callable(self.on_preview_click):
            self.on_preview_click(self.av_files.current_av_file().name)


    def handle_previous_click(self):
        self.av_files.point_to_previous()
        self.update_renderables()


    def handle_next_click(self):
        self.av_files.point_to_next()
        self.update_renderables()

