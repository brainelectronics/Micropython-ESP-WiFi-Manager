#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import netifaces
import random
import re
import socket
import subprocess
from sys import platform
from typing import List, Optional, Tuple, Union

STA_IF = 1
AP_IF = 2


class NetworkHelper(object):
    """docstring for Common"""
    def __init__(self):
        pass

    @staticmethod
    def _internal_scan() -> list:
        networks = list()

        if platform == "linux" or platform == "linux2":
            networks = NetworkHelper._scan_linux()
        elif platform == "darwin":
            networks = NetworkHelper._scan_mac()
        elif platform == "win32":
            networks = NetworkHelper._scan_windows()

        return networks

    @staticmethod
    def _convert_dummy_data_to_raw(data: List[dict]) -> List[list]:
        raw_nets = list()

        for net in data:
            this_raw = [
                net['ssid'],
                net['bssid'],
                net['channel'],
                net['RSSI'],
                net['authmode'],
                net['hidden']
            ]
            # [
            #     'FRITZ!Box 7490',
            #     '3810d517eb39',
            #     11,
            #     -random.randint(0, 100),
            #     'WPA2-PSK',
            #     False
            # ]

            raw_nets.append(this_raw)

        return raw_nets

    @staticmethod
    def _scan_mac() -> List[dict]:
        scan_result = subprocess.check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '--scan'])

        if len(scan_result) == 0:
            print('### Check WiFi to be active ###')
            print('Returning dummy data')
            return NetworkHelper._dummy_data_raw()

        scan_result = [ele.decode('ascii') for ele in scan_result.splitlines()]
        # print('scan_result: {}'.format(scan_result))
        # [
        #     b'                            SSID BSSID             RSSI CHANNEL HT CC SECURITY (auth/unicast/group)',
        #     b'                  TP-LINK_FBFC3C a0:f3:c1:fb:fc:3c -57  1,+1    Y  -- WPA(PSK/AES,TKIP/TKIP) WPA2(PSK/AES,TKIP/TKIP) ',
        #     b'                  FRITZ!Box 7490 38:10:d5:17:eb:39 -56  1,+1    Y  DE WPA2(PSK/AES/AES) '
        # ]

        description = re.sub(' +', ' ', scan_result[0]).lstrip().split(' ')
        # print('description: {}'.format(description))
        # [
        #   'SSID', 'BSSID', 'RSSI', 'CHANNEL', 'HT', 'CC', 'SECURITY',
        #   '(auth/unicast/group)'
        # ]

        indexes = dict()
        for kw in description[0:-1]:
            indexes[kw.lower()] = scan_result[0].index(kw)
        # print('indexes: {}'.format(indexes))
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

            # info['quality'] = dbm_to_quality(dBm=info['RSSI'])

            nets.append(info)
            # print('info: {}'.format(info))
            # {
            #     'ssid': 'FRITZ!Box 7490',
            #     'bssid': '38:10:d5:17:eb:39',
            #     'RSSI': -57,
            #     'channel': 1,
            #     'ht': 'Y',
            #     'cc': 'DE',
            #     'authmode': 'WPA2(PSK/AES/AES)',
            #     'hidden': True,
            #     # 'quality': 86
            # }

        # print('nets: {}'.format(nets))
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
        #         'hidden': True,
        #         # 'quality': 86
        #     }
        # ]

        return NetworkHelper._convert_dummy_data_to_raw(data=nets)

    @staticmethod
    def _scan_windows() -> List[dict]:
        try:
            scan_result = subprocess.check_output(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'])
        except Exception as e:
            print('### Check WiFi to be active ###')
            print('Returning dummy data')
            return NetworkHelper._dummy_data_raw()

        scan_result = [ele.decode('cp850').lstrip() for ele in scan_result.splitlines()]
        # print(scan_result)
        # [
        #     '',
        #     'Schnittstellenname : WLAN ', 'Momentan sind 2 Netzwerke sichtbar.',
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
                    val = ':'.join(this_info[1:]).lstrip().rstrip()
                else:
                    val = this_info[1].lstrip().rstrip()
                info[key] = val

            nets_parsed.append(info)

        nets = list()
        for net in nets_parsed:
            info = dict()

            ssid_key = [ssid for ssid in net.keys() if ssid.startswith('ssid ')][0]
            info['ssid'] = net[ssid_key]

            bssid_key = [bssid for bssid in net.keys() if bssid.startswith('bssidd ')][0]
            info['bssid'] = net[bssid_key]

            quality = int(net['signal'][:-1])
            info['RSSI'] = NetworkHelper._quality_to_dbm(quality=quality)

            info['channel'] = int(net['kanal'])

            info['ht'] = '???'

            info['cc'] = '???'

            auth_key = [auth for auth in net.keys() if auth.startswith('auth')][0]
            info['authmode'] = net[auth_key]

            info['hidden'] = False

            nets.append(info)
            # print('info: {}'.format(info))
            # {
            #     'ssid': 'FRITZ!Box 7490',
            #     'bssid': '38:10:d5:17:eb:39',
            #     'RSSI': '87%',
            #     'channel': '11',
            #     'ht': '???',
            #     'cc': 'WAP',
            #     'authmode': 'WPA2-Personal',
            #     'hidden': False
            # }

        # print('nets: {}'.format(nets))
        # [
        #     {
        #         'ssid': 'FRITZ!Box 7490',
        #         'bssid': '38:10:d5:17:eb:39',
        #         'RSSI': '85%',
        #         'channel': '11',
        #         'ht': '???',
        #         'cc': '???',
        #         'authmode': 'WPA2-Personal',
        #         'hidden': False
        #     },
        #     {
        #         'ssid': 'TP-LINK_FBFC3C',
        #         'bssid': 'a0:f3:c1:fb:fc:3c',
        #         'RSSI': '83%',
        #         'channel': '1',
        #         'ht': '???',
        #         'cc': '???',
        #         'authmode': 'WPA2-Personal',
        #         'hidden': False
        #     }
        # ]

        return NetworkHelper._convert_dummy_data_to_raw(data=nets)

    @staticmethod
    def _quality_to_dbm(quality: int) -> int:
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

    @staticmethod
    def _scan_linux() -> List[dict]:
        return NetworkHelper._dummy_data_raw()

    @staticmethod
    def _dummy_data() -> List[dict]:
        nets = [
            {
                'ssid': 'TP-LINK_FBFC3C',
                'RSSI': -random.randint(0, 100),
                'bssid': 'a0f3c1fbfc3c',
                'authmode': 'WPA/WPA2-PSK',
                # 'quality': random.randint(0, 100),
                'channel': 1,
                'hidden': False
            },
            {
                'ssid': 'FRITZ!Box 7490',
                'RSSI': -random.randint(0, 100),
                'bssid': '3810d517eb39',
                'authmode': 'WPA2-PSK',
                # 'quality': random.randint(0, 100),
                'channel': 11,
                'hidden': False
            }
        ]

        return nets

    @staticmethod
    def _dummy_data_raw() -> List[list]:
        dummy_data = NetworkHelper._dummy_data()
        nets_raw = NetworkHelper._convert_dummy_data_to_raw(data=dummy_data)
        """
        [
            [
                'TP-LINK_FBFC3C',
                'a0f3c1fbfc3c',
                1,
                -random.randint(0, 100),
                'WPA/WPA2-PSK',
                False
            ],
            [
                'FRITZ!Box 7490',
                '3810d517eb39',
                11,
                -random.randint(0, 100),
                'WPA2-PSK',
                False
            ]
        ]
        """
        return nets_raw

    @staticmethod
    def _gather_ifconfig_data() -> Tuple[str, str, str, str]:
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

    def isconnected(self) -> bool:
        """
        Get connection status

        :returns:   Flag whether device is connected to network or not
        :rtype:     bool
        """
        return self.connected

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

    def active(self, value=None) -> Union[None, bool]:
        if value is not None:
            print('Change working mode to: {}'.format(value))
            self._active = value
        else:
            return self._active

    def scan(self) -> list:
        networks = list()

        networks = self._internal_scan()

        return networks

    def ifconfig(self, value: Optional[Tuple[str, str, str, str]] = None) -> Union[None, Tuple[str, str, str, str]]:
        if value is not None:
            print('Change of ifconfig not supported')
        else:
            return self._gather_ifconfig_data()


class Client(NetworkHelper):
    """docstring for Client"""
    def __init__(self):
        pass

    def ifconfig(self, value: Optional[Tuple[str, str, str, str]] = None) -> Union[None, Tuple[str, str, str, str]]:
        if value is not None:
            print('Change of ifconfig not supported')
        else:
            return self._gather_ifconfig_data()


class WLAN(Client, Station):
    """docstring for WLAN"""
    def __init__(self, val: int) -> None:
        Station.__init__(self)
        Client.__init__(self)
