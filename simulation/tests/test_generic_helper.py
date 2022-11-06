#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of Generic Helper"""

import gc
import logging
import os
from nose2.tools import params
import time
from typing import List, Union
import unittest
from unittest.mock import patch, mock_open, Mock
from random import randint

# custom imports
from generic_helper import GenericHelper


class TestGenericHelper(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @params(
        (None),
        ('Sauerkraut')
    )
    def test_create_logger(self, logger_name: Union[None, str]) -> None:
        """
        Test creation of loggers

        :param      logger_name:  The logger name
        :type       logger_name:  Union[None, str]
        """
        logger = GenericHelper.create_logger(logger_name=logger_name)

        if not logger_name:
            logger_name = 'generic_helper.generic_helper'

        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertEqual(logger.name, logger_name)

    def test_set_level(self) -> None:
        """Test setting the logger level"""
        logger = GenericHelper.create_logger()
        self.assertEqual(logger.level, logging.DEBUG)

        GenericHelper.set_level(logger=logger, level='debug')
        self.assertEqual(logger.level, logging.DEBUG)

        GenericHelper.set_level(logger=logger, level='info')
        self.assertEqual(logger.level, logging.INFO)

        GenericHelper.set_level(logger=logger, level='warning')
        self.assertEqual(logger.level, logging.WARNING)

        GenericHelper.set_level(logger=logger, level='error')
        self.assertEqual(logger.level, logging.ERROR)

        GenericHelper.set_level(logger=logger, level='critical')
        self.assertEqual(logger.level, logging.CRITICAL)

        GenericHelper.set_level(logger=logger, level='unknonw_level')
        self.assertEqual(logger.level, logging.CRITICAL)

    def test_set_logger_verbose_level(self) -> None:
        """Test setting the logger level"""
        logger = GenericHelper.create_logger()
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertFalse(logger.disabled)

        # set verbose level -vv == WARNING
        GenericHelper.set_logger_verbose_level(logger=logger,
                                               verbose_level=2,
                                               debug_output=True)
        self.assertEqual(logger.level, logging.WARNING)

        # disable logger output
        logger = GenericHelper.create_logger()
        GenericHelper.set_logger_verbose_level(logger=logger,
                                               verbose_level=None,
                                               debug_output=False)
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertTrue(logger.disabled)

        logger = GenericHelper.create_logger()
        GenericHelper.set_logger_verbose_level(logger=logger,
                                               verbose_level=None,
                                               debug_output=True)
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertTrue(logger.disabled)

    @params(
        (0),
        (123)
    )
    def test_get_random_value(self, expectation: int) -> None:
        """
        Test getting a random value within some range

        :param      expectation:  The expectation
        :type       expectation:  int
        """
        # mocking random values feels so random
        with patch('random.randint', return_value=expectation):
            value = GenericHelper.get_random_value()
            self.assertEqual(value, expectation)

    def test_get_uuid(self) -> None:
        """Test getting the UUID of the device"""
        value = GenericHelper.get_uuid()
        self.assertEqual(value, b'deadbeef')

        requested_length = 10
        value = GenericHelper.get_uuid(length=requested_length)
        self.assertEqual(len(value), requested_length)
        self.assertEqual(value, b'deadbeefde')

        requested_length = -5
        value = GenericHelper.get_uuid(length=requested_length)
        self.assertEqual(len(value), abs(requested_length))
        self.assertEqual(value, b'dbeef')

    @params(
        (None, 61354754048),
        ('byte', '61354754048 byte'),
        ('BYTE', '61354754048 byte'),
        ('kb', '59916752.000 kB'),
        ('kB', '59916752.000 kB'),
        ('Kb', '59916752.000 kB'),
        ('Kb', '59916752.000 kB'),
        ('KB', '59916752.000 kB'),
        ('mb', '58512.453 MB'),
        ('mB', '58512.453 MB'),
        ('Mb', '58512.453 MB'),
        ('MB', '58512.453 MB'),
        ('unknown', -1)
    )
    def test_df(self,
                unit: Union[None, str],
                expectation: Union[int, str]) -> None:
        """
        Test getting free diskspace in different size formats

        :param      unit:         The unit
        :type       unit:         Union[None, str]
        :param      expectation:  The expectation
        :type       expectation:  Union[int, str]
        """
        return_value = os.statvfs_result((
            4096, 4096, 61069442, 14979188, 14915188, 61069440, 14915188,
            14915188, 0, 255))

        with patch('os.statvfs', return_value=return_value):
            result = GenericHelper.df(unit=unit)

        if unit:
            if unit != 'unknown':
                self.assertIsInstance(result, str)
            else:
                self.assertIsInstance(result, int)
        else:
            self.assertIsInstance(result, int)

        if expectation:
            self.assertEqual(result, expectation)

    @params(
        (0, 0, '100.00%'),
        (100, 0, '100.00%'),
        (0, 100, '0.00%'),
        (100, 100, '50.00%'),
        (10, 20, '33.33%')
    )
    def test_get_free_memory(self,
                             free: int,
                             allocated: int,
                             expectation: str) -> None:
        """
        Test getting free memory (RAM)

        :param      free:         Free bytes
        :type       free:         int
        :param      allocated:    Allocated bytes
        :type       allocated:    int
        :param      expectation:  Expected ratio
        :type       expectation:  str
        """
        gc.mem_free = Mock(return_value=free)
        gc.mem_alloc = Mock(return_value=allocated)

        result = GenericHelper.get_free_memory()

        self.assertIsInstance(result, dict)
        self.assertIn('free', result)
        self.assertIn('total', result)
        self.assertIn('percentage', result)

        self.assertEqual(result['free'], free)
        self.assertEqual(result['total'], allocated + free)
        self.assertEqual(result['percentage'], expectation)

    @params(
        (False, 0, 0, '100.00%'),
        (True, 0, 0, 'Total: 0.0 kB, Free: 0.00 kB (100.00%)'),
        (True, 100, 0, 'Total: 0.1 kB, Free: 0.10 kB (100.00%)'),
        (True, 0, 100, 'Total: 0.1 kB, Free: 0.00 kB (0.00%)'),
        (True, 100, 100, 'Total: 0.2 kB, Free: 0.10 kB (50.00%)'),
        (True, 100, 200, 'Total: 0.3 kB, Free: 0.10 kB (33.33%)'),
        (True, 1000, 2000, 'Total: 2.9 kB, Free: 0.98 kB (33.33%)'),
        (True, 1024, 2048, 'Total: 3.0 kB, Free: 1.00 kB (33.33%)'),
    )
    def test_free(self,
                  full: bool,
                  free: int,
                  allocated: int,
                  expectation: str) -> None:
        """
        Test getting detailed informations about free memory (RAM)

        :param      full:         Flag to get full details
        :type       full:         bool
        :param      free:         Free bytes
        :type       free:         int
        :param      allocated:    Allocated bytes
        :type       allocated:    int
        :param      expectation:  Expected ratio
        :type       expectation:  str
        """
        gc.mem_free = Mock(return_value=free)
        gc.mem_alloc = Mock(return_value=allocated)

        result = GenericHelper.free(full=full)

        self.assertIsInstance(result, str)
        self.assertEqual(result, expectation)

    def test_get_system_infos_raw(self) -> None:
        """Test getting the system infos"""
        mem_free_value = 10
        mem_alloc_value = 100
        ticks_ms_value = randint(1000, 1000 * 1000)
        statvfs_return_value = os.statvfs_result((
            4096, 4096, 61069442, 14979188, 14915188, 61069440, 14915188,
            14915188, 0, 255))

        expectation = {
            'df': '59916752.000 kB',
            'free_ram': mem_free_value,
            'frequency': 160000000,
            'percentage_ram': '9.09%',
            'total_ram': mem_alloc_value + mem_free_value,
            'uptime': ticks_ms_value
        }

        # mock all functions
        os.statvfs = Mock(return_value=statvfs_return_value)
        gc.mem_free = Mock(return_value=mem_free_value)
        gc.mem_alloc = Mock(return_value=mem_alloc_value)
        time.ticks_ms = Mock(return_value=ticks_ms_value)

        sys_info = GenericHelper.get_system_infos_raw()
        self.assertIsInstance(sys_info, dict)
        self.assertEqual(sys_info, expectation)

    def test_get_system_infos_human(self) -> None:
        """Test getting the system infos in human readable format"""
        # mock gc functions
        mem_free_value = 10
        mem_alloc_value = 100
        ticks_ms_value = 498042
        statvfs_return_value = os.statvfs_result((
            4096, 4096, 61069442, 14979188, 14915188, 61069440, 14915188,
            14915188, 0, 255))

        expectation = {
            'df': '59916752.000 kB',
            'free_ram': '0.01 kB',
            'frequency': '160 MHz',
            'percentage_ram': '9.09%',
            'total_ram': '0.11 kB',
            'uptime': '0 days, 00:08:18'
        }

        # mock all functions
        os.statvfs = Mock(return_value=statvfs_return_value)
        gc.mem_free = Mock(return_value=mem_free_value)
        gc.mem_alloc = Mock(return_value=mem_alloc_value)
        time.ticks_ms = Mock(return_value=ticks_ms_value)

        sys_info = GenericHelper.get_system_infos_human()
        self.assertIsInstance(sys_info, dict)
        self.assertEqual(sys_info, expectation)

    @params(
        (
            "{'test': 123}",
            {'test': 123}
        ),
        (
            "{'val': true}",
            {'val': True}
        ),
        (
            "{'nested': {'this': 'that'}}",
            {'nested': {'this': 'that'}}
        ),
        (
            "[{'val': true}, {'other': false}]",
            [{'val': True}, {'other': False}]
        ),
    )
    def test_str_to_dict(self,
                         data: str,
                         expectation: Union[dict, List[dict]]) -> None:
        """
        Test converting a string to a dictionary

        :param      data:         The data
        :type       data:         str
        :param      expectation:  The expectation
        :type       expectation:  Union[dict, List[dict]]
        """
        result = GenericHelper.str_to_dict(data=data)

        self.assertIsInstance(result, type(expectation))
        self.assertEqual(result, expectation)

    def test_save_json(self) -> None:
        """Test saving data as JSON to a file"""
        fake_file_path = "fake/file/path"
        fake_content = {
            "data": "Content which is never written to a file",
            "other": 123
        }
        file_mode = 'w'

        with patch("builtins.open", mock_open()) as mock_file:
            with patch("json.dump",
                       Mock(return_value=fake_content)) as mock_dump:
                GenericHelper.save_json(data=fake_content,
                                        path=fake_file_path,
                                        mode=file_mode)

                mock_dump.assert_called_once_with(fake_content,
                                                  open(fake_file_path,
                                                       file_mode))

            # assert if opened file on write mode 'w'
            mock_file.assert_called_with(fake_file_path, file_mode)

    def test_load_json(self) -> None:
        """Test loading data as JSON from a file"""
        fake_file_path = "fake/file/path"
        fake_content = {
            "data": "Content which is never written to a file",
            "other": 123
        }
        file_mode = 'r'

        with patch("builtins.open", mock_open()) as mock_file:
            with patch("json.load", Mock(return_value=fake_content)):
                actual = GenericHelper.load_json(path=fake_file_path,
                                                 mode=file_mode)
            mock_file.assert_called_once_with(fake_file_path, file_mode)

        self.assertEqual(actual, fake_content)
        self.assertIsInstance(actual, dict)

    def test_save_file(self) -> None:
        """Test saving data to a file"""
        fake_file_path = "fake/file/path"
        fake_content = "Content which is never written to a file"
        file_mode = 'w'

        with patch("builtins.open", mock_open()) as mock_file:
            GenericHelper.save_file(data=fake_content,
                                    path=fake_file_path,
                                    mode=file_mode)

            # assert if opened file on write mode 'w'
            mock_file.assert_called_once_with(fake_file_path, file_mode)

            # assert if write(content) was called from the file opened
            # in another words, assert if the specific content was written
            mock_file().write.assert_called_once_with(fake_content)

    def test_load_file(self) -> None:
        """Test loading data from a file"""
        fake_file_path = "fake/file/path"
        fake_content = "Content which is never written to a file"
        file_mode = 'r'

        with patch("builtins.open",
                   mock_open(read_data=fake_content)) as mock_file:
            actual = GenericHelper.load_file(path=fake_file_path,
                                             mode=file_mode)
            mock_file.assert_called_once_with(fake_file_path, file_mode)

        self.assertEqual(actual, fake_content)

    def test_read_file(self) -> None:
        """Test reading data from a file"""
        fake_file_path = "fake/file/path"
        fake_content = "Content which is never written to a file"
        file_mode = 'r'

        with patch("builtins.open",
                   mock_open(read_data=fake_content)) as mock_file:
            actual = GenericHelper.read_file(path=fake_file_path,
                                             mode=file_mode)
            mock_file.assert_called_once_with(fake_file_path, file_mode)

        self.assertEqual(actual, fake_content)


if __name__ == '__main__':
    unittest.main()
