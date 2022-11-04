#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Fake Micropython network class

See https://docs.micropython.org/en/latest/library/network.html
"""

import netifaces
import random
import re
import socket
import subprocess
import sys
from typing import Any, List, Optional, Tuple, Union

STA_IF = 1
AP_IF = 2

AUTH_OPEN = 1
AUTH_WEP = 2
AUTH_WPA_PSK = 3
AUTH_WPA2_PSK = 4
AUTH_WPA_WPA2_PSK = 5


class NetworkHelper(object):
    """docstring for NetworkHelper"""
    def __init__(self):
        pass

    @staticmethod
    def _internal_scan() -> List[Tuple[Union[str, int]]]:
        """
        Wrapper around internal functions depending on the platform type

        :returns:   List of found networks as tuple
        :rtype:     List[Tuple[Union[str, int]]]
        """
        scan_result = list(dict())

        if sys.platform == "linux" or sys.platform == "linux2":
            scan_result = NetworkHelper._scan_linux()
        elif sys.platform == "darwin":
            scan_result = NetworkHelper._scan_mac()
        elif sys.platform == "win32":
            scan_result = NetworkHelper._scan_windows()
        else:
            scan_result = NetworkHelper._dummy_data()

        networks = NetworkHelper._convert_scan_to_upy_format(data=scan_result)

        return networks

    @staticmethod
    def _scan_linux() -> List[dict]:
        """
        Perform WiFi scan on Linux systems.

        This is currently not yet implemented, dummy data will be returned

        :returns:   List of found networks as dict
        :rtype:     List[dict]
        """
        return NetworkHelper._dummy_data()

    @staticmethod
    def _scan_mac() -> List[dict]:
        """
        Perform WiFi scan on Mac systems.

        Use command line interface of airport

        :returns:   List of found networks as dict
        :rtype:     List[dict]
        """
        scan_result = subprocess.check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '--scan'])  # noqa: E501

        if len(scan_result) == 0:
            return NetworkHelper._dummy_data()

        scan_result = [ele.decode('ascii') for ele in scan_result.splitlines()]
        # [
        #     b'                            SSID BSSID             RSSI CHANNEL HT CC SECURITY (auth/unicast/group)',   # noqa: E501
        #     b'                  TP-LINK_FBFC3C a0:f3:c1:fb:fc:3c -57  1,+1    Y  -- WPA(PSK/AES,TKIP/TKIP) WPA2(PSK/AES,TKIP/TKIP) ', # noqa: E501
        #     b'                  FRITZ!Box 7490 38:10:d5:17:eb:39 -56  1,+1    Y  DE WPA2(PSK/AES/AES) '   # noqa: E501
        # ]

        description = re.sub(' +', ' ', scan_result[0]).lstrip().split(' ')
        # [
        #   'SSID', 'BSSID', 'RSSI', 'CHANNEL', 'HT', 'CC', 'SECURITY',
        #   '(auth/unicast/group)'
        # ]

        indexes = dict()
        for kw in description[0:-1]:
            indexes[kw.lower()] = scan_result[0].index(kw)
        # {
        #     'ssid': 28,
        #     'bssid': 33,
        #     'rssi': 51,
        #     'channel': 56,
        #     'ht': 64,
        #     'cc': 67,
        #     'security': 70
        # }

        nets = list()
        for net in scan_result[1:]:
            info = dict()

            ssid_info = net[0:indexes['bssid']]
            info['ssid'] = ssid_info.rstrip().lstrip()

            bssid_info = net[indexes['bssid']:indexes['rssi']]
            info['bssid'] = bssid_info.rstrip().lstrip()

            rssi_info = net[indexes['rssi']:indexes['channel']]
            info['RSSI'] = int(rssi_info.rstrip().lstrip())

            channel_info = net[indexes['channel']:indexes['ht']]
            info['channel'] = int(channel_info.rstrip().lstrip().split(',')[0])

            ht_info = net[indexes['ht']:indexes['cc']]
            info['ht'] = ht_info.rstrip().lstrip()

            cc_info = net[indexes['cc']:indexes['security']]
            info['cc'] = cc_info.rstrip().lstrip()

            authmode_info = net[indexes['security']:]
            info['authmode'] = authmode_info.rstrip().lstrip()

            info['hidden'] = True if info['ht'] == "Y" else False

            nets.append(info)
            # {
            #     'ssid': 'FRITZ!Box 7490',
            #     'bssid': '38:10:d5:17:eb:39',
            #     'RSSI': -57,
            #     'channel': 1,
            #     'ht': 'Y',
            #     'cc': 'DE',
            #     'authmode': 'WPA2(PSK/AES/AES)',
            #     'hidden': True
            # }

        # [
        #     {
        #         'ssid': 'FRITZ!Box 7490',
        #         'bssid': '38:10:d5:17:eb:39',
        #         'RSSI': -57,
        #         'channel': 1,
        #         'ht': 'Y',
        #         'cc': 'DE',
        #         'authmode': 'WPA2(PSK/AES/AES)',
        #         'hidden': True,
        #         # 'quality': 86
        #     },
        #     {
        #         'ssid': 'TP-LINK_FBFC3C',
        #         'bssid': 'a0:f3:c1:fb:fc:3c',
        #         'RSSI': -57,
        #         'channel': 1,
        #         'ht': 'Y',
        #         'cc': '--',
        #         'authmode': 'WPA(PSK/AES,TKIP/TKIP) WPA2(PSK/AES,TKIP/TKIP)',
        #         'hidden': True
        #     }
        # ]

        return nets

    @staticmethod
    def _scan_windows() -> List[dict]:
        """
        Perform WiFi scan on Windows systems.

        Use command line interface of netsh.

        This function might fail on non english or german language systems

        :returns:   List of found networks as dict
        :rtype:     List[dict]
        """
        try:
            scan_result = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'networks', 'mode=bssid']
            )
        except Exception:
            return NetworkHelper._dummy_data()

        # netsh call returns report in local language, try to decode it
        try:
            scan_result = [
                ele.decode('cp850').lstrip() for ele in scan_result.splitlines()    # noqa: E501
            ]
        except Exception:
            return NetworkHelper._dummy_data()

        # [
        #     '',
        #     'Schnittstellenname : WLAN ', 'Momentan sind 2 Netzwerke sichtbar.',  # noqa: E501
        #     '',
        #     'SSID 1 : FRITZ!Box 7490',
        #     'Netzwerktyp             : Infrastruktur',
        #     'Authentifizierung       : WPA2-Personal',
        #     'Verschl▒sselung         : CCMP',
        #     'BSSIDD 1                 : 38:10:d5:17:eb:39',
        #     'Signal             : 83%  ',
        #     'Funktyp         : 802.11n',
        #     'Kanal           : 11 ',
        #     'Basisraten (MBit/s)   : 1 2 5.5 6 11 12 24',
        #     'Andere Raten (MBit/s) : 9 18 36 48 54', '',
        #     'SSID 2 : TP-LINK_FBFC3C',
        #     'Netzwerktyp             : Infrastruktur',
        #     'Authentifizierung       : WPA2-Personal',
        #     'Verschl▒sselung         : CCMP',
        #     'BSSIDD 1                 : a0:f3:c1:fb:fc:3c',
        #     'Signal             : 83%  ',
        #     'Funktyp         : 802.11n',
        #     'Kanal           : 1 ',
        #     'Basisraten (MBit/s)   : 1 2 5.5 11',
        #     'Andere Raten (MBit/s) : 6 9 12 18 24 36 48 54',
        #     ''
        # ]

        nets_tmp = list()
        this_net = list()
        active_net = False
        for idx, line in enumerate(scan_result):
            if line.startswith('SSID'):
                active_net = True

            if line == '':
                active_net = False
                if len(this_net):
                    nets_tmp.append(this_net.copy())
                this_net = list()

            if active_net:
                this_net.append(line)

        nets_parsed = list()
        for net in nets_tmp:
            info = dict()

            for ele in net:
                this_info = ele.split(':')
                key = this_info[0].lstrip().rstrip().lower()
                if len(this_info) > 2:
                    # bssid keyword
                    val = ':'.join(this_info[1:]).lstrip().rstrip()
                else:
                    val = this_info[1].lstrip().rstrip()
                info[key] = val

            nets_parsed.append(info)

        nets = list()
        for net in nets_parsed:
            info = dict()

            ssid_key = [
                ssid for ssid in net.keys() if ssid.startswith('ssid ')
            ][0]
            info['ssid'] = net[ssid_key]

            bssid_key = [
                bssid for bssid in net.keys() if bssid.startswith('bssidd ')
            ][0]
            info['bssid'] = net[bssid_key]

            quality = int(net['signal'][:-1])
            info['RSSI'] = NetworkHelper._quality_to_dbm(quality=quality)

            if 'channel' in net:
                # english system language
                info['channel'] = int(net['channel'])
            elif 'kanal' in net:
                # german system language
                info['channel'] = int(net['kanal'])
            else:
                # other system language
                info['channel'] = 1

            auth_key = [
                auth for auth in net.keys() if auth.startswith('auth')
            ][0]
            if len(auth_key):
                # german or english system language
                info['authmode'] = net[auth_key]
            else:
                # other system language
                info['authmode'] = 'WPA2-Dummy'

            info['hidden'] = False

            nets.append(info)
            # {
            #     'ssid': 'FRITZ!Box 7490',
            #     'bssid': '38:10:d5:17:eb:39',
            #     'RSSI': '87%',
            #     'channel': '11',
            #     'authmode': 'WPA2-Personal',
            #     'hidden': False
            # }

        # [
        #     {
        #         'ssid': 'FRITZ!Box 7490',
        #         'bssid': '38:10:d5:17:eb:39',
        #         'RSSI': '85%',
        #         'channel': '11',
        #         'authmode': 'WPA2-Personal',
        #         'hidden': False
        #     },
        #     {
        #         'ssid': 'TP-LINK_FBFC3C',
        #         'bssid': 'a0:f3:c1:fb:fc:3c',
        #         'RSSI': '83%',
        #         'channel': '1',
        #         'authmode': 'WPA2-Personal',
        #         'hidden': False
        #     }
        # ]

        return nets

    @staticmethod
    def _quality_to_dbm(quality: int) -> int:
        """
        Convert quality to dBm

        :param      quality:  The quality [0, 100]
        :type       quality:  int

        :returns:   dBm in range [-100, -50]
        :rtype:     int
        """
        # https://stackoverflow.com/questions/15797920/how-to-convert-wifi-signal-strength-from-quality-percent-to-rssi-dbm/30585711    # noqa: E501
        return min(max((quality / 2) - 100, -100), -50)

    @staticmethod
    def _dummy_data() -> List[dict]:
        """
        Get dummy WiFi scan data.

        RSSI value is fluctuating between 0 and 100

        :returns:   List of found networks as dict
        :rtype:     List[dict]
        """
        nets = [
            {
                'ssid': 'TP-LINK_FBFC3C',
                'RSSI': -random.randint(0, 100),
                'bssid': 'a0f3c1fbfc3c',
                'authmode': 'WPA/WPA2-PSK',
                'channel': 1,
                'hidden': False
            },
            {
                'ssid': 'FRITZ!Box 7490',
                'RSSI': -random.randint(0, 100),
                'bssid': '3810d517eb39',
                'authmode': 'WPA2-PSK',
                'channel': 11,
                'hidden': False
            }
        ]
        # print('Returning dummy data')

        return nets

    @staticmethod
    def _dummy_data_upy() -> List[list]:
        """
        Get dummy WiFi scan data in same style as Mircopython would return it

        :returns:   List of lists with scan data as reported on Micropython
        :rtype:     List[Union[str, int]]
        """
        dummy_data = NetworkHelper._dummy_data()
        nets_raw = NetworkHelper._convert_scan_to_upy_format(data=dummy_data)

        return nets_raw

    @staticmethod
    def _convert_scan_to_upy_format(data: List[dict]) -> List[Tuple[Union[str, int]]]:  # noqa: E501
        """
        Convert dummy data to raw data as Mircopython scan would return

        :param      data:  List of complete WiFi scan data
        :type       data:  List[dict]

        :returns:   List of tuples with scan data as reported on Micropython
        :rtype:     List[Tuple[Union[str, int]]]
        """
        raw_nets = list()

        for net in data:
            this_raw = (
                net['ssid'],
                net['bssid'],
                net['channel'],
                net['RSSI'],
                net['authmode'],
                net['hidden']
            )
            # (
            #     'FRITZ!Box 7490',
            #     '3810d517eb39',
            #     11,
            #     -random.randint(0, 100),
            #     'WPA2-PSK',
            #     False
            # )

            raw_nets.append(this_raw)

        return raw_nets

    @staticmethod
    def _gather_ifconfig_data() -> Tuple[str, str, str, str]:
        """
        Gather ifconfig data

        :returns:   fifconfig data in same style as Micropython would return it
        :rtype:     Tuple[str, str, str, str]
        """
        ip = '192.168.0.1'
        subnet = '255.255.255.0'
        gateway = '192.168.0.1'
        dns = '8.8.8.8'

        # get IP address
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
        except Exception:
            pass

        # get subnet
        try:
            addrs = netifaces.ifaddresses('en0')
            subnet = addrs[netifaces.AF_INET][0]['netmask']
        except Exception:
            pass

        # get gateway
        try:
            gws = netifaces.gateways()
            gateway = gws['default'][netifaces.AF_INET][0]
        except Exception:
            pass

        return (ip, subnet, gateway, dns)


class Station(NetworkHelper):
    """docstring for Station"""
    def __init__(self):
        self._connected = False
        self._active = False
        self._connected_network = None

    def active(self, is_active: Optional[bool] = None) -> Union[None, bool]:
        """
        Get/set WiFi status

        :param      is_active:  Flag to change state of WiFi
        :type       is_active:  Optional[bool]

        :returns:   State of WiFi interface
        :rtype:     Union[None, bool]
        """
        if is_active is not None:
            self._active = is_active
        else:
            return self._active

    def connect(self,
                service_id: str,
                key: Optional[str] = None,
                **kwargs) -> None:
        """
        Connect to a network

        :param      service_id:  The service identifier (BSSID/MAC address)
        :type       service_id:  str
        :param      key:         The key (password)
        :type       key:         Optional[str]
        :param      kwargs:      The keywords arguments
        :type       kwargs:      dictionary
        """
        # remember connected BSSID
        self._connected_network = service_id
        self.connected = True

    def disconnect(self) -> None:
        """Disconnect from network."""
        self.connected = False

    def isconnected(self) -> bool:
        """
        Get connection status

        :returns:   Flag whether device is connected to network or not
        :rtype:     bool
        """
        return self.connected

    def scan(self) -> List[Tuple[Union[str, int]]]:
        """
        Return WiFi scan data

        :returns:   List of tuples with discovered service parameters
        :rtype:     List[Tuple[Union[str, int]]]
        """
        return self._internal_scan()

    def status(self, param: Optional[str] = None) -> Union[str, int, tuple]:
        """
        Query dynamic status information of the interface

        :param      param:  The status parameter to retrieve
        :type       param:  Optional[str]

        :returns:   Status information
        :rtype:     Union[str, int, tuple]
        """
        if param is not None:
            return self.isconnected()
        else:
            pass

    def ifconfig(self,
                 value: Optional[Tuple[str, str, str, str]] = None) -> Union[None, Tuple[str, str, str, str]]:  # noqa: E501
        """
        Get/set IP-level network interface parameters

        :param      value:  The value to set
        :type       value:  Optional[Tuple[str, str, str, str]]

        :returns:   A 4-tuple with information about IO, subnet, gateway, DNS
        :rtype:     Union[None, Tuple[str, str, str, str]]
        """
        if value is not None:
            print('Change of ifconfig not supported')
        else:
            return self._gather_ifconfig_data()

    def config(self, param: str) -> Union[str, int]:
        """
        Get/set general network interface parameters

        :param      param:  The status parameter to set
        :type       param:  Optional[str]

        :returns:   Status information
        :rtype:     Union[str, int, tuple]
        """
        if param == 'essid':
            return self._connected_network
        else:
            pass

    @property
    def connected(self) -> bool:
        """
        Get connection status

        :returns:   Flag whether device is connected to network or not
        :rtype:     bool
        """
        return self._connected

    @connected.setter
    def connected(self, value: bool) -> None:
        """
        Set connection status

        :param      value:  The value
        :type       value:  bool
        """
        self._connected = value


class Client(NetworkHelper):
    """docstring for Client"""
    valid_kwargs = ['_essid', '_authmode', '_password', '_channel', '_active']

    def __init__(self):
        # for key in Client.valid_kwargs:
        #     setattr(self, key, None)

        self._essid = None
        self._authmode = None
        self._password = None
        self._channel = None
        self._active = None
        self._active = False

    def active(self, is_active: Optional[bool] = None) -> Union[None, bool]:
        """
        Get/set WiFi status

        :param      is_active:  Flag to change state of WiFi
        :type       is_active:  Optional[bool]

        :returns:   State of WiFi interface
        :rtype:     Union[None, bool]
        """
        if is_active is not None:
            self._active = is_active
        else:
            return self._active

    def ifconfig(self,
                 value: Optional[Tuple[str, str, str, str]] = None) -> Union[None, Tuple[str, str, str, str]]:  # noqa: E501
        """
        Get/set IP-level network interface parameters

        :param      value:  The value to set
        :type       value:  Optional[Tuple[str, str, str, str]]

        :returns:   A 4-tuple with information about IO, subnet, gateway, DNS
        :rtype:     Union[None, Tuple[str, str, str, str]]
        """
        if value is not None:
            print('Change of ifconfig not supported')
        else:
            return self._gather_ifconfig_data()

    def config(self, **kwargs) -> None:
        print('Config Accesspoint with: {}'.format(kwargs))
        for key, val in kwargs.items():
            key_name = '_{}'.format(key)
            if key_name not in Client.valid_kwargs:
                raise TypeError("Invalid keyword argument {}".format(key))
            print('Set {} to {}'.format(key_name, val))
            setattr(self, key_name, val)


class WLAN(object):
    """
    WLAN would inherit from Station and Client.

    Due to the diamond problem this hack fakes an inheritance of another object
    by trying to find the attribute in its child classes in case it has not
    been found in the parent class. The lookup is done in that class, which has
    been set as "true" child during the init.

    See https://en.wikipedia.org/wiki/Multiple_inheritance#The_diamond_problem
    """
    def __init__(self, val: int) -> None:
        self._type = None
        self._type_name = None

        if val == STA_IF:
            self._type = Station()
            self._type_name = STA_IF
        elif val == AP_IF:
            self._type = Client()
            self._type_name = AP_IF

    def __getattr__(self, item: Any) -> Any:
        if self._type_name == STA_IF:
            return super(Station, self._type).__getattribute__(item)
        elif self._type_name == AP_IF:
            return super(Client, self._type).__getattribute__(item)
        else:
            raise AttributeError("WLAN has no attribute '{}'".format(item))
