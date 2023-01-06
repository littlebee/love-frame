"""

"""
import sys
import time
import threading

from rpi_ws281x import PixelStrip, ws, Color


BPM_NORMAL = 60
BPM_SLEEPING = 40
BPM_EXCITED = 110

DARKEST_ADJ_COLOR =  (0, 6, 32)

NEW_MESSAGE_COLOR = (16, 232, 139, 0)


LED_COUNT = 37      # Number of LED pixels.
LED_PIN = 12      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# this is the strip type for the 60/M RGBW from adafruit
LED_STRIP = ws.SK6812_STRIP_RGBW

MIN_COLOR_VALUE = 10


strip = None
# this is a FIFO queue of commands to run
queue = []
current_color = None
last_requested_color = None
thread_should_stop = False

def init_leds():
    thread = threading.Thread(target=_thread)
    thread.start()


def quit():
    global thread_should_stop
    thread_should_stop = True


def normalize(cc):
    return int(max(0, min(255, cc)))


def adjustColor(rgb):
    (r, g, b) = rgb
    if r < MIN_COLOR_VALUE and g < MIN_COLOR_VALUE and b < MIN_COLOR_VALUE:
        (r, g, b) = DARKEST_ADJ_COLOR

    # the red element in the 5050 RGB neopixels in combo with the PLA
    # is too intense.  tamp down red a little to compensate
    if r > 50:
        r = r * .8
    if b > 50:
        b = b * .9

    print(f"adjusted color {rgb} - {r}, {g}, {b}")
    return (normalize(r), normalize(g), normalize(b))


def fill(rgb, white=0, adjust=True):
    global queue
    global last_requested_color
    (r, g, b) = adjustColor(rgb) if adjust else rgb
    last_requested_color = (r, g, b)
    queue.append([_fill, (r, g, b, white)])


def fade_to(rgb, white=0, adjust=True, steps=10, duration=.1):
    global queue
    global last_requested_color
    (r, g, b) = adjustColor(rgb) if adjust else rgb
    last_requested_color = (r, g, b)
    queue.append([_fade_to, [(r, g, b, white), steps, duration]])


def new_message():
    global queue
    queue.append([_new_message, []])


def bright_white():
    fill((255, 255, 255), white=255)

# internal use only below


def _init_strip():
    global strip

    strip = PixelStrip(
        LED_COUNT,
        LED_PIN,
        LED_FREQ_HZ,
        LED_DMA,
        LED_INVERT,
        LED_BRIGHTNESS,
        LED_CHANNEL,
        LED_STRIP
    )
    print(f"Initializing LEDs")
    strip.begin()



def _thread():
    global queue
    global strip

    _init_strip()

    while not thread_should_stop:
        while len(queue) > 0:
            [fn, data] = queue.pop(0)
            fn(data)
        time.sleep(.1)



def _fill(rgbw):
    global current_color
    global strip
    [r, g, b, w] = rgbw
    c = Color(g, r, b, w)

    for i in range(strip.numPixels()):
        strip.setPixelColor(i, c)
        strip.show()

    current_color = rgbw


# fade from current color to rgb

def _fade_to(args):
    global current_color
    global strip

    [rgbw, steps, duration] = args

    if current_color == None:
        _fill(rgb)

    (r1, g1, b1, w1) = current_color
    (r2, g2, b2, w2) = rgbw
    r_inc = (r1 - r2) / steps
    g_inc = (g1 - g2) / steps
    b_inc = (b1 - b2) / steps
    w_inc = (w1 - w2) / steps

    if abs(r_inc) + abs(g_inc) + abs(b_inc) <= 0:
        return;

    r = r1
    g = g1
    b = b1
    w = w1

    for i in range(steps):
        r -= r_inc
        g -= g_inc
        b -= b_inc
        w -= w_inc
        _fill((int(r), int(g), int(b), int(w)))
        time.sleep(duration / steps)


    _fill(rgbw)
    current_color = rgbw


def _new_message(_args):
    global current_color

    band_width = 24
    laps = 1

    for r in range(laps):
        for i in range(LED_COUNT + 1):
            time.sleep(.01)
            for j in range (band_width):
                if i + j < LED_COUNT:
                    strip.setPixelColor(i+j, Color(*NEW_MESSAGE_COLOR))
            strip.show()
            (r, g, b) = last_requested_color
            strip.setPixelColor(i, Color(g, r, b))


if __name__ == '__main__':

    _init_strip()
    sSleep = 3

    while 1:
        print('red fill')
        _fill((255, 0, 0, 0))
        time.sleep(sSleep)
        print('green fill')
        _fill((0, 255, 0, 0))
        time.sleep(sSleep)
        print('blue fill')
        _fill((0, 0, 255, 0))
        time.sleep(sSleep)
        print('white fill')
        _fill((255, 255, 255, 0))
        time.sleep(sSleep)
        print('extra white fill')
        _fill((255, 255, 255, 255))
        time.sleep(sSleep)


