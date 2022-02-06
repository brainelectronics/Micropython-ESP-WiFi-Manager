#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Generic helper

Collection of helper functions used in other modules
"""

import gc
import json
import logging
import os
import random
import sys

from typing import (Optional, Union)


class GenericHelper(object):
    """docstring for GenericHelper"""
    def __init__(self):
        pass

    @staticmethod
    def create_logger(logger_name: Optional[str] = None) -> logging.Logger:
        """
        Create a logger.

        :param      logger_name:  The logger name
        :type       logger_name:  str, optional

        :returns:   Configured logger
        :rtype:     logging.Logger
        """
        custom_format = '[%(asctime)s] [%(levelname)-8s] [%(filename)-15s @'\
                        ' %(funcName)-15s:%(lineno)4s] %(message)s'

        # configure logging
        logging.basicConfig(level=logging.INFO,
                            format=custom_format,
                            stream=sys.stdout)

        if logger_name and (isinstance(logger_name, str)):
            logger = logging.getLogger(logger_name)
        else:
            logger = logging.getLogger(__name__)

        # set the logger level to DEBUG if specified differently
        logger.setLevel(logging.DEBUG)

        return logger

    @staticmethod
    def set_level(logger: logging.Logger, level: str) -> None:
        """
        Set the level of a logger.

        :param      logger:  The logger to set the level
        :type       logger:  logging.Logger
        :param      level:   The new level
        :type       level:   str
        """
        if level.lower() == 'debug':
            logger.setLevel(level=logging.DEBUG)
        elif level.lower() == 'info':
            logger.setLevel(level=logging.DEBUG)
        elif level.lower() == 'warning':
            logger.setLevel(level=logging.WARNING)
        elif level.lower() == 'error':
            logger.setLevel(level=logging.ERROR)
        elif level.lower() == 'critical':
            logger.setLevel(level=logging.CRITICAL)

    @staticmethod
    def set_logger_verbose_level(logger: logging.Logger,
                                 verbose_level: int,
                                 debug_output: bool):
        """
        Set the logger verbose level and debug output

        :param      logger:         The logger to apply the settings to
        :type       logger:         logging.Logger
        :param      verbose_level:  The verbose level
        :type       verbose_level:  int
        :param      debug_output:   The debug mode
        :type       debug_output:   bool
        """
        LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        LOG_LEVELS = LOG_LEVELS[::-1]

        if verbose_level is None:
            if not debug_output:
                # disable the logger
                logger.disabled = True
        else:
            log_level = min(len(LOG_LEVELS) - 1, max(verbose_level, 0))
            log_level_name = LOG_LEVELS[log_level]

            # set the level of the logger
            logger.setLevel(log_level_name)

    @staticmethod
    def get_random_value(lower: int = 0, upper: int = 255) -> int:
        """
        Get a random value within the given range

        :param      lower:  The lower boundary
        :type       lower:  int, optional
        :param      upper:  The upper boundary, inclusive, default 255
        :type       upper:  int, optional

        :returns:   The random value.
        :rtype:     int
        """
        return random.randint(lower, upper)

    @staticmethod
    def df(path: str = '//', unit: Optional[str] = None) -> Union[int, str]:
        """
        Get free disk space

        :param      path:    Path to obtain informations
        :type       path:    str, optional
        :param      unit:    Unit of returned size [None, 'byte', 'kB', 'MB']
        :type       unit:    str, optional

        :returns:   Available disk space in byte or as string in kB or MB
        :rtype:     int or str
        """
        info = os.statvfs(path)

        result = -1

        if unit is None:
            result = info[0] * info[3]
        elif unit.lower() == 'byte':
            result = ('{} byte'.format((info[0] * info[3])))
        elif unit.lower() == 'kb':
            result = ('{0:.3f} kB'.format((info[0] * info[3]) / 1024))
        elif unit.lower() == 'mb':
            result = ('{0:.3f} MB'.format((info[0] * info[3]) / 1048576))

        return result

    @staticmethod
    def get_free_memory() -> dict:
        """
        Get free memory (RAM)

        :param      update:  Flag to collect latest informations
        :type       update:  bool, optional

        :returns:   Informations about system RAM
        :rtype:     dict
        """
        gc.collect()
        free = gc.mem_free()
        allocated = gc.mem_alloc()
        total = free + allocated

        if total:
            percentage = '{0:.2f}%'.format((free / total) * 100)
        else:
            percentage = '100.00%'

        memory_stats = {'free': free,
                        'total': total,
                        'percentage': percentage}

        return memory_stats

    @staticmethod
    def free(full: bool = False) -> Union[int, str]:
        """
        Get detailed informations about free RAM

        :param      full:    Flag to return str with total, free, percentage
        :type       full:    bool, optional

        :returns:   Informations, percentage by default
        :rtype:     int or str
        """
        memory_stats = GenericHelper.get_free_memory()

        if full is False:
            return memory_stats['percentage']
        else:
            return ('Total: {0:.1f} kB, Free: {1:.2f} kB ({2})'.
                    format(memory_stats['total'] / 1024,
                           memory_stats['free'] / 1024,
                           memory_stats['percentage']))

    @staticmethod
    def str_to_dict(data: str) -> dict:
        """
        Convert string to dictionary

        :param      data:  The data
        :type       data:  str

        :returns:   Dictionary of string
        :rtype:     dict
        """
        return json.loads(data.replace("'", "\""))

    @staticmethod
    def save_json(data: dict, path: str, mode: str = 'w') -> None:
        """
        Save data as JSON file.

        :param      data:  The data
        :type       data:  dict
        :param      path:  The path to the JSON file
        :type       path:  str
        :param      mode:  The mode of file operation
        :type       mode:  str, optional
        """
        with open(path, mode) as file:
            json.dump(data, file)

    @staticmethod
    def load_json(path: str, mode: str = 'r') -> dict:
        """
        Load data from JSON file.

        :param      path:  The path to the JSON file
        :type       path:  str
        :param      mode:  The mode of file operation
        :type       mode:  str, optional

        :returns:   Loaded data
        :rtype:     dict
        """
        read_data = dict()
        with open(path, mode) as file:
            read_data = json.load(file)

        return read_data

    @staticmethod
    def save_file(data: str, path: str, mode: str = 'wb') -> None:
        """
        Save data to a file.

        :param      data:  The data
        :type       data:  str
        :param      path:  The path to the file
        :type       path:  str
        :param      mode:  The mode of file operation
        :type       mode:  str, optional
        """
        # save to file as binary by default
        with open(path, mode) as file:
            file.write(data)

    @staticmethod
    def load_file(path: str, mode: str = 'rb') -> str:
        """
        Wrapper for read_file.

        :param      path:  The path to the file to read
        :type       path:  str

        :returns:   The raw file content.
        :rtype:     str
        :param      mode:  The mode of file operation
        :type       mode:  str, optional

        :returns:   Content of file
        :rtype:     str
        """
        return GenericHelper.read_file(path=path, mode=mode)

    @staticmethod
    def read_file(path: str, mode: str = 'rb') -> str:
        """
        Read file content.

        :param      path:  The path to the file to read
        :type       path:  str
        :param      mode:  The mode of file operation
        :type       mode:  str, optional

        :returns:   The raw file content.
        :rtype:     str
        """
        read_data = ""

        with open(path, mode) as file:
            read_data = file.read()

        return read_data
