#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of Path Helper"""

from pathlib import Path
import unittest
from unittest.mock import patch

# custom imports
from path_helper import PathHelper


class TestPathHelper(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_exists(self) -> None:
        with patch.object(Path, 'exists') as mock_exists:
            # mock file existance
            mock_exists.return_value = True
            result = PathHelper.exists(path='/some/path')
            self.assertTrue(result)

            # mock file unexistance
            mock_exists.return_value = False
            result = PathHelper.exists(path='/some/path')
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
