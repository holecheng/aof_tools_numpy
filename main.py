#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from config_parse import config
from numpy_handler.file_handler import NumpyReadFile
from numpy_handler.db_handler import NumpyReadDb


def run():
    if config.get_args('mode') == 'cmd':
        print('正在从命令行获取数据地址')
        NumpyReadFile(config.get_config('path'))
    elif config.get_args('mode') == 'db':
        print('正在从数据库获取数据')
        NumpyReadDb()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
