#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Run WiFi Manager simulation"""

from wifi_manager import WiFiManager


def main():
    wm = WiFiManager(logger=None, quiet=False)
    result = wm.load_and_connect()
    print('Result of load_and_connect: {}'.format(result))

    print('Starting configuration anyway in simulation')
    result = False

    if result is False:
        wm.start_config()
    else:
        print('Successfully connected to a network :)')


if __name__ == "__main__":
    main()
