#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of Network"""

from nose2.tools import params
import random
from typing import Union
import unittest
from unittest.mock import patch
import sys

# custom imports
from wifi_helper.network import NetworkHelper
from wifi_helper.network import Station
from wifi_helper.network import Client
from wifi_helper.network import WLAN


class TestNetworkHelper(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test__internal_scan(self) -> None:
        pass
        # with patch('sys.platform', 'unsupported') as mock_platform:
        #     nets = NetworkHelper._internal_scan()

    @unittest.skipIf(sys.platform == "linux" or sys.platform == "linux2",
                     'Linux not tested on this system')
    def test__scan_linux(self) -> None:
        pass

    @unittest.skipIf(sys.platform == 'darwin',
                     'Linux not tested on this system')
    def test__scan_mac(self) -> None:
        pass

    @unittest.skipIf(sys.platform == 'win32',
                     'Windows not tested on this system')
    @unittest.skip("Not yet implemented")
    def test__scan_windows(self) -> None:
        pass

    @params(
        (50, -75),  # percentage, dBm
    )
    def test__quality_to_dbm(self, quality: int, expectation: int) -> None:
        result = NetworkHelper._quality_to_dbm(quality=quality)
        self.assertEqual(result, expectation)

    def test__dummy_data(self) -> None:
        # get two random values for RSSI in range of 0 to 100
        mocked_rssi = random.sample(range(0, 100), 2)

        # patch call of random.randint inside of _dummy_data with mocked_rssi
        with patch('random.randint') as mock_randint:
            mock_randint.side_effect = mocked_rssi
            nets = NetworkHelper._dummy_data()

        self.assertIsInstance(nets, list)
        self.assertEqual(len(nets), 2)

        for net in nets:
            self.assertIsInstance(net, dict)
            required_keys = ['ssid', 'RSSI', 'bssid', 'authmode', 'channel', 'hidden']
            self.assertEqual(len(net.keys()), len(required_keys))
            self.assertTrue(all(name in required_keys for name in net.keys()))

        # check first network
        self.assertEqual(nets[0]['ssid'], 'TP-LINK_FBFC3C')
        self.assertEqual(nets[0]['RSSI'], -mocked_rssi[0])
        self.assertEqual(nets[0]['bssid'], 'a0f3c1fbfc3c')
        self.assertEqual(nets[0]['authmode'], 'WPA/WPA2-PSK')
        self.assertEqual(nets[0]['channel'], 1)
        self.assertEqual(nets[0]['hidden'], False)

        # check second network
        self.assertEqual(nets[1]['ssid'], 'FRITZ!Box 7490')
        self.assertEqual(nets[1]['RSSI'], -mocked_rssi[1])
        self.assertEqual(nets[1]['bssid'], '3810d517eb39')
        self.assertEqual(nets[1]['authmode'], 'WPA2-PSK')
        self.assertEqual(nets[1]['channel'], 11)
        self.assertEqual(nets[1]['hidden'], False)

    def test__dummy_data_upy(self) -> None:
        """Test getting dummy data in same style as Micropython"""
        # get two random values for RSSI in range of 0 to 100
        mocked_rssi = random.sample(range(0, 100), 2)

        # patch call of random.randint inside of _dummy_data with mocked_rssi
        with patch('random.randint') as mock_randint:
            mock_randint.side_effect = mocked_rssi
            dummy_data_upy = NetworkHelper._dummy_data_upy()

        self.assertIsInstance(dummy_data_upy, list)
        self.assertEqual(len(dummy_data_upy), 2)

        for net in dummy_data_upy:
            self.assertIsInstance(net, tuple)

        # check first network
        self.assertEqual(dummy_data_upy[0][0], 'TP-LINK_FBFC3C')
        self.assertEqual(dummy_data_upy[0][1], 'a0f3c1fbfc3c')
        self.assertEqual(dummy_data_upy[0][2], 1)
        self.assertEqual(dummy_data_upy[0][3], -mocked_rssi[0])
        self.assertEqual(dummy_data_upy[0][4], 'WPA/WPA2-PSK')
        self.assertEqual(dummy_data_upy[0][5], False)

        # check second network
        self.assertEqual(dummy_data_upy[1][0], 'FRITZ!Box 7490')
        self.assertEqual(dummy_data_upy[1][1], '3810d517eb39')
        self.assertEqual(dummy_data_upy[1][2], 11)
        self.assertEqual(dummy_data_upy[1][3], -mocked_rssi[1])
        self.assertEqual(dummy_data_upy[1][4], 'WPA2-PSK')
        self.assertEqual(dummy_data_upy[1][5], False)

    def test__convert_scan_to_upy_format(self) -> None:
        """Test converting the dummy data to same style as Micropython"""
        # get two random values for RSSI in range of 0 to 100
        mocked_rssi = random.sample(range(0, 100), 2)

        # patch call of random.randint inside of _dummy_data with mocked_rssi
        with patch('random.randint') as mock_randint:
            mock_randint.side_effect = mocked_rssi
            dummy_data = NetworkHelper._dummy_data()

        dummy_data_upy = NetworkHelper._convert_scan_to_upy_format(data=dummy_data)

        self.assertIsInstance(dummy_data_upy, list)
        self.assertEqual(len(dummy_data_upy), 2)

        for net in dummy_data_upy:
            self.assertIsInstance(net, tuple)

        # check first network
        self.assertEqual(dummy_data_upy[0][0], 'TP-LINK_FBFC3C')
        self.assertEqual(dummy_data_upy[0][1], 'a0f3c1fbfc3c')
        self.assertEqual(dummy_data_upy[0][2], 1)
        self.assertEqual(dummy_data_upy[0][3], -mocked_rssi[0])
        self.assertEqual(dummy_data_upy[0][4], 'WPA/WPA2-PSK')
        self.assertEqual(dummy_data_upy[0][5], False)

        # check second network
        self.assertEqual(dummy_data_upy[1][0], 'FRITZ!Box 7490')
        self.assertEqual(dummy_data_upy[1][1], '3810d517eb39')
        self.assertEqual(dummy_data_upy[1][2], 11)
        self.assertEqual(dummy_data_upy[1][3], -mocked_rssi[1])
        self.assertEqual(dummy_data_upy[1][4], 'WPA2-PSK')
        self.assertEqual(dummy_data_upy[1][5], False)

    @unittest.skip("Not yet implemented")
    def test__gather_ifconfig_data(self) -> None:
        pass


class TestStation(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test__init__(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_active(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_connect(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_disconnect(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_isconnected(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_scan(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_status(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_ifconfig(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_config(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_connected(self) -> None:
        pass


class TestClient(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test__init__(self) -> None:
        ap = Client()

        self.assertIsNone(ap._bssid)
        self.assertIsNone(ap._authmode)
        self.assertIsNone(ap._password)
        self.assertIsNone(ap._channel)
        self.assertFalse(ap._active)

    @unittest.skip("Not yet implemented")
    def test_ifconfig(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test_config(self) -> None:
        pass


class TestWLAN(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test__init__(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
