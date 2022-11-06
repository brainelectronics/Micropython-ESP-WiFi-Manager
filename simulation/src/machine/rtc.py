#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Fake Micropython RTC class

See https://docs.micropython.org/en/latest/library/machine.RTC.html
"""

import time
from datetime import date

from typing import Tuple


class RTC(object):
    """docstring for RTC"""
    def __init__(self, id: int = 0):
        self._time_tuple = (
            2000,   # year      0
            1,      # month     1
            1,      # day       2
            0,      # weekday   3
            0,      # hour      4
            0,      # minute    5
            0,      # second    6
            0       # subsecond 7
        )

    def init(self, time_tuple: Tuple[int]) -> None:
        """
        Initialize the RTC with the given time tuple.

        :param      time_tuple:  The time tuple
        :type       time_tuple:  Tuple[int]
        """
        print('RTC init as: {}'.format(time_tuple))
        print('year, month, day, hour, minute, second, subsec, tzinfo')

        weekday = date(time_tuple[0], time_tuple[1], time_tuple[2]).weekday()

        # set current time to the given time tuple
        self._time_tuple = (
            time_tuple[0], time_tuple[1], time_tuple[2],    # year, month, day
            weekday,    # weekday
            time_tuple[3], time_tuple[4], time_tuple[5],    # hour, min, sec
            time_tuple[6]   # subsecond
        )

    def datetime(self) -> time.struct_time:
        """
        Get current datetime

        :returns:   Time tuple
        :rtype:     time.struct_time
        """
        # return time.localtime()
        return self._time_tuple
