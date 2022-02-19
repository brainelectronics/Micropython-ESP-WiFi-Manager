#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Fake Micropython Machine class

See https://docs.micropython.org/en/latest/library/machine.html
"""


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
        return machine.SOFT_RESET

    @staticmethod
    def unique_id() -> bytes:
        return b'DEADBEEF'
