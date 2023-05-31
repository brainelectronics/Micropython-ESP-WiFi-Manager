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
		- [Install package](#install-package)
		- [General](#general)
		- [Specific version](#specific-version)
		- [Test version](#test-version)
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

#### Install package

Connect your MicroPython board to a network

```python
import network
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect('SSID', 'PASSWORD')
station.isconnected()
```

#### General

Install the latest package version of this lib on the MicroPython device

```python
import mip
mip.install("github:brainelectronics/micropython-esp-wifi-manager")

# maybe install the dependencies manually afterwards
# mip.install("github:brainelectronics/micropython-modules")
```

For MicroPython versions below 1.19.1 use the `upip` package instead of `mip`

```python
import upip
upip.install('micropython-esp-wifi-manager')
# dependencies will be installed automatically
```

#### Hook the WiFi Manager logic into `/boot.py` and `/main.py`

Because the `mip` installation will not install files outside of `/lib`, to run the WiFi Manager at startup,
add this line to your `/boot.py`:

```python
import wifi_manager.boot
```

And also add this line to your `/main.py`, before your application code:

```python
import wifi_manager.main
```

#### Specific version

Install a specific, fixed package version of this lib on the MicroPython device

```python
import mip
# install a verions of a specific branch
mip.install("github:brainelectronics/micropython-esp-wifi-manager", version="feature/support-mip")
# install a tag version
mip.install("github:brainelectronics/micropython-esp-wifi-manager", version="1.7.0")
```

#### Test version

Install a specific release candidate version uploaded to
[Test Python Package Index](https://test.pypi.org/) on every PR on the
MicroPython device. If no specific version is set, the latest stable version
will be used.

```python
import mip
mip.install("github:brainelectronics/micropython-esp-wifi-manager", version="1.7.0-rc5.dev22")
```

For MicroPython versions below 1.19.1 use the `upip` package instead of `mip`

```python
import upip
# overwrite index_urls to only take artifacts from test.pypi.org
upip.index_urls = ['https://test.pypi.org/pypi']
upip.install('micropython-esp-wifi-manager')
```

See also [brainelectronics Test PyPi Server in Docker][ref-brainelectronics-test-pypiserver]
for a test PyPi server running on Docker.

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
mkdir /pyboard/lib/utemplate/
mkdir /pyboard/lib/wifi_manager/
mkdir /pyboard/lib/static/
mkdir /pyboard/lib/static/css
mkdir /pyboard/lib/static/js

cp static/css/*.gz /pyboard/lib/static/css
cp static/js/*.gz /pyboard/lib/static/js
# around 24kB compared to uncompressed 120kB

# optional, not used so far
# mkdir /pyboard/lib/static/js
# cp static/js/*.gz /pyboard/lib/static/js
# around 12kB compared to uncompressed 40kB

mkdir /pyboard/lib/templates/
cp templates/* /pyboard/lib/templates/
# around 20kB

cp wifi_manager/* /pyboard/lib/wifi_manager/
cp microdot/* /pyboard/lib/microdot/
cp utemplate/* /pyboard/lib/utemplate/
cp main.py /pyboard
cp boot.py /pyboard
# around 40kB
```

##### Install additional MicroPython packages

As this package has not been installed with `upip` additional modules are
required, which are not part of this repo.

Connect the board to a network and install the package like this for
MicroPython 1.20.0 or never

```python
import mip
mip.install("github:brainelectronics/micropython-modules")
```

For MicroPython versions below 1.19.1 use the `upip` package instead of `mip`

```python
import upip
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
| `/configure` | Manage already configured networks |
| `/scan_result` | JSON of available networks |
| `/shutdown` | Shutdown webserver and return from `run` function |

To leave from the Webinterface, just press CTRL+C and wait until all threads
finish running. This takes around 1 second. The device will return to its REPL

<!-- Links -->
[ref-esptool]: https://github.com/espressif/esptool
[ref-remote-upy-shell]: https://github.com/dhylands/rshell
[ref-brainelectronics-test-pypiserver]: https://github.com/brainelectronics/test-pypiserver
[ref-upy-firmware-download]: https://micropython.org/download/
