#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of Machine"""

import unittest

# custom imports
from machine import machine


class TestMachine(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_reset_cause(self) -> None:
        """Test getting the reset cause"""
        result = machine.reset_cause()
        self.assertEqual(result, 5)
        self.assertEqual(result, machine.SOFT_RESET)

    def test_unique_id(self) -> None:
        """Test getting the unique ID"""
        result = machine.unique_id()
        self.assertIsInstance(result, bytes)
        self.assertEqual(result, b'\xde\xad\xbe\xef')

    def test_freq(self) -> None:
        """Test getting the device CPU frequency"""
        result = machine.freq()
        self.assertIsInstance(result, int)
        self.assertEqual(result, 160 * 1000 * 1000)


if __name__ == '__main__':
    unittest.main()
