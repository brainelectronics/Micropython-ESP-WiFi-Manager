#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of LED Helper"""

from nose2.tools import params
import _thread
from typing import Union
import unittest

# custom imports
from led_helper import Neopixel
from led_helper import NeoPixel


class TestNeopixel(unittest.TestCase):
    def setUp(self) -> None:
        self.pixel = Neopixel()

    def tearDown(self) -> None:
        pass

    def test__init__(self) -> None:
        """Test initial values"""
        self.assertEqual(self.pixel._neopixel_amount, 1)
        self.assertIsInstance(self.pixel.pixel, NeoPixel)

        # check values of the pixel
        self.assertEqual(self.pixel._color, [30, 0, 0])
        self.assertEqual(self.pixel._intensity, 30)
        self.assertEqual(self.pixel._last_intensity, 30)
        self.assertEqual(self.pixel._active, False)

        # check thread specific values
        # self.assertIsInstance(self.pixel._fade_lock, _thread.allocate_lock)
        self.assertEqual(self.pixel._fade_delay, 50)
        self.assertEqual(self.pixel._fading, False)
        self.assertEqual(self.pixel._fade_pixel_amount, -1)

    @unittest.skip("Not yet implemented")
    def test_clear(self) -> None:
        """Test clearing Neopixel color"""
        pass

    @unittest.skip("Not yet implemented")
    def test_set(self) -> None:
        """Test setting Neopixel color"""
        pass

    @unittest.skip("Not yet implemented")
    def test_red(self) -> None:
        """Test setting Neopixel color to red"""
        pass

    @unittest.skip("Not yet implemented")
    def test_green(self) -> None:
        """Test setting Neopixel color to green"""
        pass

    @unittest.skip("Not yet implemented")
    def test_blue(self) -> None:
        """Test setting Neopixel color to blue"""
        pass

    @unittest.skip("Not yet implemented")
    def test_pixels(self) -> None:
        """Test getting number of Neopixels"""
        pass

    @unittest.skip("Not yet implemented")
    def test_color(self) -> None:
        """Test getting and setting the current Neopixel color"""
        pass

    @unittest.skip("Not yet implemented")
    def test_intensity(self) -> None:
        """Test getting and setting the current Neopixel intensity"""
        pass

    @unittest.skip("Not yet implemented")
    def test_active(self) -> None:
        """Test getting and setting the current Neopixel status"""
        pass

    @unittest.skip("Not yet implemented")
    def test_colors(self) -> None:
        """Test getting and setting the available Neopixel colors"""
        pass

    @unittest.skip("Not yet implemented")
    def test_fade(self) -> None:
        """Test fading the Neopixel"""
        pass

    @unittest.skip("Not yet implemented")
    def test__fade(self) -> None:
        """Test fade thread"""
        pass

    @unittest.skip("Not yet implemented")
    def test_fade_delay(self) -> None:
        """Test getting and setting the fade delay"""
        pass

    @unittest.skip("Not yet implemented")
    def test_fade_pixel_amount(self) -> None:
        """Test getting and setting the amount of faidng Neopixels"""
        pass

    @unittest.skip("Not yet implemented")
    def test_fading(self) -> None:
        """Test getting and setting the fading status"""
        pass


if __name__ == '__main__':
    unittest.main()
