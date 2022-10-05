import pygame

from lib.renderables import Renderables
from lib.colors import Colors

from components.flashing_bar import FlashingBar
from components.rectangle import Rectangle

TOP_LEFT=(900, 50)
BARS=4


class Battery(object):
    """
        Renders an old school camcorder style battery monitor that decreases bars
        as duration expires.

        This component does not self destruct
    """

    def __init__(
        self,
        surface,
        duration=15,
    ):
        self.has_closed = False
        self.surface = surface


        self.renderables = Renderables()
        self.renderables.append([
            Rectangle(
                self.surface,
                (TOP_LEFT[0], TOP_LEFT[1] + 10, 5, 20)
            ),
            Rectangle(
                self.surface,
                (TOP_LEFT[0] + 5, TOP_LEFT[1], 65, 40),
                color=None,
                border_width=3,
                border_color=Colors.GREY
            )
        ])

        qt = duration / BARS
        for i in range(4):
            flash_color, flash_after = (Colors.GREEN, i * qt + 1) if i < 3 else (Colors.RED, i * qt)
            dim_after = i * qt + 3 * qt / BARS
            self.renderables.append([
                FlashingBar(surface, (10 + TOP_LEFT[0] + i * 15, TOP_LEFT[1] + 5, 10, 30),
                    flash_color = flash_color,
                    flash_after = flash_after,
                    dim_after = dim_after,
                )
        ])


    def close(self):
        self.has_closed = True

    def render(self, t):
        if self.has_closed:
            return False

        self.renderables.render(t)

        return True
