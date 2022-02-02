#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""connect to specified network(s) or create an accesspoint"""

# import ubinascii
import json
# import network
from . import network
import time
from collections import namedtuple

# from .time_helper import TimeHelper

# not natively supported on micropython, see lib/typing.py
from typing import (List, NamedTuple, Union)


class WifiHelper(object):
    """docstring for WifiHelper"""
    def __init__(self):
        self._scan_info = ['ssid', 'bssid', 'channel', 'RSSI', 'authmode', 'hidden']
        self._auth_modes = {
            0: "open",
            1: "WEP",
            2: "WPA-PSK",
            3: "WPA2-PSK",
            4: "WPA/WPA2-PSK"
        }
        self._network_list = list()
        self._station = network.WLAN(network.STA_IF)

    @staticmethod
    def _do_connect(station: network.WLAN,
                    ssid: str,
                    password: str,
                    timeout: int) -> bool:
        """
        Establish the network connection.

        :param      station:   The network object
        :type       station:   network.WLAN
        :param      ssid:      The SSID of the network to connect to
        :type       ssid:      str
        :param      password:  The password of the network
        :type       password:  str
        :param      timeout:   Seconds to establish a connection to the network
        :type       timeout:   int, optional

        :returns:   Result of connection
        :rtype:     bool
        """
        is_successfull = False

        # noting implemented here
        is_successfull = True

        return is_successfull

    @staticmethod
    def connect(ssid: Union[None, List[str], str] = None,
                password: Union[None, List[str], str] = None,
                networks: Union[dict, None] = None,
                timeout: int = 5,
                reconnect: bool = False) -> bool:
        """
        Connect to the configured network

        :param      ssid:      The SSID of the network to connect to
        :type       ssid:      list or str
        :param      password:  The password of the network
        :type       password:  list or str
        :param      networks:  Networks and passwords
        :type       networks:  dict, optional
        :param      timeout:   Seconds to establish a connection to the network
        :type       timeout:   int, optional
        :param      reconnect: Reconnect/disconnect from active connection
        :type       reconnect: bool, optional

        :returns:   Result of connection
        :rtype:     bool
        """
        is_connected = False

        # noting implemented here
        is_connected = True

        return is_connected

    @property
    def isconnected(self) -> bool:
        """
        Return whether device is connected as client to a network

        :returns:   Result of connection status
        :rtype:     bool
        """
        # configure the WiFi as station mode (client)
        station = self.station
        return station.isconnected()

    @property
    def station(self):
        """
        Return WiFi network station aka client interface object

        :returns:   WiFi network station aka client interface object
        :rtype:     WLAN
        """
        return self._station

    @staticmethod
    def create_ap(ssid: str,
                  password: str = '',
                  channel: int = 11,
                  timeout: int = 5) -> bool:
        """
        Create an Accesspoint

        :param      ssid:      The SSID of the network to create
        :type       ssid:      str
        :param      password:  The password of the accesspoint
        :type       password:  str, optional
        :param      channel:   The channel of the accesspoint
        :type       channel:   int, optional
        :param      timeout:   Seconds to create an accesspoint
        :type       timeout:   int, optional

        :returns:   Result of connection
        :rtype:     bool
        """
        is_successfull = True

        # noting implemented here

        return is_successfull

    @property
    def scan_info(self) -> list:
        """
        Get WiFi scan informations.

        :returns:   WiFi scan properties
        :rtype:     list
        """
        return self._scan_info

    @property
    def auth_modes(self) -> dict:
        """
        Get authentication modes.

        :returns:   Supported authentication modes
        :rtype:     dict
        """
        return self._auth_modes

    def scan_networks(self) -> None:
        """
        Scan for available WiFi networks and return found networks.

        :param      sort_key:  The sort key
        :type       sort_key:  str, optional

        :returns:   The WiFi networks
        :rtype:     List[dict]
        """
        station = self.station

        # activate WiFi if not yet enabled
        if not station.active():
            station.active(True)

        # scan for available networks
        found_networks = list()
        try:
            found_networks = station.scan()
            if not len(found_networks):
                station.active(False)
        except RuntimeError:
            print('RuntimeError during scan')
            # no access points were found.
            # RuntimeError: Wifi Unknown Error 0x0102
        except Exception as e:
            print('Unknown exception: {}'.format(e))

        # create dict based on scan_info and found networks
        self._network_list = [dict(zip(self.scan_info, x)) for x in found_networks]

        for net in self._network_list:
            net['quality'] = self.dbm_to_quality(dBm=net['RSSI'])
            if 'authmode' in net:
                try:
                    net['authmode'] = self.auth_modes[net['authmode']]
                except KeyError:
                    print('{} is unknown authmode'.format(net['authmode']))
                except Exception:
                    pass
            if 'bssid' in net:
                try:
                    # net['bssid'] = ubinascii.hexlify(net['bssid'])
                    net['bssid'] = net['bssid']
                except Exception:
                    pass

    @property
    def networks(self) -> List[NamedTuple]:
        """
        Get list of available networks

        :returns:   List of NamedTuple networks
        :rtype:     List[NamedTuple]
        """
        return [namedtuple('net', list(net.keys()))(*net.values()) for net in self._network_list]

    def get_wifi_networks_sorted(self,
                                 rescan: bool = False,
                                 scan_if_empty: bool = False,
                                 as_json: bool = False,
                                 sort_key: str = 'RSSI') -> Union[List[dict], str]:
        """
        Get the available WiFi networks in sorted order.

        :param      rescan:         Flag to scan before returning result
        :type       rescan:         bool
        :param      scan_if_empty:  Flag to scan if network list is empty
        :type       scan_if_empty:  bool
        :param      as_json:        Flag to return data as json string
        :type       as_json:        bool
        :param      sort_key:       The sort key
        :type       sort_key:       str

        :returns:   The available WiFi networks in sorted order.
        :rtype:     Union[List[dict], str]
        """
        if (scan_if_empty and not len(self.networks)) or rescan:
            self.scan_networks()

        if not (sort_key in self.scan_info):
            sort_key = 'RSSI'

        # sort list by specified sort_key
        sorted(self._network_list, key=lambda k: k[sort_key])

        if as_json:
            return json.dumps(self._network_list)
        else:
            return self._network_list

    @staticmethod
    def dbm_to_quality(dBm: int) -> int:
        """
        Convert dBm to quality

        :param      dBm:  The dBm [-100, -50]
        :type       dBm:  int

        :returns:   Quality index in percent [0, 100]
        :rtype:     int
        """
        # https://stackoverflow.com/questions/15797920/how-to-convert-wifi-signal-strength-from-quality-percent-to-rssi-dbm/30585711
        """
        quality = 0
        if dBm <= -100:
            # very bad signal
            quality = 0
        elif dBm >= -50:
            quality = 100
        else:
            quality = 2 * (dBm + 100)

        return quality
        """
        return min(max(2 * (dBm + 100), 0), 100)

    @staticmethod
    def quality_to_dbm(quality: int) -> int:
        """
        Convert quality to dBm

        :param      quality:  The quality [0, 100]
        :type       quality:  int

        :returns:   dBm in range [-100, -50]
        :rtype:     int
        """
        # https://stackoverflow.com/questions/15797920/how-to-convert-wifi-signal-strength-from-quality-percent-to-rssi-dbm/30585711
        """
        dBm = 0
        if quality <= 0:
            # very bad signal
            dBm = -100
        elif quality >= 100:
            dBm = -50
        else:
            dBm = (quality / 2) - 100

        return dBm
        """
        return min(max((quality / 2) - 100, -100), -50)

    @property
    def ifconfig_client(self):
        """
        Get current network interface parameters of the client

        :returns:   WiFi or general network informations
        :rtype:     NamedTuple
        """
        empty_config = ('0.0.0.0', '0.0.0.0', '0.0.0.0', '0.0.0.0')
        _ifconfig = namedtuple('ifconfig', ('ip', 'subnet', 'gateway', 'dns'))
        station = self.station

        if station.active() and station.isconnected():
            return _ifconfig(*station.ifconfig())
        else:
            return _ifconfig(*empty_config)

    @property
    def ifconfig_ap(self):
        """
        Get current network interface parameters of the accesspoint

        :returns:   WiFi or general network informations
        :rtype:     NamedTuple
        """
        _ifconfig = namedtuple('ifconfig', ('ip', 'subnet', 'gateway', 'dns'))
        ap = network.WLAN(network.AP_IF)

        return _ifconfig(*ap.ifconfig())
