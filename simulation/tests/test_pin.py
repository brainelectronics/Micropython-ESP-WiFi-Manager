#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of Machine Pin"""

from nose2.tools import params
import unittest

from typing import Any

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
        self.assertEqual(pin._value, 0)

        pin = Pin(pin=34, mode=Pin.OUT)

        self.assertEqual(pin._pin, 34)
        self.assertEqual(pin._mode, 2)
        self.assertEqual(pin._value, 0)

    @params(
        (None, False),  # new pin state, expectation
        (True, True),
        (False, False),
        (1, True),
        (0, False),
        ('asdf', True),
        ('', False),
    )
    def test_value_output_pin(self, new_state: Any, expectation: bool) -> None:
        """
        Test setting and getting the output pin state

        :param      new_state:      New desired pin state
        :type       new_state:      Any
        :param      expectation:    Expected pin state after change
        :type       expectation:    bool
        """
        pin = Pin(pin=12, mode=Pin.OUT)

        # set new pin state
        pin.value(new_state)
        self.assertEqual(pin.value(), expectation)

    @params(
        (None),
        (True),
        (False),
        (1),
        (0),
        ('asdf'),
        (''),
    )
    def test_value_input_pin(self, new_state: Any) -> None:
        """
        Test setting and getting the input pin state

        :param      new_state:  New desired pin state
        :type       new_state:      Any
        """
        pin = Pin(pin=12, mode=Pin.IN)

        # check default pin state
        self.assertEqual(pin.value(), False)

        # set new pin state
        pin.value(new_state)
        self.assertEqual(pin.value(), False)

    def test_on_off(self) -> None:
        """Test setting pin to "0" or "1" output level"""
        # input pins can not be changed
        input_pin = Pin(pin=12, mode=Pin.IN)

        # check default pin state
        self.assertEqual(input_pin.value(), False)

        # set new pin state
        input_pin.on()
        self.assertEqual(input_pin.value(), False)

        # set new pin state
        input_pin.off()
        self.assertEqual(input_pin.value(), False)

        input_pin.on()
        self.assertEqual(input_pin.value(), False)

        # output pins can be changed
        output_pin = Pin(pin=12, mode=Pin.OUT)

        # check default pin state
        self.assertEqual(output_pin.value(), False)

        # set new pin state
        output_pin.on()
        self.assertEqual(output_pin.value(), True)

        # set new pin state
        output_pin.off()
        self.assertEqual(output_pin.value(), False)

        # set new pin state
        output_pin.on()
        self.assertEqual(output_pin.value(), True)


if __name__ == '__main__':
    unittest.main()
