#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of LED Helper"""

from datetime import datetime
from io import StringIO
import math
from nose2.tools import params
from random import randint, randrange
import _thread
import time
import unittest
from unittest.mock import patch

# custom imports
from led_helper import Led
from led_helper import Neopixel
from led_helper import NeoPixel
from machine import Pin


class TestLed(unittest.TestCase):
    def setUp(self) -> None:
        self.led = Led(led_pin=4, inverted=False)
        self.assertEqual(self.led.state, False)

    def tearDown(self) -> None:
        pass

    def test__init__(self) -> None:
        """Test initial values"""
        self.assertIsInstance(self.led.led_pin, Pin)
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
        time.sleep(0.1)     # thread might not start immediately
        self.assertTrue(self.led.blinking)
        time.sleep(blink_time)

        self.led.blinking = False
        self.assertFalse(self.led.blinking)

        # expected call of pin.value() function is two times of blink amount
        # 1. get current LED pin state
        # 2. set new inverted LED pin state
        expected_call_count = math.ceil((blink_time * 1000) / delay_ms) * 2
        self.assertGreaterEqual(mocked_pin_value.call_count,
                                expected_call_count)

    @patch('machine.pin.Pin.value')
    def test__blink(self, mocked_pin_value: unittest.mock.MagicMock) -> None:
        """Test internal blink thread content"""
        delay_ms = randrange(10, 100, 10)
        blink_time = 1.0    # second
        blink_lock = _thread.allocate_lock()

        blink_lock.acquire()
        params = (delay_ms, blink_lock)
        _thread.start_new_thread(self.led._blink, params)

        time.sleep(0.1)     # thread might not start immediately
        self.assertTrue(blink_lock.locked())
        time.sleep(blink_time)

        # terminate thread
        blink_lock.release()
        time.sleep(0.1)
        self.assertFalse(blink_lock.locked())

        # expected call of pin.value() function is two times of blink amount
        # 1. get current LED pin state
        # 2. set new inverted LED pin state
        # +1 due to "turn_off" call after leaving the while loop
        expected_call_count = math.ceil((blink_time * 1000) / delay_ms) * 2 + 1
        self.assertGreaterEqual(mocked_pin_value.call_count,
                                expected_call_count)

        # start thread without acquired locking
        _thread.start_new_thread(self.led._blink, params)

        time.sleep(blink_time)

        self.assertFalse(blink_lock.locked())

        # expected call of pin.value() function is one
        # 1. due to "turn_off" call after leaving the while loop
        expected_call_count = 1
        self.assertGreaterEqual(mocked_pin_value.call_count,
                                expected_call_count)

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
        self.pixel = Neopixel(neopixel_pin=27, neopixels=1)

    def tearDown(self) -> None:
        pass

    def test__init__(self) -> None:
        """Test initial values"""
        self.assertEqual(self.pixel._neopixel_amount, 1)
        self.assertIsInstance(self.pixel.pixel, NeoPixel)

        self.assertEqual(
            self.pixel._colors,
            {
                'red': [30, 0, 0],
                'green': [0, 30, 0],
                'blue': [0, 0, 30],
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
        )

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

    @patch('led_helper.led_helper.Neopixel.set')
    def test_clear(self, mocked_neopixel_set: unittest.mock.MagicMock) -> None:
        """Test clearing Neopixel color"""
        self.pixel.clear(number=3)
        mocked_neopixel_set.assert_called_once_with(rgb=[0, 0, 0], number=3)

    @unittest.skip("Not yet implemented")
    def test_set(self) -> None:
        """Test setting Neopixel color"""
        pass

    @patch('led_helper.led_helper.Neopixel.set')
    def test_red(self, mocked_neopixel_set: unittest.mock.MagicMock) -> None:
        """Test setting Neopixel color to red"""
        self.pixel.green(intensity=40, number=2)
        mocked_neopixel_set.assert_called_once_with(green=40, number=2)

    @patch('led_helper.led_helper.Neopixel.set')
    def test_green(self, mocked_neopixel_set: unittest.mock.MagicMock) -> None:
        """Test setting Neopixel color to green"""
        self.pixel.green(intensity=50, number=3)
        mocked_neopixel_set.assert_called_once_with(green=50, number=3)

    @patch('led_helper.led_helper.Neopixel.set')
    def test_blue(self, mocked_neopixel_set: unittest.mock.MagicMock) -> None:
        """Test setting Neopixel color to blue"""
        self.pixel.blue(intensity=60, number=4)
        mocked_neopixel_set.assert_called_once_with(blue=60, number=4)

    def test_pixels(self) -> None:
        """Test getting number of Neopixels"""
        self.assertEqual(self.pixel.pixels, 1)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('led_helper.led_helper.Neopixel.clear')
    def test_color(self,
                   mocked_clear: unittest.mock.MagicMock,
                   mock_stdout: StringIO) -> None:
        """Test getting and setting the current Neopixel color"""
        self.assertEqual(self.pixel.color, [30, 0, 0])

        # set color as string value
        self.pixel.color = 'blue'
        self.assertEqual(self.pixel.color, [0, 0, 30])

        # set undefined color by string value
        undefined_color = 'grey'
        self.pixel.color = undefined_color
        self.assertIn('Color "{}" unknown, may add it with "colors" function'.
                      format(undefined_color),
                      mock_stdout.getvalue())
        # color should not be changed
        self.assertEqual(self.pixel.color, [0, 0, 30])

        # set color as list of int
        self.pixel.color = [0, 30, 0]
        self.assertEqual(self.pixel.color, [0, 30, 0])

        # turn Neopixel off
        self.pixel.color = [0, 0, 0]
        self.assertEqual(self.pixel.color, [0, 0, 0])
        self.assertEqual(mocked_clear.call_count, 1)

    def test_intensity(self) -> None:
        """Test getting and setting the current Neopixel intensity"""
        self.pixel.active = True    # pixel must be active to change intensity
        self.assertTrue(self.pixel.active)
        self.assertEqual(self.pixel.color, [30, 0, 0])

        new_intensity = 100

        with patch('led_helper.led_helper.Neopixel.set') as mocked_set:
            self.pixel.intensity = new_intensity
            self.assertEqual(self.pixel._last_intensity, new_intensity)
            mocked_set.assert_called_once_with(rgb=[100, 0, 0], number=-1)

        # test turning pixel off via intensity settings
        new_intensity = 0

        with patch('led_helper.led_helper.Neopixel.clear') as mocked_clear:
            self.pixel.intensity = new_intensity
            self.assertEqual(self.pixel._last_intensity, new_intensity)
            mocked_clear.assert_called_once_with(number=-1)

    @patch('led_helper.led_helper.Neopixel.set')
    @patch('led_helper.led_helper.Neopixel.clear')
    def test_active(self,
                    mocked_clear: unittest.mock.MagicMock,
                    mocked_set: unittest.mock.MagicMock) -> None:
        """Test getting and setting the current Neopixel status"""
        current_pixel_state = self.pixel.active
        current_pixel_color = self.pixel.color
        self.assertFalse(current_pixel_state)

        # disable pixel again
        self.pixel.active = False
        self.assertFalse(self.pixel.active)

        # enable pixel
        self.pixel.active = True
        self.assertTrue(self.pixel.active)
        mocked_set.assert_called_once_with(rgb=current_pixel_color, number=-1)

        # disable pixel
        self.pixel.active = False
        self.assertFalse(self.pixel.active)
        mocked_clear.assert_called_once_with(number=-1)

    def test_colors(self) -> None:
        """Test getting and setting the available Neopixel colors"""
        default_colors = {
            'red': [30, 0, 0],
            'green': [0, 30, 0],
            'blue': [0, 0, 30],
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
        default_colors_number = 13
        self.assertIsInstance(self.pixel.colors, dict)
        self.assertEqual(len(self.pixel.colors), default_colors_number)
        self.assertEqual(self.pixel.colors, default_colors)

        # update colors with already existing color
        updated_color = {'red': [10, 0, 0]}
        default_colors.update(updated_color)
        self.pixel.colors = updated_color

        self.assertIsInstance(self.pixel.colors, dict)
        self.assertEqual(len(self.pixel.colors), default_colors_number)
        self.assertEqual(self.pixel.colors, default_colors)

        # add new color
        new_color = {'black': [0, 0, 0]}
        default_colors.update(new_color)
        self.pixel.colors = new_color

        self.assertIsInstance(self.pixel.colors, dict)
        self.assertEqual(len(self.pixel.colors), default_colors_number + 1)
        self.assertEqual(self.pixel.colors, default_colors)

    @unittest.skip("Not yet implemented")
    def test_fade(self) -> None:
        """Test fading the Neopixel"""
        pass

    @unittest.skip("Not yet implemented")
    def test__fade(self) -> None:
        """Test fade thread"""
        pass

    @params(
        (-10),
        (0),
        (1),
        (123),
    )
    def test_fade_delay(self, value: int) -> None:
        """
        Test getting and setting the fade delay

        :param      value:  The value
        :type       value:  int
        """
        pass

        default_fade_delay = self.pixel.fade_delay
        self.assertEqual(default_fade_delay, 50)

        # set and get new blink delay
        self.pixel.fade_delay = value
        fade_delay = self.pixel.fade_delay

        if value > 1:
            self.assertEqual(fade_delay, value)
        else:
            self.assertEqual(fade_delay, 1)

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
