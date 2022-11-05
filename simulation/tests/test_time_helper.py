#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of TimeHelper"""

import time
import unittest
from unittest.mock import Mock

# custom imports
from time_helper import TimeHelper


class TestTimeHelper(unittest.TestCase):
    def setUp(self) -> None:
        time.localtime = Mock(
            #            (year, m, day, h, min, sec, weekday, yearday)
            return_value=(2022, 11, 3, 18, 15, 31, 3, 307)
            #             0,    1,  2, 3,  4,  5,  6,  7
        )
        self.th = TimeHelper()
        self.th.sync_time()

    def tearDown(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_sync_time(self) -> None:
        """Test sync_time"""
        pass

    def test_timezone(self) -> None:
        """Test getting current timezone"""
        self.assertEqual(self.th.timezone, 1)

        self.th.timezone = 2
        self.assertEqual(self.th.timezone, 2)

    def test_year(self) -> None:
        """Test getting current year"""
        self.assertEqual(self.th.year, 2022)

    def test_month(self) -> None:
        """Test getting current month"""
        self.assertEqual(self.th.month, 11)

    def test_day(self) -> None:
        """Test getting current day"""
        self.assertEqual(self.th.day, 3)

    def test_weekday(self) -> None:
        """Test getting current weekday"""
        self.assertEqual(self.th.weekday, 3)

    def test_hour(self) -> None:
        """Test getting current hour"""
        self.assertEqual(self.th.hour, 18 + self.th.timezone)

    def test_minute(self) -> None:
        """Test getting current minute"""
        self.assertEqual(self.th.minute, 15)

    def test_second(self) -> None:
        """Test getting current second"""
        self.assertEqual(self.th.second, 31)

    def test_current_timestamp(self) -> None:
        """Test getting current timestamp"""
        self.assertEqual(self.th.current_timestamp,
                         (2022, 11, 3, 18, 15, 31, 3, 307))

    def test_current_timestamp_iso8601(self) -> None:
        """Test getting current timestamp in ISO8601 format"""
        self.assertEqual(self.th.current_timestamp_iso8601,
                         '18:15:31 2022-11-03')

    def test_current_timestamp_human(self) -> None:
        """Test getting current timestamp in human readable ISO8601 format"""
        self.assertEqual(self.th.current_timestamp_human,
                         '18:15:31 2022-11-03')


if __name__ == '__main__':
    unittest.main()
