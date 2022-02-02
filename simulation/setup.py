#!/usr/bin/env python3

"""
A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup
import pathlib
import shutil

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

# Clean up previous builds
if pathlib.Path('build').is_dir():
    shutil.rmtree('build', ignore_errors=True)
if pathlib.Path('dist').is_dir():
    shutil.rmtree('dist', ignore_errors=True)

setup(
    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    #
    # For a discussion on single-sourcing the version across setup.py and the
    # project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    # version='2.0.0',  # Required
    use_scm_version=True,
)
