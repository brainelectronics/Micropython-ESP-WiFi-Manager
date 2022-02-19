#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
boot script, do initial stuff here, similar to the setup() function on Arduino
"""

import esp
import gc
import network
import time

# custom packages
from helpers.led_helper import Led


# set clock speed to 240MHz instead of default 160MHz
# machine.freq(240000000)

# disable ESP os debug output
esp.osdebug(None)

led = Led()
led.flash(amount=3, delay_ms=50)
led.turn_on()

station = network.WLAN(network.STA_IF)
if station.active() and station.isconnected():
    station.disconnect()
station.active(False)
time.sleep_ms(1000)
station.active(True)

led.turn_off()

# run garbage collector at the end to clean up
gc.collect()

print('Finished booting')
