#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Fake Micropython Pin class

See https://docs.micropython.org/en/latest/library/machine.Pin.html
"""


class Pin(object):
    """docstring for Pin"""
    IN = 1
    OUT = 2

    def __init__(self, pin: int, mode: int):
        self._pin = pin
        self._mode = mode
