#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
main script, do your stuff here, similar to the loop() function on Arduino
"""

# system packages
from Crypto.Cipher import AES
from flask import Flask, render_template, abort, request, jsonify
import gc
import json
import random
import _thread
import time
from typing import List, Union

# custom packages
from generic_helper import GenericHelper
from generic_helper import Message
from led_helper import Neopixel
from path_helper import PathHelper
from wifi_helper import WifiHelper


class WiFiManager(object):
    """docstring for WiFiManager"""
    def __init__(self, logger=None, quiet=False, name=__name__):
        # setup and configure logger if none is provided
        # self.mh = GenericHelper()
        if logger is None:
            logger = GenericHelper.create_logger(logger_name=name)
        self.logger = logger

        self._config_file = '../../wifi-secure.json'

        flask_root_folder = (Path(__file__).parent / '..' / '..').resolve()
        template_folder = flask_root_folder / 'templates'
        static_folder = flask_root_folder / 'static'
        self.app = Flask(name,
                         template_folder=template_folder,
                         static_folder=static_folder)
        self.wh = WifiHelper()
        self.pixel = Neopixel()
        self.pixel.color = 'yellow'
        self.pixel.intensity = 20

        self.add_app_routes()

        # encryption key not defined as encryption is not supported here
        required_len = 16
        uuid = b'DEADBEEF'
        amount = required_len // len(uuid) + (required_len % len(uuid) > 0)
        self._enc_key = (uuid * amount).decode('ascii')[:required_len]

        self._configured_networks = list()

        # WiFi scan specific defines
        self._scan_lock = _thread.allocate_lock()
        self._scan_interval = 5000  # milliseconds
        # Queue also works, but not in this case there is no need for a history
        self._scan_net_msg = Message()
        self._scan_net_msg.set([])  # empty list, required by save_wifi_config
        self._latest_scan = None
        # other class defines are not required

        # finally start the WiFi scanning thread
        self.scanning = True

    def load_and_connect(self) -> bool:
        """
        Load configured network credentials and try to connect to those

        :returns:   Result of connection
        :rtype:     bool
        """
        result = False

        # check wifi config file existance
        if PathHelper.exists(path=self._config_file):
            self.logger.debug('Encrypted wifi config file exists')
            loaded_cfg = self.load_wifi_config_data(path=self._config_file,
                                                    encrypted=True)
            # self.logger.warning('loaded_cfg: {}'.format(loaded_cfg))
            # self.logger.warning('loaded_cfg type: {}'.format(type(loaded_cfg)))

            private_cfg = None
            ssids = list()
            passwords = list()

            if isinstance(loaded_cfg, list):
                # deepcopy would be necessary but not builtin in micropython
                private_cfg = json.loads(json.dumps(loaded_cfg))
                for net in private_cfg:
                    if 'ssid' in net:
                        ssids.append(net['ssid'])
                    if 'password' in net:
                        passwords.append(net['password'])
                        net['password'] = '*' * 8
                    else:
                        passwords.append('')
                self._configured_networks = list(ssids).copy()
            elif isinstance(loaded_cfg, dict):
                private_cfg = loaded_cfg.copy()
                if 'ssid' in loaded_cfg:
                    ssids = loaded_cfg['ssid']
                if 'password' in private_cfg:
                    passwords = loaded_cfg['password']
                    private_cfg['password'] = '*' * 8
                self._configured_networks = ssids

            # self._configured_networks = list(ssids).copy()
            self.logger.debug('All SSIDs: {}'.format(ssids))
            self.logger.debug('Config content: {}'.format(loaded_cfg))
            self.logger.debug('Private config content: {}'.format(private_cfg))
            self.logger.debug('Configured networks: {}'.
                              format(self._configured_networks))

            self.logger.info('Connecting to loaded network config...')
            result = WifiHelper.connect(ssid=ssids,
                                        password=passwords,
                                        timeout=5,
                                        reconnect=False)
            result = True
            self.logger.debug('Result of connection: {}'.format(result))
        else:
            self.logger.debug('WiFi config file does not (yet) exist')

        return result

    def start_config(self) -> None:
        """Start WiFi manager accesspoint and webserver."""
        self.logger.info('Starting Manager with AccessPoint')
        result = self.wh.create_ap(ssid='WiFiManager',
                                   password='',
                                   channel=11,
                                   timeout=5)
        result = True
        self.logger.debug('Created AP: {}'.format(result))
        # ifconfig = self.wh.ifconfig_ap
        # self.logger.debug(ifconfig)

        # finally
        self.run(port=80, debug=True)

    def add_app_routes(self) -> None:
        """Add all application routes to the webserver."""
        self.app.add_url_rule("/", view_func=self.landing_page)
        self.app.add_url_rule("/wifi_selection", view_func=self.wifi_selection)
        self.app.add_url_rule("/wifi_configs", view_func=self.wifi_configs)
        self.app.add_url_rule("/save_wifi_config",
                              view_func=self.save_wifi_config,
                              methods=['POST', 'GET'])
        self.app.add_url_rule("/remove_wifi_config",
                              view_func=self.remove_wifi_config,
                              methods=['POST', 'GET'])
        self.app.add_url_rule("/scan_result", view_func=self.scan_result)

    def encrypt_data(self, data: Union[str, list, dict]) -> bytes:
        """
        Encrypt data with encryption key

        :param      data:  The data
        :type       data:  Union[str, list, dict]

        :returns:   Encrypted data
        :rtype:     bytes
        """
        # create bytes array of the data and encrypt it
        if not isinstance(data, str):
            data = str(data)

        data_bytes = data.encode()
        enc = AES.new(self._enc_key, AES.MODE_ECB)

        # add '\x00' to fill up the data string to reach a multiple of 16
        encrypted_data = enc.encrypt(data_bytes + b'\x00' * ((16 - (len(data_bytes) % 16)) % 16))

        return encrypted_data

    def decrypt_data(self, data: str) -> str:
        """
        Decrypt data with decryption key

        :param      data:  The data
        :type       data:  str

        :returns:   Decrypted data
        :rtype:     str
        """
        # decrypt bytes array
        dec = AES.new(self._enc_key, AES.MODE_ECB)
        decrypted_data = dec.decrypt(data)

        # remove added '\x00' stuff after decoding it to ascii
        decrypted_data_str = decrypted_data.decode('ascii').rstrip('\x00')

        return decrypted_data_str

    def extend_wifi_config_data(self,
                                data: Union[dict, list],
                                path: str,
                                encrypted: bool = False) -> None:
        """
        Extend WiFi configuration data of file.

        :param      data:       The data
        :type       data:       Union[dict, list]
        :param      path:       The full path to the file
        :type       path:       str
        :param      encrypted:  Flag to save data encrypted
        :type       encrypted:  bool, optional
        """
        # in case the file already exists, extend its data content
        if PathHelper.exists(path=path):
            existing_data = self.load_wifi_config_data(path=path,
                                                       encrypted=encrypted)
            self.logger.debug('Existing WiFi config data: {}'.
                              format(existing_data))
            if isinstance(existing_data, dict):
                data = [existing_data, data]
            elif isinstance(existing_data, list):
                existing_data.append(data)
                data = existing_data
            else:
                # unknown content, overwrite it
                pass

        self.logger.debug('Updated data: {}'.format(data))

        ssids = list()
        if isinstance(data, list):
            for net in data:
                if 'ssid' in net:
                    ssids.append(net['ssid'])
        elif isinstance(data, dict):
            if 'ssid' in data:
                ssids = [data['ssid']]

        self._configured_networks = ssids.copy()

        if encrypted:
            # create bytes array of the dict and encrypt it
            encrypted_data = self.encrypt_data(data=data)

            # save data to file as binary as it contains encrypted data
            GenericHelper.save_file(data=encrypted_data,
                                    path=path,
                                    mode='wb')
            self.logger.debug('Saved encrypted data as json: {}'.
                              format(encrypted_data))
        else:
            # save data to file, no need for binary mode
            GenericHelper.save_json(data=data,
                                    path=path,
                                    mode='w')
            self.logger.debug('Saved data as json: {}'.format(data))

    def load_wifi_config_data(self,
                              path: str,
                              encrypted: bool = False) -> Union[dict, List[dict]]:
        """
        Load WiFi configuration data from file.

        :param      path:       The full path to the file
        :type       path:       str
        :param      encrypted:  Flag to decrypt data
        :type       encrypted:  bool, optional

        :returns:   The loaded data
        :rtype:     dict
        """
        data = dict()

        if encrypted:
            # read file in binary as it contains encrypted data
            encrypted_read_data = GenericHelper.load_file(path=path, mode='rb')
            self.logger.debug('Read encrypted data: {}'.
                              format(encrypted_read_data))

            # decrypt read data
            decrypted_data_str = self.decrypt_data(data=encrypted_read_data)
            self.logger.debug('Decrypted data str: {}'.
                              format(decrypted_data_str))
            self.logger.warning('type: {}'.format(type(decrypted_data_str)))

            # convert string to dict
            data = GenericHelper.str_to_dict(data=decrypted_data_str)
            self.logger.debug('Decrypted data dict: {}'.format(data))
        else:
            data = GenericHelper.load_json(path=path, mode='r')
            self.logger.debug('Read non encrypted data: {}'.
                              format(data))

        """
        # convert string to dict
        data = GenericHelper.str_to_dict(data=data)

        self.logger.debug('data content: {}'.format(data))
        self.logger.debug('type: {}'.format(type(data)))
        """

        return data

    @property
    def configured_networks(self) -> List[str]:
        # available_nets = self.latest_scan
        # _configured_networks = [ele['ssid'] for ele in available_nets]
        # return _configured_networks
        return self._configured_networks

    # def _scan(self, **kwargs):
    def _scan(self,
              pixel: Neopixel,
              wh: WifiHelper,
              msg: Message,
              scan_interval: int,
              lock: int) -> None:
              # lock: lock) -> None:
        pixel.fading = True

        while lock.locked():
            try:
                # rescan for available networks
                found_nets = wh.get_wifi_networks_sorted(rescan=True,
                                                         scan_if_empty=True)

                # wait for specified time
                # time.sleep_ms(scan_interval)
                time.sleep(scan_interval / 1000.0)

                msg.set(found_nets)
            except KeyboardInterrupt:
                break

        pixel.fading = False
        print('Finished scanning')

    @property
    def scan_interval(self) -> int:
        """
        Get the WiFi scan interval in milliseconds.

        :returns:   Interval of WiFi scans in milliseconds
        :rtype:     int
        """
        return self._scan_interval

    @scan_interval.setter
    def scan_interval(self, value: int) -> None:
        """
        Set the WiFi scan interval in milliseconds.

        Values below 1000ms are set to 1000ms.
        One scan takes around 3 sec, which leads to maximum 15 scans per minute

        :param      value:  Interval of WiFi scans in milliseconds
        :type       value:  int
        """
        if isinstance(value, int):
            if value < 1000:
                value = 1000
            self._scan_interval = value

    @property
    def scanning(self) -> bool:
        """
        Get the scanning status.

        :returns:   Flag whether WiFi network scan is running or not.
        :rtype:     bool
        """
        return self._scan_lock.locked()

    @scanning.setter
    def scanning(self, value: int) -> None:
        """
        Start or stop scanning for available WiFi networks.

        :param      value:  The value
        :type       value:  int
        """
        if value and (not self._scan_lock.locked()):
            # start scanning if not already scanning
            self._scan_lock.acquire()

            # parameters of the _scan function
            params = (
                self.pixel,
                self.wh,
                self._scan_net_msg,
                self._scan_interval,
                self._scan_lock
            )
            _thread.start_new_thread(self._scan, params)
            self.logger.info('Scanning started')
        elif (value is False) and self._scan_lock.locked():
            # stop scanning if not already stopped
            self._scan_lock.release()
            self.logger.info('Scanning stoppped')

    @property
    def latest_scan(self) -> Union[List[dict], str]:
        gc.collect()
        # free = gc.mem_free()
        # self.logger.debug('Free memory: {}'.format(free))
        latest_scan_result = self._scan_net_msg.value()
        self.logger.info('Requested latest scan result: {}'.format(latest_scan_result))
        return latest_scan_result

    # -------------------------------------------------------------------------
    # Webserver functions

    # @app.route('/landing_page')
    def landing_page(self):
        # return render_template('wifi_select_loader.tpl.html',
        return render_template('index.tpl.html')

    # @app.route('/scan_result')
    def scan_result(self):
        return jsonify(self.latest_scan)

    # @app.route('/wifi_selection')
    def wifi_selection(self):
        # abort(404)
        available_nets = self.latest_scan
        # return render_template('wifi_select_loader.tpl.html',
        return render_template('wifi_select_loader_bootstrap.tpl.html',
                               wifi_nets=available_nets)

    # @app.route('/wifi_configs')
    def wifi_configs(self):
        # abort(404)
        configured_nets = self.configured_networks
        self.logger.debug('Existing config content: {}'.
                          format(configured_nets))

        if isinstance(configured_nets, str):
            configured_nets = [configured_nets]

        return render_template('wifi_configs.tpl.html',
                               wifi_nets=configured_nets)

    # @app.route('/save_wifi_config', methods=['POST', 'GET'])
    def save_wifi_config(self):
        # abort(404)
        if request.method == 'POST':
            data = request.form

        form_data = dict(request.form)

        # print('Posted data in save_wifi_config: {}'.format(data))
        self.logger.info('WiFi user input content: {}'.format(form_data))
        # {'bssid': 'a0f3c1fbfc3c', 'ssid': '', 'password': 'sdsfv'}

        network_cfg = self._save_wifi_config(form_data=form_data)

        # resp = jsonify(success=True)
        # return resp
        return render_template('result.html', result=network_cfg)

    def _save_wifi_config(self, form_data: dict) -> dict:
        network_cfg = dict()
        available_nets = self.latest_scan
        self.logger.info('Available nets: {}'.format(available_nets))
        # [{'ssid': 'TP-LINK_FBFC3C', 'RSSI': -21, 'bssid': 'a0f3c1fbfc3c', 'authmode': 'WPA/WPA2-PSK', 'quality': 9, 'channel': 1, 'hidden': False}, {'ssid': 'FRITZ!Box 7490', 'RSSI': -17, 'bssid': '3810d517eb39', 'authmode': 'WPA2-PSK', 'quality': 27, 'channel': 11, 'hidden': False}]

        # find SSID of network based on given bssid value
        if form_data['ssid'] != '':
            network_cfg['ssid'] = form_data['ssid']
        else:
            # selected_bssid = form_data['wifi_network']
            selected_bssid = form_data['bssid']
            for ele in available_nets:
                if (isinstance(selected_bssid, str) and
                   selected_bssid.startswith("b'")):
                    # actually a bytes element used as string
                    # this is a bug due to the XMLHttpRequest updated list as
                    # JSON which does not handle bytes format
                    this_bssid = str(ele['bssid'])
                else:
                    this_bssid = ele['bssid']   #.decode('ascii')

                if this_bssid == selected_bssid:
                    # use string, json loading will fail otherwise later
                    network_cfg['ssid'] = ele['ssid']   #.decode('ascii')
                    break

        network_cfg['password'] = form_data['password']
        self.logger.info('Network cfg: {}'.format(network_cfg))
        # Network cfg: {'ssid': 'TP-LINK_FBFC3C', 'password': 'qwertz'}

        if 'ssid' in network_cfg:
            if isinstance(network_cfg['ssid'], bytes):
                network_cfg['ssid'] = network_cfg['ssid'].decode('ascii')

            self.logger.info('Raw network config: {}'.format(network_cfg))

            # save data in encrypted mode
            #
            #
            # ENABLE THIS AGAIN
            #
            #
            """
            self.extend_wifi_config_data(data=network_cfg,
                                         path=self._config_file,
                                         encrypted=True)
            """
            #
            #
            # ENABLE THIS AGAIN
            #
            #
            self.logger.info('Saving of network config to {} done'.
                             format(self._config_file))
        else:
            self.logger.info('No valid SSID found, will not save this net')

        return network_cfg

    # @app.route('/remove_wifi_config', methods=['POST', 'GET'])
    def remove_wifi_config(self):
        # abort(404)
        if request.method == 'POST':
            data = request.args

        # Whether form data comes from GET or POST request, once parsed,
        # it's available as req.form dictionary
        form_data = request.get_json(force=True)
        self.logger.info('Received data: {}'.format(form_data))
        # print('Posted data in remove_wifi_config: {}'.format(data))

        if all(ele in form_data for ele in ['name', 'index']):
            network_name = form_data['name']
            network_index = int(form_data['index']) - 1  # th is also counted

            self.logger.debug('Remove network "{}" at index {}'.
                              format(form_data['name'], form_data['index']))

            if network_name == "all" and network_index == -1:
                if PathHelper.exists(path=self._config_file):
                    os.remove(self._config_file)
                    self.logger.debug('Removed network file')
                return

            loaded_cfg = self.load_wifi_config_data(path=self._config_file,
                                                    encrypted=True)
            self.logger.debug('Existing config content: {}'.format(loaded_cfg))

            try:
                network_cfg = loaded_cfg[network_index]
                if network_cfg['ssid'] == network_name:
                    self.logger.debug('Found specified network in network cfg')

                    ssids = list()
                    if isinstance(loaded_cfg, list):
                        # remove element from list
                        del loaded_cfg[network_index]

                        self.logger.debug('Updated data: {}'.
                                          format(loaded_cfg))

                        # list of dicts
                        for net in loaded_cfg:
                            if 'ssid' in net:
                                ssids.append(net['ssid'])
                    elif isinstance(loaded_cfg, dict):
                        pass
                        # do not do anything, updated data will be empty list

                        # if 'ssid' in loaded_cfg:
                        #     ssids = loaded_cfg['ssid']

                    self._configured_networks = ssids.copy()

                    # create bytes array of the dict and encrypt it
                    encrypted_data = self.encrypt_data(data=loaded_cfg)

                    # save to file as binary
                    GenericHelper.save_file(data=encrypted_data,
                                            path=self._config_file,
                                            mode='w')     # 'wb' for encrypted data
                    # self.mh.save_file(data=encrypted_data,
                    #                   path=self._config_file,
                    #                   mode='w')     # 'wb' for encrypted data
                    self.logger.debug('Saved encrypted data as json: {}'.
                                      format(encrypted_data))
            except IndexError as e:
                self.logger.debug('Specified network at index {} not found'.
                                  format(network_index))
            except Exception as e:
                self.logger.debug('Catched: {}'.format(e))

        # resp = jsonify(success=True)
        # return resp
        return render_template('result.html', result=data)

    """
    @app.route('/result')
    def show_result():
        return render_template('result.html', result=result)
    """

    def run(self,
            host: str = '0.0.0.0',
            port: int = 80,
            debug: bool = False) -> None:
        """
        Run the web application

        :param      host:   The hostname to listen on
        :type       host:   str, optional
        :param      port:   The port of the webserver
        :type       port:   int, optional
        :param      debug:  Flag to automatically reload for code changes and
                            show debugger content
        :type       debug:  bool, optional
        """
        self.logger.debug('Run app on {}:{} with debug: {}'.format(host,
                                                                   port,
                                                                   debug))
        try:
            # self.app.run()
            self.app.run(debug=debug)
            # self.app.run(host=host, port=port, debug=debug)
        except KeyboardInterrupt:
            self.logger.debug('Catched KeyboardInterrupt at run of web app')
        except Exception as e:
            self.logger.warning(e)


if __name__ == "__main__":
    # app.run()
    # app.run(debug=True)
    # app.run(host=host, port=port, debug=debug)
    wm = WiFiManager(logger=None, quiet=False)
    result = wm.load_and_connect()
    print('Result of load_and_connect: {}'.format(result))
    wm.start_config()
