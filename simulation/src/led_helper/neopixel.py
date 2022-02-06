#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Fake Micropython NeoPixel

See https://docs.micropython.org/en/latest/library/neopixel.html
"""

from machine import Pin


class NeoPixel(object):
    """docstring for NeoPixel"""
    def __init__(self, pin: Pin, n: int, bpp: int = 3, timing: int = 1):
        """
        Initialise NeoPixel

        :param      pin:    Pin of Neopixel LED
        :type       pin:    Pin
        :param      n:      Number of Neopixel LEDs
        :type       n:      int
        :param      bpp:    3 for RGB LEDs, 4 for RGBW LEDs
        :type       bpp:    int, optional
        :param      timing: 0 for 400KHz, and 1 for 800kHz LEDs
        :type       timing: int, optional
        """
        self._pin = pin
        self._amount = n

    def fill(self, pixel) -> None:
        for _ in range(0, self.__len__()):
            pass

    def __len__(self) -> int:
        return self._amount

    def __setitem__(self, index, value) -> None:
        setattr(self, str(index), value)

    def __getitem__(self, index):
        return getattr(self, index)

    def write(self) -> None:
        pass
