# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
## [x.y.z] - yyyy-mm-dd
### Added
### Changed
### Removed
### Fixed
-->

## [Unreleased]

## [0.1.0] - 2022-02-06
### Added
- This changelog file
- Empty [`LICENSE.md`](LICENSE.md) file
- [Micropython helpers](helpers) submodule
- [`.gitignore`](.gitignore) file
- [Micropython primitives](primitives)
- [Static CSS](static) and [HTML template](templates) files
- Initial [`WiFi Manager`](wifi_manager.py) implementation
- Micropython [`boot`](boot.py) and [`main`](main.py) files
- [`README`](README.md) and [`requirements.txt`](requirements.txt) files
- Compressed version of
  [`bootstrap.min.css`](simulation/static/css/bootstrap.min.css) and
  [`bootstrap.min.js`](simulation/static/js/bootstrap.min.js)
- Scan only for available networks if `start_config` is called

#### Simulation
- [`Simulation README`](simulation/README.md) file
- [`.coverage`](simulation/.coveragerc) and [`.flake8`](simulation/.flake8) file
- [`requirements.txt`](simulation/requirements.txt) file
- Empty [`LICENSE.txt`](simulation/LICENSE.txt) file
- Setup [cfg](simulation/setup.cfg) and [py](simulation/setup.py) files
- [Static CSS](simulation/static/CSS), [JavaScript](simulation/static/js) and
  [HTML template](templates) files
- [`GenericHelper`](simulation/src/generic_helper/generic_helper.py),
  [`Neopixel`](simulation/src/led_helper/led_helper.py),
  [`PathHelper`](simulation/src/path_helper/path_helper.py),
  [`WifiHelper`](simulation/src/wifi_helper/wifi_helper.py) and
  [`WiFiManager`](simulation/src/wifi_manager/wifi_manager.py) files
- main [simulation file](simulation/src/run_simulation.py)
- [Simple bash script](simulation/run.sh) to start simulation
- Fake implementation of Micropython's [machine](simulation/src/machine)
  including [`RTC`](simulation/src/machine/rtc.py) and
  [`Pin`](simulation/src/machine/pin.py)
- [`TimeHelper`](simulation/src/time_helper/time_helper.py) class
- Fake implementation of Micropython's
  [neopixel](simulation/src/led_helper/neopixel.py)
- Fake implementation of Micropython's
  [network station and client](simulation/src/wifi_helper/network.py)
- Bash script to prepare all folders for a unittest coverage report
- Unittests for all modules and fakes
- Render list of selectable networks in Python and provide result via API
- `sendfile` function implemented in same way as on Micropythons PicoWeb

<!-- Links -->
[Unreleased]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager/compare/0.1.0...develop


[0.1.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/0.1.0
