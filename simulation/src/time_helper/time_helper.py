#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Time Helper

Sync and set internal clock (RTC) with NTP server time
"""

from machine import RTC
# import ntptime
import time


class TimeHelper(object):
    """docstring for TimeHelper"""
    def __init__(self, tz: int = 1):
        """
        Initialize TimeHelper

        :param      tz: Timezone offset
        :type       tz: int, optional
        """
        self.rtc = RTC()
        self._timezone = tz

    def sync_time(self, timezone: int = None) -> None:
        """
        Sync the RTC with data from NTP server.

        No network check is performed.
        Existing RTC value will not be changed if NTP server is not reached.
        No daylight saving is implemented.

        :param      timezone:  The timezone shift
        :type       timezone:  int, optional
        """
        pass
