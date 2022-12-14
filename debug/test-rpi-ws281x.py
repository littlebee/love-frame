#!/usr/bin/env python3
import time

from rpi_ws281x import PixelStrip

LED_COUNT = 30     # Number of LED pixels.
LED_PIN = 12      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


strip = PixelStrip(
    LED_COUNT,
    LED_PIN,
    LED_FREQ_HZ,
    LED_DMA,
    LED_INVERT,
    LED_BRIGHTNESS,
    LED_CHANNEL
)
strip.begin()

def fill(r, g, b):
    for i in range(strip.numPixels()):
        strip.setPixelColorRGB(i, r, g, b, 255)
    strip.show()

while True:
    fill(255, 0, 0)
    time.sleep(1)
    fill(0, 255, 0)
    time.sleep(1)
    fill(0, 0, 255)
    time.sleep(1)
    fill(255, 255, 255)
    time.sleep(1)
    fill(0, 0, 0)
    time.sleep(1)
