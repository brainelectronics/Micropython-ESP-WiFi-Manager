#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of Message"""

from nose2.tools import params
from typing import Any
import unittest

# custom imports
from generic_helper import Message


class TestMessage(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @unittest.skip("Checked by test_set")
    def test_clear(self) -> None:
        pass

    @params(
        (None),
        (False),
        (True),
        (0),
        (1),
        (3.14),
        ("string"),
        (["string", True]),
        ({'key': ["string", True], 'key2': 42}),
    )
    def test_set(self, data: Any) -> None:
        msg = Message()
        msg.set(data)

        result = msg.value()
        self.assertEqual(result, data)

        for x in range(3, 10):
            msg.set(x)
            result = msg.value()
            self.assertNotEqual(result, data)
            self.assertEqual(result, x)

        msg2 = Message()
        msg.set(msg2)

        result = msg.value()
        self.assertEqual(result, msg2)

    @unittest.skip("Checked by test_set")
    def test_is_set(self) -> None:
        pass

    @unittest.skip("Checked by test_set")
    def test_value(self) -> None:
        """Test getting latest value of Message"""
        pass


if __name__ == '__main__':
    unittest.main()
