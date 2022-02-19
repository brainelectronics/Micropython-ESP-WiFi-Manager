#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Path Helper

Provide unavailable path functions for Micropython boards
"""

# import os
from pathlib import Path


class PathHelper(object):
    """docstring for PathHelper"""
    def __init__(self):
        pass

    # There's currently no os.path.exists() support in MicroPython
    @staticmethod
    def exists(path: str) -> bool:
        """
        Check existance of file at given path.

        :param      path:   The path to the file
        :type       path:   str

        :returns:   Existance of file
        :rtype:     bool
        """
        result = Path(path).exists()
        return result

        """
        result = False

        path_to_file_list = path.split('/')
        # ['path', 'to', 'some', 'file.txt']

        root_path = ''
        # if sys.platform == 'esp32':
        # if sys.platform not in ['aix', 'linux', 'win32', 'cygwin', 'darwin']:
        #     root_path = ''
        # else:
        #     root_path = os.path.dirname(os.path.abspath(__file__))
        # print('The root path: {}'.format(root_path))

        this_path = root_path
        for ele in path_to_file_list[:-1]:
            files_in_dir = os.listdir(this_path)
            # print('Files in {}: {}'.format(this_path, files_in_dir))

            if ele in files_in_dir:
                # print('"{}" found in "{}"'.format(ele, files_in_dir))

                if this_path == '':
                    this_path += '{}'.format(ele)
                else:
                    this_path += '/{}'.format(ele)

                # print('Next folder to be checked is: {}'.format(this_path))
            else:
                return result

        files_in_dir = os.listdir(this_path)
        if path_to_file_list[-1] in files_in_dir:
            # print('File "{}" found in "{}"'.
            #       format(path_to_file_list[-1], this_path))
            return True
        else:
            return False
        """
