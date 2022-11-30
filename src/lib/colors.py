
class Colors(object):
    GREEN = (0, 200, 10)
    OFF_WHITE = (220, 220, 220)
    ALMOST_BLACK = (30, 30, 30)
    BUTTON_BLUE = (49, 19, 214)
    RED = (200, 10, 10)
    DARK_GREY = (64, 64, 64)
    GREY = (127, 127, 127)
    LIGHT_GREY = (192, 192, 192)
    PURPLE = (139, 16, 232)
    MIDNIGHT_BLUE = (0, 6, 32)

def normalize_alpha(alpha):
    return max(min(int(alpha), 255), 0)