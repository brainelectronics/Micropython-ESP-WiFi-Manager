#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
main script, do your stuff here, similar to the loop() function on Arduino
"""

from wifi_manager import WiFiManager

wm = WiFiManager()

# if there is enough RAM on the board, may increase the buffer size on send
# stream operations to read bigger chunks from disk, default is 128
# wm.app.SEND_BUFSZ = 1024

result = wm.load_and_connect()
print('Connection result: {}'.format(result))

if result is False:
    print('Starting config server')
    wm.start_config()
else:
    print('Successfully connected to a network :)')

print('Finished booting steps of MicroPython WiFiManager')
