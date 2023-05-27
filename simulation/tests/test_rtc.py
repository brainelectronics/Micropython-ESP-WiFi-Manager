#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of Machine RTC"""

from datetime import datetime
import unittest
import time

# custom imports
from machine import RTC


class TestRTC(unittest.TestCase):
    def setUp(self) -> None:
        self.rtc = RTC()

    def tearDown(self) -> None:
        pass

    def test__init(self) -> None:
        """Test initial values"""
        time_tuple = self.rtc._time_tuple
        self.assertIsInstance(time_tuple, tuple)
        self.assertTrue(all(isinstance(ele, int) for ele in time_tuple))
        self.assertEqual(time_tuple, (2000, 1, 1, 0, 0, 0, 0, 0))

    @unittest.skip("Failing on CI")
    def test_init(self) -> None:
        """Test initialization of RTC"""
        timezone = 0
        tm = time.localtime()
        # now = datetime.fromtimestamp(time.mktime(tm))
        now = datetime.fromtimestamp(time.time())

        self.rtc.init(
            (tm[0], tm[1], tm[2], tm[3], tm[4], tm[5], 0, timezone)
        )

        time_tuple = self.rtc._time_tuple
        self.assertEqual(time_tuple,
                         (now.year, now.month, now.day,
                          now.weekday(),
                          now.hour, now.minute, now.second, 0))

    @unittest.skip("Failing on CI")
    def test_datetime(self) -> None:
        """Test getting current datetime"""
        datetime = self.rtc.datetime()
        self.assertIsInstance(datetime, tuple)
        self.assertTrue(all(isinstance(ele, int) for ele in datetime))
        self.assertEqual(datetime, (2000, 1, 1, 0, 0, 0, 0, 0))


if __name__ == '__main__':
    unittest.main()
