#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Fake Micropython Timer class

See https://docs.micropython.org/en/latest/library/machine.Timer.html
"""

from threading import Timer as ThreadTimer

from typing import Any, Callable


class RepeatTimer(ThreadTimer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class TimerError(Exception):
    """Base class for exceptions in this module."""
    pass


class Timer(object):
    """docstring for Timer"""
    ONE_SHOT = 0
    PERIODIC = 1

    def __init__(self, id: int = 0):
        self._timer = None

    def init(self,
             mode: int = PERIODIC,
             period: int = -1,
             callback: Callable[[Any], None] = None) -> None:
        """
        Initialise the timer

        :param      mode:      The mode
        :type       mode:      int
        :param      period:    The timer period in milliseconds
        :type       period:    int
        :param      callback:  The callable to call upon expiration of the
                               timer period
        :type       callback:  Callable[[Any], None]
        """
        if mode == self.ONE_SHOT:
            self._timer = ThreadTimer(interval=(period / 1000),
                                      function=callback,
                                      args=None)
            self._timer.start()
        elif mode == self.PERIODIC:
            self._timer = RepeatTimer(interval=(period / 1000),
                                      function=callback,
                                      args=None)
            self._timer.start()
        else:
            raise TimerError('Unsupported Timer mode: {}'.format(mode))

    def deinit(self) -> None:
        """Deinitialises/stops the timer"""
        if self._timer:
            self._timer.cancel()
