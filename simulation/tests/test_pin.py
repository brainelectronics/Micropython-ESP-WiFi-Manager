#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of Machine Pin"""

import unittest

# custom imports
from machine import Pin


class TestPin(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test__init__(self) -> None:
        pin = Pin(pin=12, mode=Pin.IN)

        self.assertEqual(pin._pin, 12)
        self.assertEqual(pin._mode, 1)

        pin = Pin(pin=34, mode=Pin.OUT)

        self.assertEqual(pin._pin, 34)
        self.assertEqual(pin._mode, 2)


if __name__ == '__main__':
    unittest.main()
