import argparse
import os
import json


file_path = os.path.dirname(os.path.abspath(__file__))


class Config(object):

    def __init__(self):
        self.config_path = os.sep.join([file_path, 'config.json'])
        self.mode = None
        self._db_host = None
        self._args = None
        self._parser = argparse.ArgumentParser(description='传递参数')
        self._init_parser()
        self.config = None
        self._init_config()

    def _init_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as file:
            self.config = json.load(file)

    def _init_parser(self):
        self._parser.add_argument('--select-time', type=str, nargs='?', help='起始时间')
        self._parser.add_argument('--player', type=str, nargs='?', help='玩家pid')
        self._parser.add_argument('--flop', type=str, nargs='?', help='flop保险')
        self._parser.add_argument('--turn', type=str, nargs='?', help='turn保险')
        self._parser.add_argument('--path', type=str, nargs='?', help='文件路径')
        self._parser.add_argument('--mode', type=str, nargs='?', help='数据库连接方式', default='cmd')
        self._parser.add_argument('--query-time', type=str, nargs='?', help='数据库连接筛选时段')
        self._args = self._parser.parse_args()

    def get_args(self, key):
        return getattr(self._args, key)


config = Config()






