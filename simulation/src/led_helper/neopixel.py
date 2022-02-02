#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


class NeoPixel(object):
    """docstring for NeoPixel"""
    def __init__(self, pin, n: int):
        pass
        # self.list = list()

    def __setitem__(self, key, value):
        setattr(self, str(key), value)

    def __getitem__(self, key):
        return getattr(self, key)

    def write(self):
        pass
