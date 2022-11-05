#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of LED Helper"""

from datetime import datetime
import math
from nose2.tools import params
from random import randint, randrange
import time
import unittest
from unittest.mock import patch

# custom imports
from led_helper import Led
from led_helper import Neopixel
from led_helper import NeoPixel


class TestLed(unittest.TestCase):
    def setUp(self) -> None:
        self.led = Led(led_pin=4, inverted=False)
        self.assertEqual(self.led.state, False)

    def tearDown(self) -> None:
        pass

    def test__init__(self) -> None:
        """Test initial values"""
        # check thread specific values
        # self.assertIsInstance(self.led._fade_lock, _thread.allocate_lock)
        self.assertEqual(self.led._inverted, False)
        self.assertEqual(self.led._blink_delay, 250)

    @patch('machine.pin.Pin.value')
    def test_flash(self, mocked_pin_value: unittest.mock.MagicMock) -> None:
        """Test flashing LED for given amount of iterations"""
        toggle_amount = randint(1, 10)
        delay_ms = randint(1, 100)

        tick = datetime.now()

        # it is a static method
        self.led.flash(amount=toggle_amount, delay_ms=delay_ms)

        tock = datetime.now()

        # expected call of pin.value() function is four times of the toggle
        # amount
        # 1. get the current state
        # 2. set it to the collected state
        # 3. get the pin stage again after waiting for some time
        # 4. set it to the new collected state
        expected_call_count = toggle_amount * 4
        self.assertGreaterEqual(mocked_pin_value.call_count,
                                expected_call_count)

        self.assertGreaterEqual((tock - tick).total_seconds(),
                                (delay_ms / 1000.0) * toggle_amount * 2)

    @patch('machine.pin.Pin.value')
    def test_blink(self, mocked_pin_value: unittest.mock.MagicMock) -> None:
        """Test blinking LED infinitely."""
        delay_ms = randrange(10, 100, 10)
        blink_time = 1.0    # second

        # it is a static method
        self.led.blink(delay_ms=delay_ms)
        self.assertTrue(self.led.blinking)
        time.sleep(blink_time)

        self.led.blinking = False
        self.assertFalse(self.led.blinking)

        # expected call of pin.value() function is two times of blink amount
        # 1. get current LED pin state
        # 2. set new inverted LED pin state
        expected_call_count = math.ceil((blink_time * 1000) / delay_ms) * 2
        print('delay_ms: {}'.format(delay_ms))
        print('expected_call_count: {}'.format(expected_call_count))

        self.assertEqual(mocked_pin_value.call_count, expected_call_count)

    @unittest.skip("Checked by test_blink")
    def test__blink(self) -> None:
        """Test internal blink thread content"""
        pass

    @params(
        (-10),
        (0),
        (1),
        (123),
    )
    def test_blink_delay(self, value: int) -> None:
        """
        Test getting the blink delay in milliseconds.

        :param      value:  The value
        :type       value:  int
        """
        default_blink_delay = self.led.blink_delay
        self.assertEqual(default_blink_delay, 250)

        # set and get new blink delay
        self.led.blink_delay = value
        blink_delay = self.led.blink_delay

        if value > 1:
            self.assertEqual(blink_delay, value)
        else:
            self.assertEqual(blink_delay, 1)

    @unittest.skip("Checked by test_blink")
    def test_blinking(self) -> None:
        """Test getting the blinking status"""
        pass

    @unittest.skip("Checked by test_flash")
    def test_toggle_pin(self) -> None:
        """Test toggle pin for given amount of iterations"""
        pass

    def test_state(self) -> None:
        """Test LED state"""
        # default pin state is off
        led = Led(led_pin=4, inverted=False)
        self.assertEqual(led.state, False)

        led.state = True
        self.assertEqual(led.state, True)
        self.assertEqual(led.led_pin.value(), True)

        led.state = False
        self.assertEqual(led.state, False)
        self.assertEqual(led.led_pin.value(), False)

        inverted_led = Led(inverted=True)
        self.assertEqual(inverted_led.state, True)
        self.assertEqual(inverted_led.led_pin.value(), False)

        inverted_led.state = True
        self.assertEqual(inverted_led.state, True)
        self.assertEqual(inverted_led.led_pin.value(), False)

        inverted_led.state = False
        self.assertEqual(inverted_led.state, False)
        self.assertEqual(inverted_led.led_pin.value(), True)

    def test_turn_on(self) -> None:
        """Test turning LED on"""
        # default pin state is off
        led = Led(led_pin=4, inverted=False)
        self.assertEqual(led.state, False)
        self.assertEqual(led.led_pin.value(), False)

        led.turn_on()
        self.assertEqual(led.state, True)
        self.assertEqual(led.led_pin.value(), True)
        self.assertEqual(led.on, True)

        inverted_led = Led(inverted=True)
        self.assertEqual(inverted_led.state, True)
        self.assertEqual(inverted_led.led_pin.value(), False)

        inverted_led.turn_on()
        self.assertEqual(inverted_led.state, True)
        self.assertEqual(inverted_led.led_pin.value(), False)
        self.assertEqual(inverted_led.on, True)

    @unittest.skip("Checked by test_turn_on")
    def test_on(self) -> None:
        """Test setting and getting state of LED"""
        pass

    def test_turn_off(self) -> None:
        """Test turning LED off"""
        # default pin state is off
        led = Led(led_pin=4, inverted=False)
        self.assertEqual(led.state, False)
        self.assertEqual(led.led_pin.value(), False)

        led.turn_off()
        self.assertEqual(led.state, False)
        self.assertEqual(led.led_pin.value(), False)
        self.assertEqual(led.off, True)

        inverted_led = Led(inverted=True)
        self.assertEqual(inverted_led.state, True)
        self.assertEqual(inverted_led.led_pin.value(), False)

        inverted_led.turn_off()
        self.assertEqual(inverted_led.state, False)
        self.assertEqual(inverted_led.led_pin.value(), True)
        self.assertEqual(inverted_led.off, True)

    @unittest.skip("Checked by test_turn_off")
    def test_off(self) -> None:
        """Test setting and getting state of LED"""
        pass


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
