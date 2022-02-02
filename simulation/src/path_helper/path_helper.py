#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Provide unavailable path functions in MicroPython
"""

from pathlib import Path


class PathHelper(object):
    """docstring for PathHelper"""
    def __init__(self):
        pass

    # There's currently no os.path.exists() support in MicroPython
    @staticmethod
    def exists(path: str) -> bool:
        """
        Check existance of file at given path.

        :param      path:   The path to the file
        :type       path:   str

        :returns:   Existance of file
        :rtype:     bool
        """
        result = Path(path).exists()
