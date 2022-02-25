# ESP WiFi Manager

MicroPython WiFi Manager to configure and connect to networks

-----------------------


## Setup

The [esptool][ref-esptool] is required to flash the micropython firmware onto
the device.

For interaction with the filesystem of the device the
[Remote MicroPython shell][ref-remote-upy-shell] can be used.

### Installation

Install both python packages with the following command in a virtual
environment to avoid any conflicts with other packages installed on your local
system.

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install esptool
pip install rshell
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

Connect to a network

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
# upip.install('picoweb')
# upip.install('micropython-ulogging')
# upip.install('utemplate')
```

#### rshell

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

cp wifi_manager/wifi_manager.py /pyboard/lib/wifi_manager/
cp main.py /pyboard
cp boot.py /pyboard
# around 40kB
```

##### Open REPL in rshell

Call `repl` in the rshell. Use CTRL+X to leave the repl or CTRL+D for a soft
reboot of the device

### Install Micropython Packages

Restart ESP device and open the printed IP address in your browser

Close all connection, and start REPL of uPyCraft or other serial connection.

```python
import upip
upip.install('picoweb')
upip.install('utemplate')
upip.install('micropython-ulogging')
upip.install('micropython-brainelectronics-helper')
```

<!-- Links -->
[ref-esptool]: https://github.com/espressif/esptool
[ref-remote-upy-shell]: https://github.com/dhylands/rshell
[ref-upy-firmware-download]: https://micropython.org/download/
