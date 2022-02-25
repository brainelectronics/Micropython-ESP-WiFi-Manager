# ESP WiFi Manager

Simple Flask style Micropython Server running on an ESP32


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

### Install package with pip

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

Open the remote shell with the following command. Additionally use `-b 115200`
in case no CP210x is used but a CH34x.

```bash
rshell -p /dev/tty.SLAB_USBtoUART --editor nano
```

##### Setup check

Check the board config with this simple `boards` call inside the rshell. The
result will look similar to this after the connection

```bash
Using buffer-size of 32
Connecting to /dev/tty.SLAB_USBtoUART (buffer-size 32)...
Trying to connect to REPL  connected
Retrieving sysname ... esp32
Testing if ubinascii.unhexlify exists ... Y
Retrieving root directories ... /boot.py/ /helpers/ /lib/ /main.py/ /templates/ /wifi-secure.json/ /winbond.py/
Setting time ... Oct 11, 2021 13:15:24
Evaluating board_name ... pyboard
Retrieving time epoch ... Jan 01, 2000
Welcome to rshell. Use Control-D (or the exit command) to exit rshell.
/Users/Jones/Downloads/MicroPython/ESP-Webserver-Picoweb> boards
pyboard @ /dev/tty.SLAB_USBtoUART connected Epoch: 2000 Dirs: /boot.py /static /templates /wifi_manager.py /pyboard/boot.py /pyboard/static /pyboard/templates /pyboard/wifi_manager.py
```

##### Download files (with script)

Files can be copied to the device with the following command

```bash
cp SOURCE_FILE_NAME /pyboard

# optional copy it as another file name
cp SOURCE_FILE_NAME /pyboard/NEW_FILE_NAME
```

```bash
/Users/Jones/Downloads/MicroPython/ESP-WiFi-Manager/> cp wifi_manager.py /pyboard
Copying '/Users/Jones/Downloads/MicroPython/ESP-WiFi-Manager/wifi_manager.py' to '/pyboard/wifi_manager.py' ...
```

Create compressed CSS and JS files as described in the
[simulation static files README](simulation/static) to save disk space on the
device and increase the performance (webpages are loading faster)

```bash
mkdir /pyboard/static/
cp simulation/static/css/*.gz /pyboard/static/
# around 24kB compared to uncompressed 120kB

# optional, not used so far
# mkdir /pyboard/static/
# cp simulation/static/js/*.gz /pyboard/static/
# around 12kB compared to uncompressed 40kB

mkdir /pyboard/templates
cp templates/* /pyboard/templates
# around 20kB

mkdir /pyboard/helpers
cp helpers/*.py /pyboard/helpers
# around 64kB

mkdir /pyboard/primitives
cp primitives/*.py /pyboard/primitives
# around 8kB

mkdir /pyboard/lib
cp -r lib/* /pyboard/lib
# around 72kB

cp wifi_manager.py /pyboard
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
