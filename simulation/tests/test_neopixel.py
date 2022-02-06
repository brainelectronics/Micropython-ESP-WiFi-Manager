#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of NeoPixel"""

from nose2.tools import params
import unittest

# custom imports
from led_helper import NeoPixel
from machine import Pin


class TestNeoPixel(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test__init__(self) -> None:
        """Test __init__ function"""
        pixel_pin = Pin(12, Pin.OUT)

        pixel = NeoPixel(pin=pixel_pin, n=34)

        self.assertIsInstance(pixel._pin, Pin)
        self.assertEqual(pixel._amount, 34)

    @unittest.skip("Not yet implemented")
    @params(
        (None),
        ('Sauerkraut')
    )
    def test_fill(self, pixel) -> None:
        """Test setting the value of all pixels to the pixel value"""
        pass

    def test__len__(self) -> None:
        """Test getting the number of LEDs"""
        pixel_pin = Pin(32, Pin.OUT)

        pixels = 42
        pixel = NeoPixel(pin=pixel_pin, n=pixels)

        amount_of_pixels = len(pixel)
        self.assertEqual(amount_of_pixels, pixels)

    @unittest.skip("Not yet implemented")
    def test_write(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
