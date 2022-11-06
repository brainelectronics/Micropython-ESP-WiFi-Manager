#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Fake Micropython Machine class

See https://docs.micropython.org/en/latest/library/machine.html
"""
import binascii


class machine(object):
    """docstring for machine"""
    UNKNOWN_RESET = 0
    PWRON_RESET = 1
    HARD_RESET = 2
    WDT_RESET = 3
    DEEPSLEEP_RESET = 4
    SOFT_RESET = 5

    def __init__(self):
        pass

    @staticmethod
    def reset_cause() -> int:
        """
        Get last reset cause

        :returns:   Reset cause
        :rtype:     int
        """
        return machine.SOFT_RESET

    @staticmethod
    def unique_id() -> bytes:
        """
        Get unique device ID

        :returns:   Device ID
        :rtype:     bytes
        """
        return binascii.unhexlify(b'DEADBEEF')

    @staticmethod
    def freq() -> int:
        """
        Get current CPU frequency

        :returns:   CPU frequency in Hz
        :rtype:     int
        """
        return 160 * 1000 * 1000
