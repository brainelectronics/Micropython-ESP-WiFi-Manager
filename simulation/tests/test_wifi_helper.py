#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of WiFi Helper"""

from nose2.tools import params
from typing import List, Union
import unittest
from unittest.mock import patch

# custom imports
from machine import machine
from wifi_helper import network
from wifi_helper import WifiHelper


class TestWifiHelper(unittest.TestCase):
    # Set maximum size of the assertion error message when Unit Test fail
    maxDiff = None

    def setUp(self) -> None:
        self.wh = WifiHelper()

        # activate WiFi before usage
        self.wh.station.active(True)

    def tearDown(self) -> None:
        self.wh.station.active(False)
        self.wh.station.connected = False

    def test__init(self) -> None:
        """Test initial values if WifiHelper"""
        wh = WifiHelper()

        required_keys = [
            'ssid', 'bssid', 'channel', 'RSSI', 'authmode', 'hidden'
        ]
        self.assertIsInstance(wh._scan_info, list)
        self.assertEqual(len(wh._scan_info), len(required_keys))
        self.assertTrue(all(name in required_keys for name in wh._scan_info))

        self.assertIsInstance(wh._network_list, list)
        self.assertEqual(len(wh._network_list), 0)

        self.assertIsInstance(wh._station, network.WLAN)

    def test__do_connect_connected(self) -> None:
        """
        Test _do_connect in case a SOFT_RESET occured and system is already
        connected to a network
        """
        # mock SOFT_RESET
        with patch('machine.machine.reset_cause') as mock_reset_cause:
            mock_reset_cause.return_value = machine.SOFT_RESET
            # mock already connected
            with patch('wifi_helper.network.Station.isconnected',
                       return_value=True):
                station = network.WLAN(network.STA_IF)
                result = WifiHelper._do_connect(station=station,
                                                ssid='qwertz',
                                                password=1234,
                                                timeout=10)
                self.assertEqual(result, True)

    @params(
        (10, 0.3),
        (10, 0.5),
        (10, 0.9)
    )
    def test__do_connect_unconnected(self, timeout: int, ratio: int) -> None:
        """
        Test _do_connect within a given timeout

        :param      timeout:  The timeout to wait for a successul connection
        :type       timeout:  int
        :param      ratio:    The ratio after which a connection is established
        :type       ratio:    int
        """
        # mock unknown reset cause
        with patch('machine.machine.reset_cause') as mock_reset_cause:
            mock_reset_cause.return_value = machine.UNKNOWN_RESET
            # mock not yet connected and change to success on second call
            # mock unconnected status for n calls
            side_effect_unconnected = [False] * int(timeout * 10 * ratio)
            side_effect_connected = [True] * int(timeout * 10 * (1 - ratio))
            side_effect = side_effect_unconnected + side_effect_connected
            with patch('wifi_helper.network.Station.isconnected',
                       side_effect=side_effect):
                station = network.WLAN(network.STA_IF)

                with patch.object(station, 'disconnect') as mock_disconnect:
                    result = WifiHelper._do_connect(station=station,
                                                    ssid='qwertz',
                                                    password=1234,
                                                    timeout=timeout)

                    mock_disconnect.assert_called_once()
                    self.assertEqual(result, True)

    @params(
        (1),
        (10),
        (20)
    )
    def test__do_connect_timeout(self, timeout: int) -> None:
        """
        Test _do_connect without a successful connection within a given timeout

        The device sleeps for 100ms after each connection check call, it is
        called 100 times at a timeout of 10 sec.

        Let connection timeout trigger and fail the connection

        :param      timeout:  The timeout to wait for a successul connection
        :type       timeout:  int
        """
        # mock unknown reset cause
        with patch('machine.machine.reset_cause') as mock_reset_cause:
            mock_reset_cause.return_value = machine.UNKNOWN_RESET
            # mock unconnected status for n+1 calls
            side_effect = [False] * (timeout * 10 + 1)

            with patch('wifi_helper.network.Station.isconnected',
                       side_effect=side_effect):
                station = network.WLAN(network.STA_IF)

                with patch.object(station, 'disconnect') as mock_disconnect:
                    result = WifiHelper._do_connect(station=station,
                                                    ssid='qwertz',
                                                    password=1234,
                                                    timeout=timeout)

                    mock_disconnect.assert_called_once()
                    self.assertEqual(result, False)

    @params(
        # single network, 10 sec timeout, no reconnection
        ('qwertz', 'asdf', 10, False),
        ('qwertz', 'asdf', 10, True),
    )
    def test_connect_already_connected(self,
                                       ssid: Union[None, List[str], str],
                                       password: Union[None, List[str], str],
                                       timeout: int,
                                       reconnect: bool) -> None:
        with patch('wifi_helper.network.Station.isconnected',
                   return_value=True):
            with patch('wifi_helper.network.Station.config',
                       return_value=ssid):
                if reconnect:
                    # check call of disonnect
                    with patch.object(network.Station,
                                      'disconnect') as mock_disconnect:
                        result = WifiHelper.connect(ssid=ssid,
                                                    password=password,
                                                    timeout=timeout,
                                                    reconnect=reconnect)
                        mock_disconnect.assert_called_once()
                else:
                    # only if no reconnection is required, function will return
                    result = WifiHelper.connect(ssid=ssid,
                                                password=password,
                                                timeout=timeout,
                                                reconnect=reconnect)
                self.assertEqual(result, True)

    def test_isconnected(self) -> None:
        is_connected = self.wh.isconnected
        self.assertFalse(is_connected)

        with patch('wifi_helper.network.Station.isconnected',
                   return_value=True):
            is_connected = self.wh.isconnected
            self.assertTrue(is_connected)

    def test_station(self) -> None:
        station = self.wh.station

        self.assertIsInstance(station, network.WLAN)

    @params(
        ('qwertz', '1234', 9, 10)
    )
    def test_create_ap(self,
                       ssid: str,
                       password: str,
                       channel: int,
                       timeout: int) -> None:
        """
        Test creation of an AccessPoint

        :param      ssid:      The ssid
        :type       ssid:      str
        :param      password:  The password
        :type       password:  str
        :param      channel:   The channel
        :type       channel:   int
        :param      timeout:   The timeout
        :type       timeout:   int
        """
        pass
        """
        client = network.WLAN(network.AP_IF)
        self.assertTrue(client.dummy())

        client.config(essid=ssid)
        print(client._essid)

        with patch.object(network.WLAN(2), 'dummy') as mock_dummy:
            client = network.WLAN(network.AP_IF)
            self.assertTrue(client.dummy())

            mock_dummy.return_value = False
            self.assertFalse(client.dummy())
        """

        """
        with patch.object(network.WLAN(2), 'dummy') as mock_essid:
            # result = WifiHelper.create_ap(ssid=ssid,
            #                               password=password,
            #                               channel=channel,
            #                               timeout=timeout)
            #
            # self.assertEqual(result, True)

            client = network.WLAN(network.AP_IF)
            self.assertTrue(client.dummy)

            # self.assertEqual(mock_essid._essid, ssid)
            # print(dir(mock_essid))
            # print(mock_essid.return_value)
        """

    def test_scan_info(self) -> None:
        expectation = [
            'ssid', 'bssid', 'channel', 'RSSI', 'authmode', 'hidden'
        ]

        result = self.wh.scan_info

        self.assertEqual(result, expectation)

    def test_auth_modes(self) -> None:
        expectation = {
            0: "open",
            1: "WEP",
            2: "WPA-PSK",
            3: "WPA2-PSK",
            4: "WPA/WPA2-PSK"
        }

        result = self.wh.auth_modes

        self.assertEqual(result, expectation)

    @unittest.skip("Checked by test_networks")
    def test_scan_networks(self) -> None:
        pass

    def test_networks(self) -> None:
        # perform scan
        self.wh.scan_networks()

        result = self.wh.networks

        print(result)

        self.assertIsInstance(result, list)

        # check networks have been found
        if len(result):
            for net in result:
                self.assertEqual(self.isinstance_namedtuple(net), True)
                scan_info = self.wh.scan_info.copy()
                scan_info.append('quality')
                self.assertEqual(list(net._fields), scan_info)

    @unittest.skip("Not yet implemented")
    def test_get_wifi_networks_sorted(self) -> None:
        pass

    @params(
        (-96, 8),   # dBm, percentage
    )
    def test_dbm_to_quality(self, dBm: int, expectation: int) -> None:
        result = self.wh.dbm_to_quality(dBm=dBm)
        self.assertEqual(result, expectation)

    @params(
        (50, -75),  # percentage, dBm
    )
    def test_quality_to_dbm(self, quality: int, expectation: int) -> None:
        result = self.wh.quality_to_dbm(quality=quality)
        self.assertEqual(result, expectation)

    def test_ifconfig_client(self) -> None:
        # fake a connection to a network
        self.wh.station.connected = True

        result = self.wh.ifconfig_client
        self.assertEqual(self.isinstance_namedtuple(result), True)
        self.assertEqual(list(result._fields),
                         ['ip', 'subnet', 'gateway', 'dns'])

    def test_ifconfig_ap(self) -> None:
        # fake a connection to a network
        self.wh.station.connected = True

        result = self.wh.ifconfig_client
        self.assertEqual(self.isinstance_namedtuple(result), True)
        self.assertEqual(list(result._fields),
                         ['ip', 'subnet', 'gateway', 'dns'])

    def isinstance_namedtuple(self, obj: tuple) -> bool:
        return (
            isinstance(obj, tuple) and
            hasattr(obj, '_asdict') and
            hasattr(obj, '_fields')
        )


if __name__ == '__main__':
    unittest.main()
