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
<!--
RegEx for release version from file
r"^\#\# \[\d{1,}[.]\d{1,}[.]\d{1,}\] \- \d{4}\-\d{2}-\d{2}$"
-->

<!-- ## [Unreleased] -->

## Released
## [1.12.0] - 2023-06-12
### Added
- Instructions for using this package `boot.py` and `main.py` files
- `boot.py` and `main.py` are part of `package.json` and are installed into `wifi_manager/`, see #32 and #33

### Changed
- Ignore boot and main files during `package.json` validation

### Removed
- No device specific dependencies in `boot.py` to LED

## [1.11.0] - 2023-05-27
### Added
- `package.json` file and installation instruction for `mip` usage, see #30
- `utemplate` is part of this package to be independent from other packages, see #30
- Content of `package.json` is validated on each test workflow run
- GitHub issues template files

### Removed
- Dependency to `micropython-ulogging` and `utemplate` packages in `setup.py` file

### Fixed
- YAML syntax in all workflow files

## [1.10.0] - 2023-02-18
### Added
- `microdot_asyncio` in `microdot` folder
- `/shutdown` endpoint to stop webserver

### Changed
- All webserver functions are `async`, see #28

## [1.9.0] - 2023-02-17
### Added
- `test-release` and `release` workflows create changelog based (pre-)releases
- Copy of [`microdot 1.2.1`](https://github.com/miguelgrinberg/microdot/releases/tag/v1.2.1) provided with this package
- brainelectronics favicon is shown on all pages

### Changed
- Replace `picoweb` with `microdot`

## [1.8.0] - 2022-11-06
### Added
- Deploy to [Test Python Package Index](https://test.pypi.org/) on every PR
  build with a [PEP440][ref-pep440] compliant `-rc<BUILDNUMBER>.dev<PR_NUMBER>`
  meta data extension
- [Test release workflow](.github/workflows/test-release.yaml) running only on
  PRs is archiving and uploading built artifacts to
  [Test Python Package Index](https://test.pypi.org/)
- Added missing functions `get_uuid`, `get_system_infos_raw` and
  `get_system_infos_human` to `generic_helper` simulation files, see
  [#16][ref-issue-16]
- Added `Led` class to `led_helper` simulation file, see [#16][ref-issue-16]
- Added missing function `freq` to `machine` simulation file, see
  [#16][ref-issue-16]
- Increased coverage of simulation unittests, relates to [#16][ref-issue-16]
- Script to [create report directories](simulation/create_report_dirs.py) for
  [simulation unittests](simulation/tests) results
- Requirements files for deploy and test setup. Link with simulation
  requirements
- Script to [create report directories](simulation/create_report_dirs.py) for
  simulation unittests
- Implement `RTC` class of `rtc` simulation file, see [#16][ref-issue-16]
- Implement `Timer` class of `timer` simulation file, see [#16][ref-issue-16]
- Add all missing functions of `time_helper` simulation file,
  see [#16][ref-issue-16]
- Added missing function `value`, `on` and `off` to `pin` simulation file, see
  [#16][ref-issue-16]

### Changed
- Author is explicitly mentioned in [`setup.py`](setup.py) instead of used by
  `__author__` variable which has been previously defined in
  [`version.py`](wifi_manager/version.py) but no longer available with
  autodeploy.
- Print source code of flake8 warnings in stdout
- `unique_id` of `machine` simulation returns binary data represented by the
  hexadecimal string `DEADBEEF` instead of binary string only
- Update test data files after hexlified machine unique ID change
- Update simulation template files to latest MicroPython implementation, see
  [#16][ref-issue-16]

### Removed
- `.flake8` definition file of [`simulation`](simulation)

### Fixed
- All uncovered flake8 warnings of [`wifi_manager`](wifi_manager) and
  [`simulation`](simulation), see [#25][ref-issue-25]
- Logger level is set to `INFO` instead of `DEBUG` if `info` is specified
- Undefined `_bssid` replaced with `_essid` in `network` simulation test

## [1.7.1] - 2022-05-06
### Fixed
- `start_config` creates an AccessPoint named `WiFiManager_xxxx` with `xxxx`
  as the last four instead of first four characters of the UUID of the device,
  see [#15][ref-issue-15]

## [1.7.0] - 2022-04-18
### Added
- [`toast.js`](static/js/toast.js) and [`toast.js.gz`](static/js/toast.js.gz)
  added to show hovering alert banners, see [#21][ref-issue-21]
- Add toast JavaScript files to [`setup.py`](setup.py) to be part of twine
  distributions

### Changed
- `/select` page shows success banner after posting new network config data
  and does not return to index page anymore. `/configure` page shows success
  banner after removing a network and redirects to its page instead of
  returning to the index page, see [#21][ref-issue-21]

## [1.6.0] - 2022-04-18
### Added
- Routing for JavaScript `.js` files added, see [#18][ref-issue-18]

### Changed
- Removed source mapping from
  [`bootstrap.min.css`](static/css/bootstrap.min.css) and the compressed file
  to avoid issues as the `bootstrap.min.css.map` is not found, see
  [#19][ref-issue-19]

## [1.5.0] - 2022-04-16
### Changed
- `start_config` creates an AccessPoint named `WiFiManager_xxxx` with `xxxx`
  as the first four characters of the UUID of the device

## [1.4.0] - 2022-03-20
### Added
- Virtual oneshot timer is created and started on `latest_scan` property
  access to stop the scanning thread again after 10.5x of `scan_interval`.
  This reduces CPU load and avoids unused scans.

### Changed
- Scanning thread is started  on `latest_scan` property access
- Scan data is no logger logged with info level on `latest_scan` property
  access to reduce time before data return, see [#11][ref-issue-11]
- Neopixel is no longer used to allow user of lib to use it as desired by its
  higher level application

## [1.3.0] - 2022-03-11
### Changed
- Index page uses cards instead of list to show available pages
- Available URLs dictionary used `text`, `title` and `color` keys per URL to
  style the cards as required
- Loading spinner is shown on index page to avoid showing a not fully rendered
  or styled webpage

## [1.2.0] - 2022-03-06
### Added
- Custom logger can be provided to `run` function to enable different logging
  levels of Picoweb other than `DEBUG`

### Changed
- Neopixel is no longer fading while scan thread is running to reduce CPU load
- `gc.collect()` is no longer called on `latest_scan` property access

## [1.1.0] - 2022-02-27
### Added
- Property `connection_timeout` to control WiFi connection timeout instead of
  default fixed 5 seconds
- Property `connection_result` to get reason for failed connection
- Badges in [`README`](README.md) for number of downloads, latest release and
  license info

### Changed
- The list of available pages at the landing page is rendered from the
  elements of the `available_urls` property by `_render_index_page` in
  alphabetic order
- `WifiHelper` connects with defined `connection_timeout` to all networks

### Removed
- Primitives folder no longer used, files are part of
  [brainelectronics MicroPython helpers][ref-be-micropython-module] which is
  an install dependency to this package

## [1.0.0] - 2022-02-25
### Added
- [`setup.py`](setup.py) and [`sdist_upip.py`](sdist_upip.py) taken from
  [pfalcon's picoweb repo][ref-pfalcon-picoweb-sdist-upip] and PEP8 improved
- [`MIT License`](LICENSE)
- [`version.py`](wifi_manager/version.py) storing current library version

### Changed
- Moved all MicroPython WiFi manager files into folder named
  [`wifi_manager`](wifi_manager)
- Update [`README`](README.md) usage description of MicroPython lib deploy to
  [PyPi][ref-pypi]
- Usage examples in [`README`](README.md) updated with new import path
- Moved static web files from [`simulation/static`](simulation/static/) to
  [`static`](static)
- Adjust path to static folder in
  [WiFi Manager Simulation](simulation/src/wifi_manager/wifi_manager.py) from
  [`simulation/static`](simulation/static/) to [`static`](static)
- Update [WiFi Manager simulation](simulation/src/wifi_manager/wifi_manager.py)
  to latest MicroPython implementation
- Update [`boot`](boot.py) and [`main`](main.py) files to use `be_helpers`

### Removed
- MicroPython helpers module no longer used, replaced by pip install
  requirement
- Lib of dependency modules no longer used
- Unused `style.css` from [`static`](static)

## [0.1.1] - 2022-02-19
### Fixed
- Sleep after adding the latest found networks to the asyncio message, not
  before

## Released
## [0.1.0] - 2022-02-19
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
[Unreleased]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager/compare/1.12.0...develop

[1.12.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/1.12.0
[1.11.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/1.11.0
[1.10.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/1.10.0
[1.9.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/1.9.0
[1.8.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/1.8.0
[1.7.1]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/1.7.1
[1.7.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/1.7.0
[1.6.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/1.6.0
[1.5.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/1.5.0
[1.4.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/1.4.0
[1.3.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/1.3.0
[1.2.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/1.2.0
[1.1.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/1.1.0
[1.0.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/1.0.0
[0.1.1]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/0.1.1
[0.1.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager//tree/0.1.0

[ref-issue-16]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager/issues/16
[ref-issue-25]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager/issues/25
[ref-pep440]: https://peps.python.org/pep-0440/
[ref-issue-21]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager/issues/21
[ref-issue-18]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager/issues/18
[ref-issue-19]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager/issues/19
[ref-issue-15]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager/issues/15
[ref-issue-11]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager/issues/11
[ref-pypi]: https://pypi.org/
[ref-pfalcon-picoweb-sdist-upip]: https://github.com/pfalcon/picoweb/blob/b74428ebdde97ed1795338c13a3bdf05d71366a0/sdist_upip.py
[ref-be-micropython-module]: https://github.com/brainelectronics/micropython-modules/tree/1.1.0
