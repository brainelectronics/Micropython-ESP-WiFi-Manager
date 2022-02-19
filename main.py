#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
main script, do your stuff here, similar to the loop() function on Arduino
"""

from wifi_manager import WiFiManager

if __name__ == '__main__':
    wm = WiFiManager()
    result = wm.load_and_connect()
    wm.start_config()

    # if result is False:
    #     wm.start_config()
    # else:
    #     print('Successfully connected to a network :)')
