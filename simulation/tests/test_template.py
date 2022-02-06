#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of ClassName"""

from nose2.tools import params
from typing import Union
import unittest

# custom imports
# from xxx import ClassName


class TestTemplate(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @params(
        (None),
        ('Sauerkraut')
    )
    def test_asdf(self, var: Union[None, str]) -> None:
        """
        Test asdf function

        :param      var:  Variable description
        :type       var:  Union[None, str]
        """
        pass

    @unittest.skip("Not yet implemented")
    def test_qwertz(self) -> None:
        """Test quertz function"""
        pass


if __name__ == '__main__':
    unittest.main()
