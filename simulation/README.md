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

use [bootstrap 3.4](https://getbootstrap.com/docs/3.4/getting-started/#download)

## Unittests

```bash
# run all unittests
python -m nose2 -v tests

# run all unittests of a class
python -m nose2 -v tests.test_wifi_manager

# run an unittest of a specific function
python -m nose2 -v tests.test_wifi_manager.TestWiFiManager.test_init
```

## Usage

Run the simulation of the ESP WiFi Manager **after** activating the virtual
environment of the [Setup section](#setup)

```bash
cd src
python run_simulation.py
```

Open [`http://127.0.0.1:5000/`](http://127.0.0.1:5000/) in a browser
