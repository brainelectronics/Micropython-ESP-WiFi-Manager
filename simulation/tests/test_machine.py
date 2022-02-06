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
        result = machine.reset_cause()
        self.assertEqual(result, 5)
        self.assertEqual(result, machine.SOFT_RESET)

    def test_unique_id(self) -> None:
        result = machine.unique_id()
        self.assertIsInstance(result, bytes)
        self.assertEqual(result, b'DEADBEEF')


if __name__ == '__main__':
    unittest.main()
