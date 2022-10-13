import pygame
from pygame.locals import MOUSEBUTTONDOWN


from lib.renderables import Renderables
from lib.colors import Colors
from lib.src_files import src_file

from components.live_video import FRAME_SIZE
from components.rectangle import Rectangle
from components.image import Image
from components.date_time import DateTime, DEFAULT_DT_FORMAT

PREV_ICON = src_file('reverse_icon.png')
NEXT_ICON = src_file('forward_icon.png')
PLAY_ICON = src_file('play_icon.png')

class MPButtonTypes:
    PLAY = 0
    PREV = 1
    NEXT = 2


class MessagePreviewButton(object):
    """
        Renders the previous message button that appears on the menu in NewMessages
        and on the PlayVideo

        This component does not self destruct
    """

    def __init__(
        self,
        parent_surface,
        pos,
        av_file,
        button_type=MPButtonTypes.PLAY,
        size=None,
        half_sized=False,
        on_click=None,
    ):
        self.has_closed = False
        self.parent_surface = parent_surface
        self.pos = pos
        self.av_file = av_file
        self.button_type = button_type
        self.size = size
        self.half_sized = half_sized
        self.on_click = on_click

        self.surface = pygame.Surface(parent_surface.get_size(), pygame.SRCALPHA)

        color = Colors.LIGHT_GREY if av_file.has_been_viewed else Colors.PURPLE
        crop_rect = self._compute_crop_rect()
        x, y = pos
        w, h = (crop_rect[2], crop_rect[3]) if crop_rect else self.size

        icon = self._get_icon(pos, (w, h))

        dt_format, font_size = ("%b. %-d", 24) if half_sized else (DEFAULT_DT_FORMAT, 24)
        dt = DateTime(self.surface, (x, y), int(av_file.name)/1000,
            fmt = dt_format,
            font_size=24
        )
        dt.text.center_for_size(w, h, y_offset=h/3)

        self.renderables = Renderables()
        self.renderables.append([
            Image(self.surface, pos,
                size=size,
                crop_rect=crop_rect,
                file_path=self.av_file.preview_file,
                on_click=self.on_click
            ),
            Rectangle(self.surface, (x, y, w, h),
                color = None,
                border_width = 3,
                border_color = color
            ),
            icon,
            dt,
        ])


    def close(self):
        self.has_closed = True


    def render(self, t):
        if self.has_closed:
            return False

        self.renderables.render(t)
        self.parent_surface.blit(self.surface, (0, 0))
        return True


    def handle_pyg_event(self, event):
        return self.renderables.handle_pyg_event(event)

    def _compute_crop_rect(self):
        crop_rect = None
        if self.size and self.half_sized:
            preview_w, preview_h = self.size
            if self.button_type == MPButtonTypes.PREV:
                crop_rect = (preview_w / 2, 0, preview_w / 2, preview_h)
            else:
                crop_rect = (0, 0, preview_w / 2, preview_h)

        elif self.half_sized:
            preview_w, preview_h = FRAME_SIZE
            if self.button_type == MPButtonTypes.PREV:
                crop_rect = (preview_w / 2, 0, preview_w / 2, preview_h)
            else:
                crop_rect = (0, 0, preview_w / 2, preview_h)

        return crop_rect


    def _get_icon(self, pos, size):
        icon_file = PLAY_ICON
        if self.button_type == MPButtonTypes.PREV:
            icon_file = PREV_ICON
        elif self.button_type == MPButtonTypes.NEXT:
            icon_file = NEXT_ICON

        return Image(self.surface, pos, icon_file, size)