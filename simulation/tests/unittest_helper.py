#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Unittest helper

Common modules used for unittesting
"""

import logging
from pathlib import Path

# custom imports
from generic_helper import GenericHelper


class UnitTestHelper(object):
    """docstring for UnitTestHelper"""
    def __init__(self, logger: logging.Logger = None, quiet: bool = False):
        if logger is None:
            logger_name = self.__class__.__name__
            logger = GenericHelper.create_logger(logger_name=logger_name)
        self.logger = logger
        self.logger.disabled = quiet

    @staticmethod
    def get_current_path() -> Path:
        """
        Get the path to this file.

        :returns:   The path of this file
        :rtype:     Path object
        """
        here = Path(__file__).parent.resolve()

        return here
