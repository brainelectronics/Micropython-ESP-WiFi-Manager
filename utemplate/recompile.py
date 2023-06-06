#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file has been copied from micropython-lib

https://github.com/pfalcon/utemplate/tree/181b974fb41c726f4f1a27d9d9fffac7407623f4/utemplate

(c) 2014-2020 Paul Sokolovsky. MIT license.
"""

try:
    from uos import stat, remove
except ImportError:
    from os import stat, remove
from . import source


class Loader(source.Loader):

    def load(self, name):
        o_path = self.pkg_path + self.compiled_path(name)
        i_path = self.pkg_path + self.dir + "/" + name
        try:
            o_stat = stat(o_path)
            i_stat = stat(i_path)
            if i_stat[8] > o_stat[8]:
                # input file is newer, remove output to force recompile
                remove(o_path)
        finally:
            return super().load(name)
