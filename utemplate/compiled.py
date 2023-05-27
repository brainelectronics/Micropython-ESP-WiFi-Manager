#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file has been copied from micropython-lib

https://github.com/pfalcon/utemplate/tree/181b974fb41c726f4f1a27d9d9fffac7407623f4/utemplate
"""


class Loader:

    def __init__(self, pkg, dir):
        if dir == ".":
            dir = ""
        else:
            dir = dir.replace("/", ".") + "."
        if pkg and pkg != "__main__":
            dir = pkg + "." + dir
        self.p = dir

    def load(self, name):
        name = name.replace(".", "_")
        return __import__(self.p + name, None, None, (name,)).render
