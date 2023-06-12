#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
boot script, do initial stuff here, similar to the setup() function on Arduino
"""

import gc
import network
from time import sleep


station = network.WLAN(network.STA_IF)
if station.active() and station.isconnected():
    station.disconnect()
    sleep(1)
station.active(False)
sleep(1)
station.active(True)

# run garbage collector at the end to clean up
gc.collect()

print('Finished booting steps of MicroPython WiFiManager')
