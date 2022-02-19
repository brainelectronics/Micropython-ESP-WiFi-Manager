#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Unittest of WiFi Manager"""

import logging
from nose2.tools import params
from pathlib import Path
import shutil
import tempfile
from typing import List, Union
import unittest
from unittest.mock import patch, mock_open

# custom imports
from .unittest_helper import UnitTestHelper
from generic_helper import GenericHelper
from generic_helper import Message
from led_helper import Neopixel     # Led
from machine import machine
from wifi_manager import WiFiManager
from wifi_helper import network
from wifi_helper import WifiHelper


class TestWiFiManager(unittest.TestCase):
    # Set maximum size of the assertion error message when Unit Test fail
    maxDiff = None

    def setUp(self) -> None:
        self.wm = WiFiManager(logger=None, quiet=False)
        self.uth = UnitTestHelper(quiet=False)

        # create a tmp directory
        # self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        self.wm.pixel.fading = False
        self.wm.scanning = False

        # shutil.rmtree(self.tmp_dir)

    def test__init__(self) -> None:
        self.assertIsInstance(self.wm.logger, logging.Logger)
        self.assertFalse(self.wm.logger.disabled)

        self.assertIsNotNone(self.wm._config_file)

        self.assertIsInstance(self.wm.wh, WifiHelper)
        self.assertIsInstance(self.wm.pixel, Neopixel)
        self.assertEqual(self.wm.pixel.color, [20, 20, 0])
        self.assertEqual(self.wm.pixel.intensity, 20)

        self.assertEqual(self.wm._enc_key, 'DEADBEEFDEADBEEF')
        self.assertEqual(len(self.wm._enc_key), 16)

        self.assertIsInstance(self.wm._configured_networks, list)
        self.assertEqual(len(self.wm._configured_networks), 0)

        self.assertEqual(self.wm._scan_interval, 5000)
        self.assertIsInstance(self.wm._scan_net_msg, Message)
        self.assertEqual(self.wm._scan_net_msg.value(), list())
        self.assertIsNone(self.wm._latest_scan)

        self.assertTrue(self.wm.scanning)

    @params(
        (
            'not-existing-file.json',   # path to config file
            [],                         # expected list of available networks
            False,                      # let connection not timeout
            False                       # expected function return value
        ),
        (
            'single-network.json',
            'MyNet',
            True,                   # let connection timeout
            False
        ),
        (
            'multi-network.json',
            ['SSID Name', 'Other-Network@1'],
            False,                  # let connection not timeout
            True
        ),
        (
            'multi-network.json',
            ['SSID Name', 'Other-Network@1'],
            True,                   # let connection timeout
            False
        )
    )
    def test_load_and_connect(self,
                              path: str,
                              network_definitions: Union[str, List[str]],
                              do_timeout: bool,
                              expectation: bool) -> None:
        """
        Test loading WiFi configuration from encrypted files and connecting to
        the specified network(s)

        :param      path:           Path to configuration file
        :type       path:           str
        :param      network_definitions:    Expected decrypted network names
        :type       network_definitions:    Union[str, List[str]]
        :param      do_timeout:     Let connect fail due to timeout
        :type       do_timeout:     bool
        :param      expectation:    Expected return value of connection to net
        :type       expectation:    bool
        """
        # overwrite config file path with given path
        file_path = self.uth.get_current_path() / 'data' / 'encrypted' / path
        self.wm._config_file = str(file_path)

        # mock unknown reset cause
        with patch('machine.machine.reset_cause') as mock_reset_cause:
            mock_reset_cause.return_value = machine.UNKNOWN_RESET
            # mock not yet connected and change to success on nth call
            # timeout is set to 5 sec by default, sleep time is 0.1 per call
            if do_timeout:
                # create list of all False with n entries
                # n = timeout(sec) * calls(sec) + calls before entering connect
                if isinstance(network_definitions, str):
                    side_effect = [False] * (int(5 * 1/0.1) + 1)
                elif isinstance(network_definitions, list):
                    side_effect = [False] * (int(5 * 1/0.1) + 2) * len(network_definitions)
                else:
                    raise TypeError('Expectation can only be string or list')
            else:
                # create list of results of the isconnected call
                # n = timeout(sec) * calls(sec) + calls before entering connect
                # mock unconnected status for first 5 calls (t = 0.5sec)
                return_unconnected = [False] * 5
                if isinstance(network_definitions, str):
                    return_connected = [True] * int(5 * 1/0.1)
                elif isinstance(network_definitions, list):
                    return_connected = [True] * int(5 * 1/0.1) * len(network_definitions)
                else:
                    raise TypeError('Expectation can only be string or list')
                side_effect = return_unconnected + return_connected
            with patch('wifi_helper.network.Station.isconnected',
                       side_effect=side_effect) as mock_isconnected:
                result = self.wm.load_and_connect()
                self.assertEqual(result, expectation)

        if result:
            self.assertEqual(self.wm.configured_networks, network_definitions)

    @unittest.skip("Not yet implemented to create an AccessPoint")
    def test_start_config(self) -> None:
        pass

    def test__add_app_routes(self) -> None:
        expectation = [
            '/',
            '/remove_wifi_config',
            '/save_wifi_config',
            '/wifi_selection',
            '/wifi_configs',
            '/scan_result',
            '/static/<path:filename>',
        ]
        for rule in self.wm.app.url_map.iter_rules():
            self.assertIn("{}".format(rule), expectation)

    @params(
        (
            'hello',
            b''',\xddZ\xa2\x16\xf3p\xd3D\xc1\x9cqN\xc2\xb7-'''
        ),
        (
            [True, 'val'],
            b'''`\x99\xd4\xcdU\xbf\x90\x8e\x16J\xa6\xc6\x18\x1b-J'''
        ),
        (
            {'some': True, 'val': 123},
            b'''ib\x03\xb5\x8a\xc1}QS\xfd\x1dl,\x80d\xcb/\xe1\xb6G\xe4]\x9c\xee\x84\xb1U\xaa#\x97\x93\xb6'''
        ),
        # single network
        (
            {"ssid": "MyNet", "password": "empty"},
            b'''E\xcd\xc6\xa4\xbc4\x05(\xc96\xf4\xa9\xf7\x83\x83\xb7\x08u\x94\xa6bn\xbf|\x19\xd5\xd2\xff\xddw\tGw\x9f\xda\xc6\xa3\xe1\x9b\x16F\xa2~ 1\xa1Z\x19'''
        ),
        # multi network
        (
            [{"ssid": "SSID Name", "password": "1234qwertz@"}, {"ssid": "Other-Network@1", "password": "password"}],
            b'''=\xd0B\xa4\xad\xc5\xbd\x07]\x0cI\x1a\xe1\x0c\xe2\x06\xe6V\xf3\x82\x8a\x83xx\xea\x13D:\xd9c\xab\x0e53\xbc1-Jo\xbb\xfb\xf4M\xd9x\xbbn;j\x10\xa63\xe9b\xbeE\x19\x8czmD\xfb\xbe\xecl\xd8\xce,\xddJ:4\\\xc1ds\xc5_\x91\x85\x16\xce$@\xab+\x9b\xf3\xe4z\xdc\xa6\xce~\x82b\x01\x83\x8b\xe4lD\x8f\xad\xc2h\xce\xeaM\xa3Y)'''
        )
    )
    def test__encrypt_data(self,
                           data: Union[str, list, dict],
                           expectation: bytes) -> None:
        """
        Test encryption of data

        :param      data:           The data
        :type       data:           Union[str, list, dict]
        :param      expectation:    Expected encrypted data as bytes
        :type       expectation:    bytes
        """
        result = self.wm._encrypt_data(data=data)

        self.assertEqual(result, expectation)

    @params(
        (
            b''',\xddZ\xa2\x16\xf3p\xd3D\xc1\x9cqN\xc2\xb7-''',
            None,
            'hello'
        ),
        (
            b'''`\x99\xd4\xcdU\xbf\x90\x8e\x16J\xa6\xc6\x18\x1b-J''',
            None,
            "[True, 'val']"
        ),
        (
            b'''ib\x03\xb5\x8a\xc1}QS\xfd\x1dl,\x80d\xcb/\xe1\xb6G\xe4]\x9c\xee\x84\xb1U\xaa#\x97\x93\xb6''',
            None,
            "{'some': True, 'val': 123}"
        ),
        (
            b'',
            'single-network.json',
            {"ssid": "MyNet", "password": "empty"}
        ),
        (
            b'',
            'multi-network.json',
            [{"ssid": "SSID Name", "password": "1234qwertz@"}, {"ssid": "Other-Network@1", "password": "password"}]
        )
    )
    def test__decrypt_data(self,
                           data: bytes,
                           file_path: str,
                           expectation: str) -> None:
        """
        Test decryption of data

        :param      data:           The data
        :type       data:           bytes
        :param      file_path:      Path to file to decrypt
        :type       file_path:      str
        :param      expectation:    Expected encrypted data as bytes
        :type       expectation:    bytes
        """
        if file_path:
            path = self.uth.get_current_path() / 'data' / 'encrypted'
            file_path = str(path / file_path)

            data = b''
            with open(file_path, 'rb') as file:
                data = file.read()

            result = self.wm._decrypt_data(data=data)
            result = GenericHelper.str_to_dict(data=result)
        else:
            result = self.wm._decrypt_data(data=data)

        self.assertEqual(result, expectation)

    @params(
        # test extension of unexisting network config file with new networks
        # extend single network with single new network
        (
            'not-existing-file.json',   # path to file to be extended
            {"ssid": "new_network", "password": "some_password"},   # new net
            ["new_network"],            # expected known networks
            {"ssid": "new_network", "password": "some_password"},   # expected file content
            False                       # file is not encrypted
        ),
        (
            'not-existing-file.json',
            {"ssid": "new_network", "password": "some_password"},
            ["new_network"],
            {"ssid": "new_network", "password": "some_password"},
            True
        ),

        # test extension of unexisting network config file with new networks
        # extend single network with multiple new networks
        (
            'not-existing-file.json',
            [
                {"ssid": "SSID Name", "password": "1234qwertz@"},
                {"ssid": "Other-Network@1", "password": "password"}
            ],
            ["SSID Name", "Other-Network@1"],
            [
                {"ssid": "SSID Name", "password": "1234qwertz@"},
                {"ssid": "Other-Network@1", "password": "password"}
            ],
            False
        ),
        (
            'not-existing-file.json',
            [
                {"ssid": "SSID Name", "password": "1234qwertz@"},
                {"ssid": "Other-Network@1", "password": "password"}
            ],
            ["SSID Name", "Other-Network@1"],
            [
                {"ssid": "SSID Name", "password": "1234qwertz@"},
                {"ssid": "Other-Network@1", "password": "password"}
            ],
            True
        ),

        # test extension of existing network config file with new networks
        # extend single network with single new network
        (
            'single-network.json',
            {"ssid": "SSID Name", "password": "1234qwertz@"},
            ["MyNet", "SSID Name"],
            [
                {"ssid": "MyNet", "password": "empty"},
                {"ssid": "SSID Name", "password": "1234qwertz@"}
            ],
            False
        ),
        (
            'single-network.json',
            {"ssid": "SSID Name", "password": "1234qwertz@"},
            ["MyNet", "SSID Name"],
            [
                {"ssid": "MyNet", "password": "empty"},
                {"ssid": "SSID Name", "password": "1234qwertz@"}
            ],
            True
        ),

        # test extension of existing network config file with new networks
        # extend single network with multiple new networks
        (
            'single-network.json',
            [
                {"ssid": "SSID Name", "password": "1234qwertz@"},
                {"ssid": "Other-Network@1", "password": "password"}
            ],
            ["MyNet", "SSID Name", "Other-Network@1"],
            [
                {"ssid": "MyNet", "password": "empty"},
                {"ssid": "SSID Name", "password": "1234qwertz@"},
                {"ssid": "Other-Network@1", "password": "password"}
            ],
            False
        ),
        (
            'single-network.json',
            [
                {"ssid": "SSID Name", "password": "1234qwertz@"},
                {"ssid": "Other-Network@1", "password": "password"}
            ],
            ["MyNet", "SSID Name", "Other-Network@1"],
            [
                {"ssid": "MyNet", "password": "empty"},
                {"ssid": "SSID Name", "password": "1234qwertz@"},
                {"ssid": "Other-Network@1", "password": "password"}
            ],
            True
        ),

        # test extension of existing network config file with new networks
        # extend multiple networks with single new network
        (
            'multi-network.json',
            {"ssid": "new_net_1", "password": "password_1"},
            ["SSID Name", "Other-Network@1", "new_net_1"],
            [
                {"ssid": "SSID Name", "password": "1234qwertz@"},
                {"ssid": "Other-Network@1", "password": "password"},
                {"ssid": "new_net_1", "password": "password_1"}
            ],
            False
        ),

        (
            'multi-network.json',
            {"ssid": "new_net_1", "password": "password_1"},
            ["SSID Name", "Other-Network@1", "new_net_1"],
            [
                {"ssid": "SSID Name", "password": "1234qwertz@"},
                {"ssid": "Other-Network@1", "password": "password"},
                {"ssid": "new_net_1", "password": "password_1"}
            ],
            True
        ),

        # test extension of existing network config file with new networks
        # extend multiple networks with multiple new networks
        (
            'multi-network.json',
            [
                {"ssid": "new_net_1", "password": "password_1"},
                {"ssid": "new_net_2", "password": "password_2"}
            ],
            ["SSID Name", "Other-Network@1", "new_net_1", "new_net_2"],
            [
                {"ssid": "SSID Name", "password": "1234qwertz@"},
                {"ssid": "Other-Network@1", "password": "password"},
                {"ssid": "new_net_1", "password": "password_1"},
                {"ssid": "new_net_2", "password": "password_2"}
            ],
            False
        ),
        (
            'multi-network.json',
            [
                {"ssid": "new_net_1", "password": "password_1"},
                {"ssid": "new_net_2", "password": "password_2"}
            ],
            ["SSID Name", "Other-Network@1", "new_net_1", "new_net_2"],
            [
                {"ssid": "SSID Name", "password": "1234qwertz@"},
                {"ssid": "Other-Network@1", "password": "password"},
                {"ssid": "new_net_1", "password": "password_1"},
                {"ssid": "new_net_2", "password": "password_2"}
            ],
            True
        ),
    )
    def test_extend_wifi_config_data(self,
                                     file_path: str,
                                     data: Union[dict, List[dict]],
                                     expected_networks: list,
                                     expected_file_content: Union[dict,
                                                                  List[dict]],
                                     is_encrypted: bool) -> None:
        root_path = self.uth.get_current_path() / 'data'
        if is_encrypted:
            path = str(root_path / 'encrypted' / file_path)
        else:
            path = str(root_path / 'unencrypted' / file_path)

        # more efficient to create temporary directory here, than in setUp
        tmp_dir = tempfile.mkdtemp()
        print('Using tmp directory at: {}'.format(tmp_dir))

        if Path(path).exists():
            print('Copied {} to {}'.format(file_path, tmp_dir))
            shutil.copy(src=path, dst=tmp_dir)

            # pre-load existing networks
            pre_known_nets = list()

            if isinstance(data, dict):
                if isinstance(expected_file_content, dict):
                    pass
                elif isinstance(expected_file_content, list):
                    for net in expected_file_content:
                        if net is not data:
                            pre_known_nets.append(net['ssid'])
            elif isinstance(data, list):
                if isinstance(expected_file_content, dict):
                    for net in data:
                        if net is not expected_file_content:
                            pre_known_nets.append(net['ssid'])
                elif isinstance(expected_file_content, list):
                    for net in expected_file_content:
                        if net not in data:
                            pre_known_nets.append(net['ssid'])

            print('Pre known nets: {}'.format(pre_known_nets))
            self.wm._configured_networks = pre_known_nets

        path = str(Path(tmp_dir) / file_path)
        print('Play with file at {}'.format(path))

        self.wm.extend_wifi_config_data(data=data,
                                        path=path,
                                        encrypted=is_encrypted)
        self.assertEqual(self.wm.configured_networks, expected_networks)

        self.assertTrue(Path(path).exists())

        saved_data = self.wm._load_wifi_config_data(path=path,
                                                    encrypted=is_encrypted)
        self.assertEqual(saved_data, expected_file_content)

        shutil.rmtree(tmp_dir)
        print('Deleted tmp directory: {}'.format(tmp_dir))

        """
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
        """

    @params(
        (
            'single-network.json',                  # path to config file
            False,                                  # data encrypted
            {"ssid": "MyNet", "password": "empty"}  # expectation
        ),
        (
            'multi-network.json',
            False,
            [
                {"ssid": "SSID Name", "password": "1234qwertz@"},
                {"ssid": "Other-Network@1", "password": "password"}
            ]
        ),
        (
            'single-network.json',
            True,
            {"ssid": "MyNet", "password": "empty"}
        ),
        (
            'multi-network.json',
            True,
            [
                {"ssid": "SSID Name", "password": "1234qwertz@"},
                {"ssid": "Other-Network@1", "password": "password"}
            ]
        ),
    )
    def test__load_wifi_config_data(self,
                                    path: str,
                                    encrypted: bool,
                                    expectation: Union[dict,
                                                       List[dict]]) -> None:
        """
        Test loading WiFi config data from existing files

        :param      path:           Path to file
        :type       path:           str
        :param      encrypted:      Flag whether file is encrypted
        :type       encrypted:      bool
        :param      expectation:    Expected encrypted data as bytes
        :type       expectation:    Union[dict, List[dict]]
        """
        root_path = self.uth.get_current_path() / 'data'
        if encrypted:
            path = str(root_path / 'encrypted' / path)
        else:
            path = str(root_path / 'unencrypted' / path)

        result = self.wm._load_wifi_config_data(path=path, encrypted=encrypted)

        self.assertEqual(result, expectation)

    @unittest.skip("Tested with test_load_and_connect")
    def test_configured_networks(self) -> None:
        pass

    @unittest.skip("Not yet implemented")
    def test__scan(self) -> None:
        pass

    @params(
        (
            10,     # desired value
            1000    # expected value
        ),
        (
            1000,
            1000
        ),
        (
            1001,
            1001
        ),
        (
            'test',
            5000
        ),
        (
            1234.5,
            5000
        )
    )
    def test_scan_interval(self, value: int, expectation: int) -> None:
        self.wm.scan_interval = value
        self.assertEqual(self.wm.scan_interval, expectation)

    @unittest.skip("Not yet implemented")
    def test_scanning(self) -> None:
        pass

    def test_latest_scan(self) -> None:
        required_keys = [
            'ssid', 'RSSI', 'bssid', 'authmode', 'quality', 'channel', 'hidden'
        ]

        # get dummy data as expectation
        self.wm.wh.scan_networks()
        expectation = self.wm.wh.get_wifi_networks_sorted()

        # set latest Message content as expectation
        self.wm._scan_net_msg.set(expectation)

        result = self.wm.latest_scan

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        for ele in result:
            self.assertIsInstance(ele, dict)
            for key in ele.keys():
                self.assertIn(key, required_keys)

    @unittest.skip("Function only works while Flask app is running")
    def test_scan_result(self) -> None:
        pass

    @unittest.skip("Function only works while Flask app is running")
    def test_wifi_selection(self) -> None:
        pass

    @unittest.skip("Function only works while Flask app is running")
    def test_wifi_configs(self) -> None:
        pass

    @unittest.skip("Function only works while Flask app is running")
    def test_save_wifi_config(self):
        pass

    @unittest.skip("Not yet implemented")
    @params(
        (
            {'bssid': 'a0f3c1fbfc3c', 'ssid': '', 'password': 'qwertz1234@'},
            {'ssid': 'TP-LINK_FBFC3C', 'password': 'qwertz1234@'}
        ),
        (
            {'bssid': '3810d517eb39', 'ssid': '', 'password': 'easy'},
            {'ssid': 'FRITZ!Box 7490', 'password': 'easy'}
        ),
        (
            {'ssid': 'TP-LINK_FBFC3C', 'password': 'nopw_needed1'},
            {'ssid': 'TP-LINK_FBFC3C', 'password': 'nopw_needed1'}
        ),
        (
            {'ssid': 'FRITZ!Box 7490', 'password': ''},
            {'ssid': 'FRITZ!Box 7490', 'password': ''}
        ),
        (
            # unknown (not in latest scan) BSSID given
            {'bssid': 'unknown', 'ssid': '', 'password': 'something'},
            {'password': 'something'}
        ),
        (
            # unknown (not in latest scan) SSID given
            {'ssid': 'unknown', 'password': 'something'},
            {'ssid': 'unknown', 'password': 'something'}
        )
    )
    def test__save_wifi_config(self,
                               form_data: dict,
                               expectation: dict) -> None:
        result = self.wm._save_wifi_config(form_data=form_data)
        self.assertIsInstance(result, dict)
        self.assertEqual(result, expectation)

    @unittest.skip("Function only works while Flask app is running")
    def test_remove_wifi_config(self):
        pass

    @unittest.skip("Not yet implemented")
    def test__remove_wifi_config(self):
        pass

    @unittest.skip("Function only works while Flask app is running")
    def test_run(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
