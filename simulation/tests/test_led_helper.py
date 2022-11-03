#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of LED Helper"""

from nose2.tools import params
import _thread
from typing import Union
import unittest

# custom imports
from led_helper import Led
from led_helper import NeoPixel


class TestLed(unittest.TestCase):
    def setUp(self) -> None:
        self.led = Led()

    def tearDown(self) -> None:
        pass

    def test__init__(self) -> None:
        """Test initial values"""
        # check thread specific values
        # self.assertIsInstance(self.led._fade_lock, _thread.allocate_lock)
        self.assertEqual(self.led._inverted, True)
        self.assertEqual(self.led._blink_delay, 250)

    @unittest.skip("Not yet implemented")
    def flash(self) -> None:
        """Test flashing LED for given amount of iterations"""
        pass

    @unittest.skip("Not yet implemented")
    def test_blink(self) -> None:
        """Test blinking LED infinitely."""
        pass

    @unittest.skip("Not yet implemented")
    def test__blink(self) -> None:
        """Test internal blink thread content"""
        pass

    @unittest.skip("Not yet implemented")
    def test_blink_delay(self) -> None:
        """Test getting the blink delay in milliseconds."""
        pass

    @unittest.skip("Not yet implemented")
    def blink_delay(self) -> None:
        """Test setting the the blink delay in milliseconds."""
        pass

    @unittest.skip("Not yet implemented")
    def test_blinking(self) -> None:
        """Test getting the blinking status"""
        pass

    @unittest.skip("Not yet implemented")
    def test_toggle_pin(self) -> None:
        """Test toggle pin for given amount of iterations"""
        pass

    @unittest.skip("Not yet implemented")
    def test_turn_on(self) -> None:
        """Test turning LED on"""
        pass

    @unittest.skip("Not yet implemented")
    def test_on(self) -> None:
        """Test setting and getting state of LED"""
        pass

    @unittest.skip("Not yet implemented")
    def test_turn_off(self) -> None:
        """Test turning LED off"""
        pass

    @unittest.skip("Not yet implemented")
    def test_off(self) -> None:
        """Test setting and getting state of LED"""


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
