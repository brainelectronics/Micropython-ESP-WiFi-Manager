#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Unittest for testing the absolute truth"""

import logging
import sys
import unittest


class TestAbsoluteTruth(unittest.TestCase):
    def setUp(self) -> None:
        """Run before every test method"""
        # define a format
        custom_format = "[%(asctime)s][%(levelname)-8s][%(filename)-20s @" \
                        " %(funcName)-15s:%(lineno)4s] %(message)s"

        # set basic config and level for all loggers
        logging.basicConfig(level=logging.INFO,
                            format=custom_format,
                            stream=sys.stdout)

        # create a logger for this TestSuite
        self.test_logger = logging.getLogger(__name__)

        # set the test logger level
        self.test_logger.setLevel(logging.DEBUG)

        # enable/disable the log output of the device logger for the tests
        # if enabled log data inside this test will be printed
        self.test_logger.disabled = False

    def test_absolute_truth(self) -> None:
        """Test the unittest itself"""
        x = 0
        y = 1
        z = 2
        none_thing = None
        some_dict = dict()
        some_list = [x, y, 40, "asdf", z]

        self.assertTrue(True)
        self.assertFalse(False)

        self.assertEqual(y, 1)
        assert y == 1
        self.assertNotEqual(x, y)
        assert x != y

        self.assertIsNone(none_thing)
        self.assertIsNotNone(some_dict)

        self.assertIn(y, some_list)
        self.assertNotIn(12, some_list)

        # self.assertRaises(exc, fun, args, *kwds)

        self.assertIsInstance(some_dict, dict)

        self.assertGreater(a=y, b=x)
        self.assertGreaterEqual(a=y, b=x)
        self.assertLess(a=x, b=y)

        self.test_logger.debug("Sample debug message")

    def tearDown(self) -> None:
        """Run after every test method"""
        pass


if __name__ == '__main__':
    unittest.main()
