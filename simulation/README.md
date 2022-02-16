# ESP WiFi Manager Simulation

Simple Flask Server to create ESP WiFi Manager webpages


-----------------------


## Setup

Install all required packages with the following command in a virtual
environment to avoid any conflicts with other packages installed on your local
system.

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### Windows

On Windows the package `pycryptodome>=3.14.0,<4` shall be used instead of
`pycrypto>=2.6.1,<3`

## Bootstrap

Simulation webpages use [bootstrap 3.4][ref-bootstrap-34].

## Usage

Run the simulation of the ESP WiFi Manager **after** activating the virtual
environment of the [Setup section](#setup)

```bash
sh run.sh
```

Open [`http://127.0.0.1:5000/`](http://127.0.0.1:5000/){:target="_blank"} in a browser

## Unittests

### General

The unittests are covering a wide range of the simulation interface and use
the `nose2` package to do so.

### Usage

Run unittests for all or a single class or even for a single function as shown
onwards

### Prepare

To create the necessary coverage report directories call the
[`prepare_test.sh`](prepare_test.sh) script

```bash
cd ./

# prepare coverage directories
sh prepare_test.sh

# run all unittests
nose2 --config tests/unittest.cfg -v tests

# run all unittests of the class WiFiManager
nose2 --config tests/unittest.cfg -v tests.test_wifi_manager

# run the unittest of the "load_and_connect" function of WiFiManager class
nose2 --config tests/unittest.cfg -v tests.test_wifi_manager.TestWiFiManager.test_load_and_connect
```

### Available tests

#### Absolute truth

Test absolute truth of the unittesting framework itself.

```bash
nose2 --config tests/unittest.cfg -v tests.test_absolute_truth.TestAbsoluteTruth
```

#### Generic Helper

Test [`generic helper`][ref-generic-helper-test] implementation

```bash
nose2 --config tests/unittest.cfg -v tests.test_generic_helper.TestGenericHelper
```

#### LED Helper

Test [`led helper`][ref-led-helper-test] implementation. Currently only
the used Neopixel part of it.

```bash
nose2 --config tests/unittest.cfg -v tests.test_led_helper.TestNeopixel
```

#### Fakes

Unittests of all Micropython fake modules.

##### Machine

Test [`fake machine`][ref-machine-test] implementations.

###### Machine

```bash
nose2 --config tests/unittest.cfg -v tests.test_machine.TestMachine
```

###### Pin

```bash
nose2 --config tests/unittest.cfg -v tests.test_pin.TestPin
```

###### RTC

```bash
nose2 --config tests/unittest.cfg -v tests.test_rtc.TestRTC
```

##### Neopixel

Test [`fake neopixel`][ref-neopixel-test] implementations.

```bash
nose2 --config tests/unittest.cfg -v tests.test_neopixel.TestNeoPixel
```

##### Network

Test [`fake network`][ref-network-test] implementations.

```bash
nose2 --config tests/unittest.cfg -v tests.test_network.TestNetworkHelper
```

##### Primitives

Test [`message`][ref-message-test] implementations.

```bash
nose2 --config tests/unittest.cfg -v tests.test_message.TestMessage
```

#### Path Helper

Test [`path helper`][ref-path-helper-test] implementation.

```bash
nose2 --config tests/unittest.cfg -v tests.test_path_helper.TestPathHelper
```

#### Time Helper

Test [`time helper`][ref-time-helper-test] implementation.

```bash
nose2 --config tests/unittest.cfg -v tests.test_time_helper.TestTimeHelper
```

#### WiFi Helper

Test [`wifi helper`][ref-wifi-helper-test] implementation.

```bash
nose2 --config tests/unittest.cfg -v tests.test_wifi_helper.TestWifiHelper
```

#### WiFi Manager

Test [`wifi manager`][ref-wifi-manager-test] implementation.

```bash
nose2 --config tests/unittest.cfg -v tests.test_wifi_manager.TestWiFiManager
```

<!-- Links -->
<!-- Generic -->
[ref-bootstrap-34]: https://getbootstrap.com/docs/3.4/getting-started/#download

<!-- Unittests -->
[ref-generic-helper-test]: src/generic_helper/generic_helper.py
[ref-led-helper-test]: src/led_helper/led_helper.py

<!-- Unittests Fakes -->
[ref-machine-test]: src/machine
[ref-neopixel-test]: src/led_helper/neopixel.py
[ref-network-test]: src/wifi_helper/network.py

<!-- Unittest primitives -->
[ref-message-test]: src/generic_helper/message.py

<!-- Unittests custom modules -->
[ref-path-helper-test]: src/path_helper/path_helper.py
[ref-time-helper-test]: src/time_helper/time_helper.py
[ref-wifi-helper-test]: src/wifi_helper/wifi_helper.py
[ref-wifi-manager-test]: src/wifi_manager/wifi_manager.py
