#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Fake Micropython Pin class

See https://docs.micropython.org/en/latest/library/machine.Pin.html
"""
from typing import Optional, Union


class Pin(object):
    """docstring for Pin"""
    IN = 1
    OUT = 2

    def __init__(self, pin: int, mode: int):
        self._pin = pin
        self._mode = mode
        self._value = False

    def value(self, val: Optional[Union[int, bool]] = None) -> Optional[bool]:
        """
        Set or get the value of the pin

        :param      val:  The value
        :type       val:  Optional[Union[int, bool]]

        :returns:   State of the pin if no value specifed, None otherwise
        :rtype:     Optional[bool]
        """
        if val is not None and self._mode == Pin.OUT:
            # set pin state
            self._value = bool(val)
        else:
            # get pin state
            return self._value

    def on(self) -> None:
        """Set pin to "1" output level"""
        if self._mode == Pin.OUT:
            self.value(val=True)

    def off(self) -> None:
        """Set pin to "0" output level"""
        if self._mode == Pin.OUT:
            self.value(val=False)
