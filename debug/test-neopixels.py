#!/usr/bin/env python3
"""

"""
import board
import neopixel
import time


pixels = neopixel.NeoPixel(board.D18, 2) #, pixel_order=neopixel.RGBW)
pixels.fill((0, 255, 128))
time.sleep(10)