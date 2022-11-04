#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of Machine Timer"""

import time
import unittest

# custom imports
import machine


class TestTimer(unittest.TestCase):
    def setUp(self) -> None:
        self.my_var = 0

    def tearDown(self) -> None:
        pass

    def increment_var(self, tim: machine.Timer = None) -> None:
        self.my_var += 1

    def test__init__(self) -> None:
        this_timer = machine.Timer(-1)
        self.assertIsNone(this_timer._timer)

    def test_init_oneshot(self) -> None:
        """Test initializing timer in one shot mode"""
        self.assertEqual(self.my_var, 0)

        this_timer = machine.Timer(-1)
        cb_period = 1000    # milliseconds

        this_timer.init(mode=machine.Timer.ONE_SHOT,
                        period=cb_period,
                        callback=self.increment_var)

        # give the timer enough space to run and perform the callback call
        time.sleep((cb_period / 1000) * 2)

        self.assertEqual(self.my_var, 1)

    def test_init_periodic(self) -> None:
        """Test initializing timer in periodic mode"""
        self.assertEqual(self.my_var, 0)

        this_timer = machine.Timer(-1)
        cb_period = 1000    # milliseconds
        iterations = 10     # let timer execute n times

        this_timer.init(mode=machine.Timer.PERIODIC,
                        period=cb_period,
                        callback=self.increment_var)

        # give the timer enough space to run and perform the callback call
        time.sleep((cb_period / 1000) * iterations + 1)
        this_timer.deinit()

        self.assertEqual(self.my_var, iterations)

    def test_init_unsupported(self) -> None:
        """Test initializing timer with unsupported mode"""
        this_timer = machine.Timer(-1)
        cb_period = 1000    # milliseconds
        unsupported_mode = 3

        with self.assertRaises(machine.TimerError) as context:
            this_timer.init(mode=unsupported_mode,
                            period=cb_period,
                            callback=self.increment_var)

        self.assertEqual('Unsupported Timer mode: {}'.format(unsupported_mode),
                         str(context.exception))

    def test_deinit(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
