import pygame
from pygame.locals import MOUSEBUTTONDOWN, FINGERDOWN


def translate_touch_event(screen, event):
    """
        If event is FINGERDOWN, this function returns a MOUSEBUTTONDOWN
        event with a `pos` member that is translated from the FINGERDOWN x and y

        Other events are returned untouched
    """
    event_out = event
    if event.type == FINGERDOWN:
        w, h = screen.get_size()
        pos = (int(event.x * w), int(event.y * h))
        # print(f"got touch event {event.x},{event.y} {w},{h} -> {pos}")
        event_out = pygame.event.Event(MOUSEBUTTONDOWN, pos=pos)

    return event_out
