#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Mock LED operations of a Micropython board"""

from . import neopixel
from machine import Pin
import _thread
import time

from typing import Union


class Neopixel(object):
    """docstring for Neopixel"""
    def __init__(self, neopixel_pin: int = 27, neopixels: int = 1) -> None:
        """
        Initialize Neopixel.

        Default Neopixel color is red with intensity of 30/255

        :param      neopixel_pin:   Pin of Neopixel LED
        :type       neopixel_pin:   int, optional
        :param      neopixels:      Number of Neopixel LEDs
        :type       neopixels:      int, optional
        """
        neopixel_pin = Pin(neopixel_pin, Pin.OUT)
        self._neopixel_amount = neopixels
        self.pixel = neopixel.NeoPixel(pin=neopixel_pin, n=neopixels)

        # 30/255 as default intensity to aviod getting blinded by the lights
        self._colors = {
            'red': [30, 0, 0],
            'green': [0, 30, 0],
            'blue': [0, 0, 30],
            # other colors may need adjustment as they are just technically
            # correct, but maybe not colorwise
            'yellow': [30, 30, 0],
            'cyan': [0, 30, 30],
            'magenta': [30, 0, 30],
            'white': [30, 30, 30],
            'maroon': [30 // 2, 0, 0],
            'darkgreen': [0, 30 // 2, 0],
            'darkblue': [0, 0, 30 // 2],
            'olive': [30 // 2, 30 // 2, 0],
            'teal': [0, 30 // 2, 30 // 2],
            'purple': [30 // 2, 0, 30 // 2],
        }
        self._pwmtable = [0, 1, 2, 2, 2, 3, 3, 4, 5, 6, 7, 8, 10, 11, 13, 16, 19, 23, 27, 32, 38, 45, 54, 64, 76, 91, 108, 128, 152, 181, 215, 255]
        self._color = self._colors['red']
        self._intensity = max(self._color)
        self._last_intensity = self._intensity
        self._active = False

        # fade specific defines
        self._fade_lock = _thread.allocate_lock()
        self._fade_delay = 50
        self._fading = False
        self._fade_pixel_amount = -1    # fade all by default

    def clear(self, number: int = -1) -> None:
        """
        Turn Neopixel off by setting the RGB color to [0, 0, 0]

        :param      number:     Neopixel number to clear, all by default
        :type       number:     int, optional
        """
        self.set(rgb=[0, 0, 0], number=number)

    def set(self,
            red: int = 0,
            green: int = 0,
            blue: int = 0,
            rgb: list = None,
            number: Union[int, list] = -1) -> None:
        """
        Set the neopixel color.

        A RGB value can be specified by a list or by setting the individual color.

        :param      red:    The red brightness
        :type       red:    int, optional
        :param      green:  The green brightness
        :type       green:  int, optional
        :param      blue:   The blue brightness
        :type       blue:   int, optional
        :param      rgb:    The RGB value
        :type       rgb:    list, optional
        :param      number: Number/list of Neopixels to change, -1 changes all
        :type       number: Union[int, list], optional
        """
        if rgb is None:
            color = (red, green, blue)
        else:
            color = tuple(rgb)

        if number == -1:
            # update all Neopixels
            for p in range(0, self._neopixel_amount):
                self.pixel[p] = color
        else:
            # update only specific Neopixels
            if isinstance(number, list):
                for p in number:
                    self.pixel[number] = color
            else:
                self.pixel[number] = color

        self.pixel.write()

        # update neopixel properties
        if color != (0, 0, 0):
            self.active = True
            if not self.fading:
                # only update if not called by fading
                # intensity would finally be 1 or zero
                self.color = list(color)
                self.intensity = max(color)
        else:
            # only update if not called by fading
            # neopixel would be cleared after every cycle
            if not self.fading:
                self.active = False
                # do not clear color or intensity property

    def red(self, intensity: int = 30, number: Union[int, list] = -1) -> None:
        """
        Set the Neopixel to red.

        :param      intensity:  The intensity
        :type       intensity:  int, optional
        :param      number:     Neopixel number/list to change, all by default
        :type       number:     Union[int, list], optional
        """
        self.set(red=intensity, number=number)

    def green(self, intensity: int = 30, number: Union[int, list] = -1) -> None:
        """
        Set the Neopixel to green.

        :param      intensity:  The intensity
        :type       intensity:  int, optional
        :param      number:     Neopixel number/list to change, all by default
        :type       number:     Union[int, list], optional
        """
        self.set(green=intensity, number=number)

    def blue(self, intensity: int = 30, number: Union[int, list] = -1) -> None:
        """
        Set the Neopixel to blue.

        :param      intensity:  The intensity
        :type       intensity:  int, optional
        :param      number:     Neopixel number/list to change, all by default
        :type       number:     Union[int, list], optional
        """
        self.set(blue=intensity, number=number)

    @property
    def pixels(self) -> int:
        """
        Get number of defined Neopixels

        :returns:   Amount of Neopixels
        :rtype:     int
        """
        return self._neopixel_amount

    @property
    def color(self) -> list:
        """
        Get the currently set color of the Neopixel, might not be active

        :returns:   Neopixel color if active
        :rtype:     list
        """
        return self._color

    @color.setter
    def color(self, color: Union[list, str]) -> None:
        """
        Set a Neopixel color. Neopixel will be activated.

        :param      color:      The color
        :type       color:      Union[list, str]
        """
        if isinstance(color, str):
            if color in self.colors:
                color = self.colors[color]
            else:
                print('Color "{}" unknown, may add it with "colors" function'.
                      format(color))
                return

        if color != self.color:
            self._color = color

            if color != [0, 0, 0]:
                self.set(rgb=color, number=-1)
            else:
                self.clear()

    @property
    def intensity(self) -> int:
        """
        Get current Neopixel intensity.

        :returns:   Neopixel intensity, maximum 255
        :rtype:     int
        """
        return self._intensity

    @intensity.setter
    def intensity(self, value: int) -> None:
        """
        Set new intensity for Neopixel.

        If Neopixel is active and is showing a color, the new intensity will
        be applied.

        :param      value:  The intensity, value will be
        :type       value:  int
        """
        do_update = False
        self._last_intensity = value

        # update neopixel if new intensity is different from current one and
        # the Neopixel is currently active
        if ((self.intensity != self._last_intensity) and self.active):
            # apply new intensity only if a valid color is set
            if self.color != [0, 0, 0]:
                do_update = True

        if not value:
            self.clear(number=-1)   # disable all Neopixel by default
            do_update = False

        value = max(min(255, value), 0)
        self._intensity = value

        if do_update:
            # intensity = 40
            # color = [60, 10, 7]
            # maximum_brightness = max(color) # 60
            # ratio = maximum_brightness / intensity  # 1.5
            # new_color = [round(ele / ratio) for ele in color]
            #  -> [40, 7, 5]
            ratio = max(self.color) / value
            new_color = [round(ele / ratio) for ele in self.color]
            self.set(rgb=new_color, number=-1)  # update all Neopixel

    @property
    def active(self) -> bool:
        """
        Get current status of Neopixel

        :returns:   Flag whether Neopixel is active or not
        :rtype:     bool
        """
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        """
        Turn all Neopixel on or off

        :param      value:  The state
        :type       value:  bool
        """
        if value != self.active:
            self._active = value

            if value:
                self.set(rgb=self.color, number=-1)     # activate all Neopixel
            else:
                self.clear(number=-1)   # disable all Neopixel by default

    @property
    def colors(self) -> dict:
        """
        Get available colors of Neopixel.

        :returns:   Neopixel colors and their RGB value
        :rtype:     dict
        """
        return self._colors

    @colors.setter
    def colors(self, value: dict) -> None:
        """
        Add new colors or change RGB value of existing color

        :param      value:  Color name as key and RGB intensity list as value
        :type       value:  dict
        """
        self._colors.update(value)

    def fade(self, delay_ms: int = 50, pixel_amount: int = -1) -> None:
        """
        Fade Neopixel color. Wrapper around property usage.

        All defined Neopixels will be fading with the same color
        A fade delay below 30ms is not recommened due to high CPU load.
        REPL might get slow.

        :param      delay_ms:       The delay between intensity changes in milliseconds
        :type       delay_ms:       int
        :param      pixel_amount:   Which or how many Neopixel to fade, default is all
        :type       pixel_amount:   int, optional
        """
        self.fade_delay = delay_ms
        self.fade_pixel_amount = pixel_amount
        self.fading = True

    def _fade(self, delay_ms: int, pixel_amount: int, lock: int) -> None:
        """
        Internal Neopixel fading thread content.

        :param      delay_ms:       The delay between intensity changes in milliseconds
        :type       delay_ms:       int
        :param      pixel_amount:   Which or how many Neopixel to fade, default is all
        :type       pixel_amount:   int, optional
        :param      lock:           The lock object
        :type       lock:           lock
        """
        # find smallest value which is not zero in latest color list
        maximum_intensity = min([val for val in self.color if val != 0])

        # find closest match of maximum_intensity in _pwmtable
        # set this as maximum_intensity
        closest_match = min(self._pwmtable, key=lambda x: abs(x - maximum_intensity))
        closest_match_index = self._pwmtable.index(closest_match)

        while lock.locked():
            try:
                for val in self._pwmtable[:closest_match_index]:
                    color = [val if ele != 0 else 0 for ele in self.color]
                    self.set(rgb=color, number=pixel_amount)
                    # time.sleep_ms(delay_ms)
                    time.sleep(delay_ms / 1000.0)

                for val in self._pwmtable[:closest_match_index][::-1]:
                    color = [val if ele != 0 else 0 for ele in self.color]
                    self.set(rgb=color, number=pixel_amount)
                    # time.sleep_ms(delay_ms)
                    time.sleep(delay_ms / 1000.0)
            except KeyboardInterrupt:
                break

        # turn LED finally off
        self.active = False
        self._fading = False

    @property
    def fade_delay(self) -> int:
        """
        Get the fade delay in milliseconds.

        :returns:   Delay between intensity changes in milliseconds
        :rtype:     int
        """
        return self._fade_delay

    @fade_delay.setter
    def fade_delay(self, delay_ms: int) -> None:
        """
        Set the Neopixel fade delay in milliseconds.

        :param      delay_ms:  The delay between intensity changes in milliseconds
        :type       delay_ms:  int
        """
        if delay_ms < 1:
            delay_ms = 1
        self._fade_delay = delay_ms

    @property
    def fade_pixel_amount(self) -> int:
        """
        Get amount of fading Neopixels

        :returns:   Number of fading pixels
        :rtype:     int
        """
        return self._fade_pixel_amount

    @fade_pixel_amount.setter
    def fade_pixel_amount(self, value: int) -> None:
        """
        Set amount of fading Neopixels

        :param      value:  The amount of fading Neopixels
        :type       value:  int
        """
        if value > 0:
            value -= 1
        self._fade_pixel_amount = value

    @property
    def fading(self) -> bool:
        """
        Get the fading status.

        :returns:   Flag whether neopixel is fading or not
        :rtype:     bool
        """
        # returning self._fade_lock.locked() is not sufficient, as it will be
        # False after "fading = False" is called and the remaining
        # "set" calls would change the color and intensity property
        # values until the for loop of "_fade" is finished
        return self._fading

    @fading.setter
    def fading(self, value: bool) -> None:
        """
        Start or stop fading of the Neopixel.

        :param      value:  The value
        :type       value:  bool
        """
        if value and (not self._fade_lock.locked()):
            # start blinking if not already blinking
            self._fade_lock.acquire()
            self.active = True
            self._fading = True
            params = (self.fade_delay, self.fade_pixel_amount, self._fade_lock)
            _thread.start_new_thread(self._fade, params)
        elif (value is False) and self._fade_lock.locked():
            # stop fading if not already stopped
            self._fade_lock.release()
