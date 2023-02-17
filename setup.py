#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from setuptools import setup
import pathlib
import sdist_upip

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# load elements of version.py
exec(open(here / 'wifi_manager' / 'version.py').read())

setup(
    name='micropython-esp-wifi-manager',
    version=__version__,
    description="MicroPython WiFi Manager to configure and connect to networks",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager',
    author='brainelectronics',
    author_email='info@brainelectronics.de',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='micropython, brainelectronics, wifi, wifimanager, library',
    project_urls={
        'Bug Reports': 'https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager/issues',
        'Source': 'https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager',
    },
    license='MIT',
    cmdclass={'sdist': sdist_upip.sdist},
    packages=[
        'wifi_manager',
        'microdot',
    ],
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],
    data_files=[
        (
            'static',
            [
                'static/css/bootstrap.min.css',
                'static/css/bootstrap.min.css.gz',
                'static/favicon.ico',
                'static/js/toast.js',
                'static/js/toast.js.gz',
            ]
        ),
        (
            'templates',
            [
                'templates/index.tpl',
                'templates/remove.tpl',
                'templates/select.tpl',
            ]
        )
    ],
    install_requires=[
        'micropython-ulogging',
        'micropython-brainelectronics-helpers',
        'utemplate',
    ]
)
