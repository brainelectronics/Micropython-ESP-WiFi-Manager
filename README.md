# ESP WiFi Manager

[![Downloads](https://pepy.tech/badge/micropython-esp-wifi-manager)](https://pepy.tech/project/micropython-esp-wifi-manager)
![Release](https://img.shields.io/github/v/release/brainelectronics/micropython-esp-wifi-manager?include_prereleases&color=success)
![MicroPython](https://img.shields.io/badge/micropython-Ok-green.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/brainelectronics/micropython-esp-wifi-manager/actions/workflows/release.yml/badge.svg)](https://github.com/brainelectronics/micropython-esp-wifi-manager/actions/workflows/release.yml)

MicroPython WiFi Manager to configure and connect to networks

-----------------------

<!-- MarkdownTOC -->

- [Installation](#installation)
	- [Install required tools](#install-required-tools)
	- [Flash firmware](#flash-firmware)
	- [Upload files to board](#upload-files-to-board)
		- [Install package with pip](#install-package-with-pip)
		- [Manually](#manually)
			- [Upload files to board](#upload-files-to-board-1)
			- [Install additional MicroPython packages](#install-additional-micropython-packages)
- [Usage](#usage)

<!-- /MarkdownTOC -->

## Installation

### Install required tools

Python3 must be installed on your system. Check the current Python version
with the following command

```bash
python --version
python3 --version
```

Depending on which command `Python 3.x.y` (with x.y as some numbers) is
returned, use that command to proceed.

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Test both tools by showing their man/help info description.

```bash
esptool.py --help
rshell --help
```

### Flash firmware

To flash the [micropython firmware][ref-upy-firmware-download] as described on
the micropython firmware download page, use the `esptool.py` to erase the
flash before flashing the firmware.

```bash
esptool.py --chip esp32 --port /dev/tty.SLAB_USBtoUART erase_flash
esptool.py --chip esp32 --port /dev/tty.SLAB_USBtoUART --baud 460800 write_flash -z 0x1000 esp32-20210623-v1.16.bin
```

If the Micropython board is equipped with an external PSRAM chip, the
`esp32spiram-20210623-v1.16.bin` can also be used for ESP32 devices. If there
is no external PRSAM only the non SPIRAM version is working.

### Upload files to board

#### Install package with pip

Connect your MicroPython board to a network

```python
import network
station = network.WLAN(network.STA_IF)
station.connect('SSID', 'PASSWORD')
station.isconnected()
```

and install this lib on the MicroPython device like this

```python
import upip
# may use the latest test version of it, by adding test.pypi.org as the first
# location to search for the package
# upip.index_urls = ["https://test.pypi.org/pypi", "https://micropython.org/pi", "https://pypi.org/pypi"]
upip.install('micropython-esp-wifi-manager')
# its dependencies will be installed alongside

# if test.pypi.org is added to the index urls, required depencendies won't be
# installed if they are not available from test.pypi.org, may install them
# manually
# upip.index_urls = ["https://micropython.org/pi", "https://pypi.org/pypi"]
# upip.install('micropython-ulogging')
# upip.install('utemplate')
```

#### Manually

##### Upload files to board

Copy the module(s) to the MicroPython board and import them as shown below
using [Remote MicroPython shell][ref-remote-upy-shell]

Open the remote shell with the following command. Additionally use `-b 115200`
in case no CP210x is used but a CH34x.

```bash
rshell -p /dev/tty.SLAB_USBtoUART --editor nano
```

Create compressed CSS and JS files as described in the
[simulation static files README](simulation/static) to save disk space on the
device and increase the performance (webpages are loading faster)

```bash
mkdir /pyboard/lib/
mkdir /pyboard/lib/microdot/
mkdir /pyboard/lib/wifi_manager/
mkdir /pyboard/lib/wifi_manager/static/
mkdir /pyboard/lib/wifi_manager/static/css
cp static/css/*.gz /pyboard/lib/wifi_manager/static/css
# around 24kB compared to uncompressed 120kB

# optional, not used so far
# mkdir /pyboard/lib/wifi_manager/static/js
# cp static/js/*.gz /pyboard/lib/wifi_manager/static/js
# around 12kB compared to uncompressed 40kB

mkdir /pyboard/lib/wifi_manager/templates/
cp templates/* /pyboard/lib/wifi_manager/templates/
# around 20kB

cp wifi_manager/* /pyboard/lib/wifi_manager/
cp microdot/* /pyboard/lib/microdot/
cp main.py /pyboard
cp boot.py /pyboard
# around 40kB
```

##### Install additional MicroPython packages

As this package has not been installed with `upip` additional modules are
required, which are not part of this repo. To install these modules on the
device, connect to a network and install them via `upip` as follows

```python
import upip

upip.install('utemplate')
upip.install('micropython-ulogging')
upip.install('micropython-brainelectronics-helper')
```

## Usage

After all files have been transfered or installed open a REPL to the device.

The device will try to load and connect to the configured networks based on an
encrypted JSON file.

In case no network has been configured or no connection could be established
to any of the configured networks within the timeout of each 5 seconds an
AccessPoint at `192.168.4.1` is created.

A simple Picoweb webserver is hosting the webpages to connect to new networks,
to remove already configured networks from the list of connections to
establish and to get the latest available networks as JSON.

This is a list of available webpages

| URL | Description |
|-----|-------------|
| `/`   | Root index page, to choose from the available pages |
| `/select` | Select and configure a network |
| `/configure` | Manage already configured networks |
| `/scan_result` | JSON of available networks |

To leave from the Webinterface, just press CTRL+C and wait until all threads
finish running. This takes around 1 second. The device will return to its REPL

<!-- Links -->
[ref-esptool]: https://github.com/espressif/esptool
[ref-remote-upy-shell]: https://github.com/dhylands/rshell
[ref-upy-firmware-download]: https://micropython.org/download/
