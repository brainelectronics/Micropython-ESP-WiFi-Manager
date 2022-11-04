#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
WiFi Manager

Load and connect to configured networks based on an encrypted JSON file.

In case no network has been configured or no connection could be established
to any of the configured networks within the timeout of each 5 seconds an
AccessPoint is created.

A simple Picoweb webserver is hosting the webpages to connect to new networks,
to remove already configured networks from the list of connections to
establish and to get the latest available networks as JSON
"""

# system packages
import binascii as ubinascii
from Crypto.Cipher import AES
import gc
import json
from machine import machine, Timer
from pathlib import Path
import _thread
import time
# import ucryptolib

# pip installed packages
from flask import Flask, render_template, url_for, redirect, request, \
    jsonify, make_response

# custom packages
from generic_helper import GenericHelper
from generic_helper import Message
from path_helper import PathHelper
from wifi_helper import WifiHelper

# typing natively supported on python
from typing import List, Union
from unittest.mock import Mock

gc.collect = Mock()


class WiFiManager(object):
    """docstring for WiFiManager"""
    ERROR = 0
    SUCCESS = 1
    CONNECTION_ISSUE_TIMEOUT = 1
    CONNECTION_ISSUE_NOT_CONFIGURED = 2

    def __init__(self, logger=None, quiet=False, name=__name__):
        # setup and configure logger if none is provided
        if logger is None:
            logger = GenericHelper.create_logger(
                logger_name=self.__class__.__name__)
            GenericHelper.set_level(logger, 'debug')
        self.logger = logger
        self.logger.disabled = quiet
        self._config_file = (Path(__file__).parent / '..' / '..').resolve() / 'wifi-secure.json'    # noqa: E501
        print('Config file at: {}'.format(self._config_file))

        flask_root_folder = (Path(__file__).parent / '..' / '..').resolve()
        template_folder = flask_root_folder / 'templates'
        static_folder = (flask_root_folder / '..' / 'static').resolve()
        self.app = Flask(name,
                         template_folder=template_folder,
                         static_folder=static_folder)
        self.wh = WifiHelper()

        self.event_sinks = set()

        self._available_urls = dict()
        self._add_app_routes()

        # other setup and init here
        # AES key shall be 16 or 32 bytes
        required_len = 16
        uuid = ubinascii.hexlify(machine.unique_id())
        amount = required_len // len(uuid) + (required_len % len(uuid) > 0)
        self._enc_key = (uuid * amount).decode('ascii')[:required_len]

        self._configured_networks = list()
        self._selected_network_bssid = ''
        self._connection_timeout = 5
        self._connection_result = self.ERROR

        # WiFi scan specific defines
        self._scan_lock = _thread.allocate_lock()
        self._scan_interval = 5000  # milliseconds
        # Queue also works, but in this case there is no need for a history
        self._scan_net_msg = Message()
        self._scan_net_msg.set([])  # empty list, required by save_wifi_config
        self._latest_scan = None
        self._stop_scanning_timer = None

        # start the WiFi scanning thread as soon as "start_config" is called
        self.scanning = False

    @property
    def available_urls(self) -> dict:
        """
        Get public available URLs.

        :returns:   Dict of available URLs as keys and description as values
        :rtype:     dict
        """
        return self._available_urls

    @available_urls.setter
    def available_urls(self, value: dict) -> None:
        """
        Set public available URLs.

        This is used to render the index page content

        :param      value:  New URL for index page
        :type       value:  Dict
        """
        if isinstance(value, dict):
            self._available_urls.update(value)

    @property
    def connection_timeout(self) -> int:
        """
        Get the WiFi connection timeout in seconds.

        :returns:   Timeout if WiFi connection can not be established within
        :rtype:     int
        """
        return self._connection_timeout

    @connection_timeout.setter
    def connection_timeout(self, value: int) -> None:
        """
        Set the WiFi connection timeout in seconds.

        Values below 3 sec are set to 3 sec.

        :param      value:  Timeout of WiFi connection per network in seconds
        :type       value:  int
        """
        if isinstance(value, int):
            if value < 3:
                value = 3
            self._connection_timeout = value

    @property
    def connection_result(self) -> int:
        """
        Get connection issue error code

        :returns:   Connection issue error
        :rtype:     int
        """
        return self._connection_result

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
            loaded_cfg = self._load_wifi_config_data(path=self._config_file,
                                                     encrypted=True)

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
            # self.logger.debug('All SSIDs: {}'.format(ssids))
            self.logger.debug('Config content: {}'.format(loaded_cfg))
            self.logger.debug('Private config content: {}'.
                              format(private_cfg))
            self.logger.debug('Configured networks: {}'.
                              format(self._configured_networks))

            self.logger.info('Connecting to loaded network config...')
            result = WifiHelper.connect(ssid=ssids,
                                        password=passwords,
                                        timeout=self.connection_timeout,
                                        reconnect=False)
            self.logger.debug('Result of connection: {}'.format(result))

            if result is False:
                self._connection_result = self.CONNECTION_ISSUE_TIMEOUT
        else:
            self.logger.debug('WiFi config file does not (yet) exist')
            self._connection_result = self.CONNECTION_ISSUE_NOT_CONFIGURED

        return result

    def start_config(self) -> None:
        """Start WiFi manager accesspoint and webserver."""
        ap_name = 'WiFiManager_{}'.format(
            GenericHelper.get_uuid(-4).decode('ascii'))
        self.logger.info('Starting WiFiManager as AccessPoint "{}"'.
                         format(ap_name))
        result = self.wh.create_ap(ssid=ap_name,
                                   password='',
                                   channel=11,
                                   timeout=5)
        self.logger.debug('Created AP: {}'.format(result))
        ifconfig = self.wh.ifconfig_ap
        self.logger.debug(ifconfig)

        # start scanning for available networks
        self.scanning = True

        # finally
        self.run(port=80, debug=True)
        # self.run(host=ifconfig.ip, port=80, debug=True)

        self.logger.debug('Finished running the PicoWeb application')
        self.scanning = False
        self.logger.debug('Stopped scanning thread')

        # wait some time to end all threads savely
        time.sleep(5)

        gc.collect()
        self.logger.debug('Goodbye from WiFiManager')

    def _add_app_routes(self) -> None:
        """Add all application routes to the webserver."""

        # self.app.add_url_rule('/', func=self.index)
        # @app.route('/index')
        # def index(self, req, resp): pass
        # https://github.com/pfalcon/picoweb/blob/b74428ebdde97ed1795338c13a3bdf05d71366a0/picoweb/__init__.py#L251
        self.app.add_url_rule('/', view_func=self.landing_page)
        self.app.add_url_rule('/select', view_func=self.wifi_selection)
        self.app.add_url_rule('/render_network_inputs',
                              view_func=self.render_network_inputs)
        self.app.add_url_rule('/configure', view_func=self.wifi_configs)
        self.app.add_url_rule('/save_wifi_config',
                              view_func=self.save_wifi_config,
                              methods=['POST', 'GET'])
        self.app.add_url_rule('/remove_wifi_config',
                              view_func=self.remove_wifi_config,
                              methods=['POST', 'GET'])
        self.app.add_url_rule('/scan_result', view_func=self.scan_result)

        self.app.add_url_rule(
            "/static/css/bootstrap.min.css",
            view_func=self.styles
        )
        self.app.add_url_rule(
            "/static/js/toast.js",
            view_func=self.scripts
        )
        # regex not supported in Flask
        # self.app.add_url_rule(re.compile(r'^\/(.+\.css)$'),
        #                       view_func=self.styles)
        # self.app.add_url_rule(url=re.compile(r'^\/(.+\.js)$'),
        #                       view_func=self.scripts)

        available_urls = {
            "/select": {
                "title": "Select WiFi",
                "color": "border-primary",
                "text": "Configure WiFi networks",
            },
            "/configure": {
                "title": "Manage WiFi networks",
                "color": "border-primary",
                "text": "Remove credentials of configured WiFi networks",
            },
            "/scan_result": {
                "title": "Scan data",
                "color": "text-white bg-info",
                "text": "Latest WiFi scan data as JSON",
            }
        }

        self.available_urls = available_urls

    def _encrypt_data(self, data: Union[str, list, dict]) -> bytes:
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
        encrypted_data = enc.encrypt(data_bytes + b'\x00' * ((16 - (len(data_bytes) % 16)) % 16))   # noqa: E501

        return encrypted_data

    def _decrypt_data(self, data: bytes) -> str:
        """
        Decrypt data with decryption key

        :param      data:  The data
        :type       data:  bytes

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
                                data: Union[dict, List[dict]],
                                path: str,
                                encrypted: bool = False) -> None:
        """
        Extend WiFi configuration data of file.

        :param      data:       The data
        :type       data:       Union[dict, List[dict]]
        :param      path:       The full path to the file
        :type       path:       str
        :param      encrypted:  Flag to save data encrypted
        :type       encrypted:  bool, optional
        """
        # in case the file already exists, extend its data content
        if PathHelper.exists(path=path):
            existing_data = self._load_wifi_config_data(path=path,
                                                        encrypted=encrypted)
            self.logger.debug('Existing WiFi config data: {}'.
                              format(existing_data))
            if isinstance(existing_data, dict):
                if isinstance(data, dict):
                    data = [existing_data, data]
                elif isinstance(data, list):
                    data = [existing_data] + data
            elif isinstance(existing_data, list):
                if isinstance(data, dict):
                    existing_data.append(data)
                    data = existing_data
                elif isinstance(data, list):
                    data = existing_data + data
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
            encrypted_data = self._encrypt_data(data=data)

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

    def _load_wifi_config_data(self,
                               path: str,
                               encrypted: bool = False) -> Union[dict,
                                                                 List[dict]]:
        """
        Load WiFi configuration data from file.

        :param      path:       The full path to the file
        :type       path:       str
        :param      encrypted:  Flag to decrypt data
        :type       encrypted:  bool, optional

        :returns:   The loaded data
        :rtype:     Union[dict, List[dict]]
        """
        data = dict()

        if encrypted:
            # read file in binary as it contains encrypted data
            encrypted_read_data = GenericHelper.load_file(path=path,
                                                          mode='rb')
            self.logger.debug('Read encrypted data: {}'.
                              format(encrypted_read_data))

            # decrypt read data
            decrypted_data_str = self._decrypt_data(data=encrypted_read_data)
            self.logger.debug('Decrypted data str: {}'.
                              format(decrypted_data_str))

            # convert string to dict
            data = GenericHelper.str_to_dict(data=decrypted_data_str)
            self.logger.debug('Decrypted data dict: {}'.format(data))
        else:
            data = GenericHelper.load_json(path=path, mode='r')
            self.logger.debug('Read non encrypted data: {}'.
                              format(data))

        return data

    @property
    def configured_networks(self) -> List[str]:
        """
        Get SSIDs of all configured networks

        :returns:   SSIDs of configured networks
        :rtype:     List[str]
        """
        return self._configured_networks

    def _scan(self,
              wh: WifiHelper,
              msg: Message,
              scan_interval: int,
              lock: int) -> None:
        """
        Scan for available networks.

        :param      wh:             Wifi helper object
        :type       wh:             WifiHelper
        :param      msg:            The shared message from this thread
        :type       msg:            Message
        :param      scan_interval:  The scan interval in milliseconds
        :type       scan_interval:  int
        :param      lock:           The lock object
        :type       lock:           _thread.lock
        """
        while lock.locked():
            try:
                # rescan for available networks
                found_nets = wh.get_wifi_networks_sorted(rescan=True,
                                                         scan_if_empty=True)

                msg.set(found_nets)

                # wait for specified time
                time.sleep(scan_interval / 1000.0)
            except KeyboardInterrupt:
                break

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

        Values below 1000 ms are set to 1000 ms.
        One scan takes around 3 sec, which leads to maximum 15 scans per min

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
            if isinstance(self._stop_scanning_timer, Timer):
                self._stop_scanning_timer.deinit()

    def _stop_scanning_cb(self, tim: Timer) -> None:
        """
        Timer callback function to stop the WiFi scan thread.

        :param      tim:  The timer calling this function.
        :type       tim:  machine.Timer
        """
        self.scanning = False

    @property
    def latest_scan(self) -> Union[List[dict], str]:
        """
        Get lastest scanned networks.

        Start scanning if not already scanning, set a oneshot timer to 10.5x
        of @see scan_interval to stop scanning again in order to reduce CPU
        load and avoid unused scans

        :returns:   Dictionary of available networks
        :rtype:     Union[List[dict], str]
        """
        if not self.scanning:
            self.scanning = True

            if self._stop_scanning_timer is None:
                self._stop_scanning_timer = Timer(-1)
            cb_period = int(self.scan_interval * 10 + self.scan_interval / 2)
            self._stop_scanning_timer.init(mode=machine.Timer.ONE_SHOT,
                                           period=cb_period,
                                           callback=self._stop_scanning_cb)

        return self._scan_net_msg.value()

    def _render_index_page(self, available_pages: dict) -> str:
        """
        Render HTML list of available pages

        :param      available_pages:    All available pages
        :type       available_pages:    dict

        :returns:   Sub content of landing page
        :rtype:     str
        """
        content = ""

        # sort dict by 'title' of the dict values
        for url, info in sorted(available_pages.items(),
                                key=lambda item: item[1]['title']):
            content += """
            <div class="col-sm-4 py-2"><div class="card h-100 {color}"><div class="card-body">
                <h3 class="card-title">{title}</h3><p class="card-text">{text}</p>
                <a href="{url}" class="stretched-link"></a></div></div></div>
            """.format(color=info['color'],     # noqa: E501
                       title=info['title'],
                       text=info['text'],
                       url=url)

        return content

    def _render_network_inputs(self,
                               available_nets: dict,
                               selected_bssid: str = '') -> str:
        """
        Render HTML list of selectable networks

        :param      available_nets:  All available nets
        :type       available_nets:  dict
        :param      selected_bssid:  Currently selected network on the webpage
        :type       selected_bssid:  str

        :returns:   Sub content of WiFi selection page
        :rtype:     str
        """
        content = ""
        if len(available_nets):
            for ele in available_nets:
                selected = ''
                if ele['bssid'] == selected_bssid:
                    selected = "checked"
                content += """
                <input class="list-group-item-check" type="radio" name="bssid" id="{bssid}" value="{bssid}" onclick="remember_selected_element(this)" {state}>
                <label class="list-group-item py-3" for="{bssid}">
                  {ssid}
                  <span class="d-block small opacity-50">
                    Signal quality {quality}&#37;, BSSID {bssid}
                  </span>
                </label>
                """.format(bssid=ele['bssid'],  # noqa: E501
                           state=selected,
                           ssid=ele['ssid'],
                           quality=ele['quality'])
        else:
            # as long as no networks are available show a spinner
            content = """
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            """

        return content

    def _save_wifi_config(self, form_data: dict) -> None:
        """
        Save a new WiFi configuration to the WiFi configuration file.

        :param      form_data:  The form data
        :type       form_data:  dict
        """
        network_cfg = dict()
        available_nets = self.latest_scan
        self.logger.info('Available nets: {}'.format(available_nets))
        # [
        #   {
        #       'ssid': 'TP-LINK_FBFC3C',
        #       'RSSI': -21,
        #       'bssid': 'a0f3c1fbfc3c',
        #       'authmode': 'WPA/WPA2-PSK',
        #       'quality': 9,
        #       'channel': 1,
        #       'hidden': False
        #   },
        #   {
        #       'ssid': 'FRITZ!Box 7490',
        #       'RSSI': -17,
        #       'bssid': '3810d517eb39',
        #       'authmode': 'WPA2-PSK',
        #       'quality': 27,
        #       'channel': 11,
        #       'hidden': False
        #   }
        # ]

        # find SSID of network based on given bssid value
        if form_data['ssid'] != '':
            network_cfg['ssid'] = form_data['ssid']
        else:
            if 'bssid' not in form_data:
                return

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
                    this_bssid = ele['bssid']   # .decode('ascii')

                if this_bssid == selected_bssid:
                    # use string, json loading will fail otherwise later
                    network_cfg['ssid'] = ele['ssid']   # .decode('ascii')
                    break

        network_cfg['password'] = form_data['password']
        self.logger.info('Network cfg: {}'.format(network_cfg))
        # Network cfg: {'ssid': 'TP-LINK_FBFC3C', 'password': 'qwertz'}

        if 'ssid' in network_cfg:
            if isinstance(network_cfg['ssid'], bytes):
                network_cfg['ssid'] = network_cfg['ssid'].decode('ascii')

            self.logger.info('Raw network config: {}'.format(network_cfg))

            # save data in encrypted mode
            self.extend_wifi_config_data(data=network_cfg,
                                         path=self._config_file,
                                         encrypted=True)
            self.logger.info('Saving of network config to {} done'.
                             format(self._config_file))
        else:
            self.logger.info('No valid SSID found, will not save this net')

    def _remove_wifi_config(self, form_data: dict) -> None:
        """
        Remove a WiFi network from the WiFi configuration file.

        :param      form_data:  The form data
        :type       form_data:  dict
        """
        if len(form_data):
            loaded_cfg = self._load_wifi_config_data(path=self._config_file,
                                                     encrypted=True)

            updated_cfg = list()
            updated_ssids = list()

            for net in loaded_cfg:
                if net['ssid'] not in form_data:
                    updated_cfg.append(net)
                    updated_ssids.append(net['ssid'])

            self._configured_networks = updated_ssids.copy()

            # create bytes array of the dict and encrypt it
            encrypted_data = self._encrypt_data(data=updated_cfg)

            # save to file as binary
            GenericHelper.save_file(data=encrypted_data,
                                    path=self._config_file,
                                    mode='wb')
            self.logger.debug('Saved encrypted data as json: {}'.
                              format(encrypted_data))

    # -------------------------------------------------------------------------
    # Webserver functions

    # @app.route('/landing_page')
    def landing_page(self):
        """
        Provide landing page aka index page

        List of available subpages is rendered from all elements of the
        @see available_urls property
        """
        available_pages = self.available_urls
        content = self._render_index_page(available_pages)

        return render_template('index.tpl.html', content=content)

    # @app.route("/scan_result")
    def scan_result(self):
        """Provide latest found networks as JSON"""
        return jsonify(self.latest_scan)

    # @app.route("/select")
    def wifi_selection(self):
        """
        Provide webpage to select WiFi network from list of available networks

        Scanning just in time of accessing the page would block all processes
        for approx. 2.5 sec.
        Using the result provided by the scan thread via a message takes only
        0.02 sec to complete
        """
        available_nets = self.latest_scan
        content = self._render_network_inputs(available_nets=available_nets)

        # do not stop scanning as page is updating scan results on the fly
        # with XMLHTTP requests to @see scan_result
        # stop scanning thread
        # self.logger.info('Stopping scanning thread')
        # self.scanning = False

        return render_template('select.tpl.html', content=content)

    # @app.route("/render_network_inputs")
    def render_network_inputs(self) -> str:
        """Return rendered network inputs content to webpage"""
        available_nets = self.latest_scan
        selected_bssid = self._selected_network_bssid
        content = self._render_network_inputs(available_nets=available_nets,
                                              selected_bssid=selected_bssid)
        return content

    # @app.route("/configure")
    def wifi_configs(self):
        """Provide webpage with table of configured networks"""
        configured_nets = self.configured_networks
        self.logger.debug('Existing config content: {}'.
                          format(configured_nets))

        if isinstance(configured_nets, str):
            configured_nets = [configured_nets]

        # disable submit button by default
        return render_template('remove.tpl.html',
                               wifi_nets=configured_nets,
                               # index_js=self.scripts,
                               button_mode='disabled')

    # @app.route("/save_wifi_config", methods=['POST', 'GET'])
    def save_wifi_config(self):
        form_data = dict(request.form)

        self.logger.info('WiFi user input content: {}'.format(form_data))
        # result if a network of the list has been selected
        # {'bssid': 'a0f3c1fbfc3c', 'ssid': '', 'password': 'sdsfv'}
        # result if a custom network is given
        # {'ssid': 'myCustom Net', 'password': 'asdf1234'}
        # result if nothing is selected
        # {'ssid': '', 'password': ''}

        self._save_wifi_config(form_data=form_data)

        return redirect(url_for('landing_page'))

    # @app.route("/remove_wifi_config, methods=['POST', 'GET'])
    def remove_wifi_config(self):
        """Remove a configured WiFi network"""
        form_data = dict(request.form)

        self.logger.info('Remove networks: {}'.format(form_data))
        # Remove networks: {'FRITZ!Box 7490': 'FRITZ!Box 7490'}

        self._remove_wifi_config(form_data=form_data)

        # redirect to '/configure'
        headers = {'Location': '/configure'}    # noqa: F841
        return redirect(url_for('wifi_configs'))

    # @app.route(re.compile('^\/(.+\.css)$'))
    def styles(self):
        """
        Send gzipped CSS content if supported by client.

        Shows specifying headers as a flat binary string, more efficient if
        such headers are static.
        """
        file_path = str(request.url_rule)
        headers = b'Cache-Control: max-age=86400\r\n'

        if 'gzip' in str(request.headers):
            self.logger.debug('gzip accepted for CSS style file')
            file_path += '.gz'
            headers += b'Content-Encoding: gzip\r\n'

        complete_file_path = file_path
        self.logger.debug('Accessed file {}'.format(complete_file_path))
        return self.sendfile(writer=request,
                             fname=complete_file_path,
                             content_type='text/css',
                             headers=headers)

    # @app.route(re.compile('^\/(.+\.js)$'))
    def scripts(self) -> None:
        """
        Send gzipped JS content if supported by client.

        Shows specifying headers as a flat binary string, more efficient if
        such headers are static.
        """
        file_path = str(request.url_rule)
        headers = b'Cache-Control: max-age=86400\r\n'

        if 'gzip' in str(request.headers):
            self.logger.debug('gzip accepted for JS script file')
            file_path += '.gz'
            headers += b'Content-Encoding: gzip\r\n'

        complete_file_path = file_path
        self.logger.debug('Accessed file {}'.format(complete_file_path))
        return self.sendfile(writer=request,
                             fname=complete_file_path,
                             content_type='text/javascript',
                             headers=headers)

    def sendfile(self,
                 fname: str,
                 content_type: str,
                 headers: str,
                 writer=None):
        """
        Fake function to send file in same style as in PicoWeb on Micropython

        :param      fname:         The filename
        :type       fname:         str
        :param      content_type:  The content type
        :type       content_type:  str
        :param      headers:       The headers
        :type       headers:       str
        :param      writer:        The writer
        :type       writer:        Optional
        """
        here = Path(__file__)
        flask_root_folder = (here.parent / '..' / '..' / '..').resolve()
        file_path = str(flask_root_folder) + str(fname)

        self.logger.debug('Open file {}'.format(file_path))
        with open(file_path, 'rb') as file:
            content = file.read()

        res = make_response(content)
        res.headers["Content-Type"] = content_type
        # res.headers['Content-Length'] = len(content)

        for ele in headers.decode('ascii').splitlines():
            key, value = ele.split(':')
            res.headers[key] = value.lstrip()

        return res

    def run(self,
            host: str = '0.0.0.0',
            port: int = 80,
            debug: bool = False,
            log=None) -> None:
        """
        Run the web application

        :param      host:   The hostname to listen on
        :type       host:   str, optional
        :param      port:   The port of the webserver
        :type       port:   int, optional
        :param      debug:  Flag to automatically reload for code changes and
                            show debugger content
        :type       debug:  bool, optional
        :param      log:    Logger of Picoweb
        :type       log:    logging.Logger
        """
        self.logger.debug('Run app on {}:{} with debug: {}'.format(host,
                                                                   port,
                                                                   debug))
        try:
            # self.app.run()
            self.app.run(debug=debug)
            # self.app.run(host=host, port=port, debug=debug, log=log)
        except KeyboardInterrupt:
            self.logger.debug('Catched KeyboardInterrupt at run of web app')
        except Exception as e:
            self.logger.warning(e)


if __name__ == "__main__":
    wm = WiFiManager(logger=None, quiet=False)
    result = wm.load_and_connect()
    print('Result of load_and_connect: {}'.format(result))
    wm.start_config()
