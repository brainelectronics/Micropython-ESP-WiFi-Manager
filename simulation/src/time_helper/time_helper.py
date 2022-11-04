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
        tm = time.localtime()
        print("Local time before synchronization: {}".format(tm))
        # Local time before synchronization: (2000, 1, 1, 0, 9, 44, 5, 1)
        #                                    (y, m, d, h, min, sec, wd, yd)

        # sync time with NTP server
        """
        try:
            ntptime.settime()
            print('Synced with NTP server')
        except Exception as e:
            print('Failed to sync with NTP server due to {}'.format(e))
            return
        """

        if timezone is None:
            timezone = self._timezone

        tm = time.localtime()
        tm = (tm[0], tm[1], tm[2], tm[3] + timezone, tm[4], tm[5], tm[6], tm[7])    # noqa
        #    (year,  month, day,   hour,             min,   sec,   wday,  yday)

        print("Local time after synchronization: {}".format(tm))
        # Local time after synchronization: (2021, 7, 15, 19, 12, 25, 1, 196)
        # (2021, 7, 15, 19, 12,  25,       1, 196)
        # (year, m, day, h, min,sec, weekday, yearday)
        # (0,    1,  2,  3,  4,   5,       6, 7)

        #    year, month, day, hours, minutes, seconds, subsec, tzinfo
        self.rtc.init(
            (tm[0], tm[1], tm[2], tm[3], tm[4], tm[5], 0, self.timezone)
        )

    @property
    def timezone(self) -> int:
        """
        Current timezone

        :returns:   This timezone
        :rtype:     int
        """
        return self._timezone

    @timezone.setter
    def timezone(self, value: int) -> None:
        """
        Set timezone for RTC

        :param      value:  The timezone offset
        :type       value:  int
        """
        self._timezone = value

    @property
    def year(self) -> int:
        """
        Current year from RTC

        :returns:   This year
        :rtype:     int
        """
        # (y,    m,  d, wd, h, m,  s, subseconds)
        # (2021, 7, 15, 5, 19, 12, 25, 1, 196)
        return self.rtc.datetime()[0]

    @property
    def month(self) -> int:
        """
        Current month from RTc

        :returns:   This month
        :rtype:     int
        """
        # (y,    m,  d, wd, h, m,  s, subseconds)
        # (2021, 7, 15, 5, 19, 12, 25, 1, 196)
        return self.rtc.datetime()[1]

    @property
    def day(self) -> int:
        """
        Current day from RTC

        :returns:   This day
        :rtype:     int
        """
        # (y,    m,  d, wd, h, m,  s, subseconds)
        # (2021, 7, 15, 5, 19, 12, 25, 1, 196)
        return self.rtc.datetime()[2]

    @property
    def weekday(self) -> int:
        """
        Current weekday from RTC

        :returns:   This weekday
        :rtype:     int
        """
        # (y,    m,  d, wd, h, m,  s, subseconds)
        # (2021, 7, 15, 5, 19, 12, 25, 1, 196)
        return self.rtc.datetime()[3]

    @property
    def hour(self) -> int:
        """
        Current hour from RTC

        :returns:   This hour
        :rtype:     int
        """
        # (y,    m,  d, wd, h, m,  s, subseconds)
        # (2021, 7, 15, 5, 19, 12, 25, 1, 196)
        return self.rtc.datetime()[4]

    @property
    def minute(self) -> int:
        """
        Current minute from RTC

        :returns:   This minute
        :rtype:     int
        """
        # (y,    m,  d, wd, h, m,  s, subseconds)
        # (2021, 7, 15, 5, 19, 12, 25, 1, 196)
        return self.rtc.datetime()[5]

    @property
    def second(self) -> int:
        """
        Current second from RTC

        :returns:   This second
        :rtype:     int
        """
        # (y,    m,  d, wd, h, m,  s, subseconds)
        # (2021, 7, 15, 5, 19, 12, 25, 1, 196)
        return self.rtc.datetime()[6]

    @property
    def current_timestamp(self) -> tuple:
        """
        Get current timestamp

        :returns:   Current system timestamp
        :rtype:     tuple
        """
        # (2021, 7,  15, 19,  12,  25,       1,     196)
        # (year, m, day,  h, min, sec, weekday, yearday)
        # (0,    1,   2,  3,    4,  5,       6,       7)
        return time.localtime()

    @property
    def current_timestamp_iso8601(self) -> str:
        """
        Get current timestamp in ISO8601 format

        :returns:   Timestamp as HH:MM:SS YYYY-MM-DD
        :rtype:     str
        """
        now = self.current_timestamp
        return (
            '{hour:02d}:{minute:02d}:{sec:02d} {year}-{month:02d}-{day:02d}'.
            format(hour=now[3],
                   minute=now[4],
                   sec=now[5],
                   year=now[0],
                   month=now[1],
                   day=now[2]))

    @property
    def current_timestamp_human(self) -> str:
        """
        Wrapper around @see current_timestamp_iso8601

        :returns:   Timestamp as HH:MM:SS YYYY-MM-DD
        :rtype:     str
        """
        return self.current_timestamp_iso8601
