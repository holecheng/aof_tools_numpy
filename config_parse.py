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
        self._parser.add_argument('--player', type=str, nargs='?', help='玩家pid')
        self._parser.add_argument('--flop', type=int, nargs='?', help='flop保险')
        self._parser.add_argument('--turn', type=int, nargs='?', help='turn保险')
        self._parser.add_argument('--path', type=str, nargs='?', help='文件路径')
        self._parser.add_argument('--types', type=str, nargs='?', help='聚合类型', default='avg')
        self._parser.add_argument('--mode', type=str, nargs='?', help='数据库连接方式', default='cmd')
        self._parser.add_argument('--query-time', type=str, nargs='?', help='数据库连接筛选时段')
        self._parser.add_argument('--group', type=str, nargs='?', help='分组索引')
        self._parser.add_argument('--col', type=str, nargs='?', help='分组列')
        self._parser.add_argument('--all', type=int, nargs='?', help='是否全部数据写入', default=0)
        self._parser.add_argument('--hand-detail', type=int, nargs='?', help='打印所有处理数据的pid详情', default=0)
        self._parser.add_argument('--enable-r', type=int, nargs='?', help='是否弃用redis数据', default=0)
        self._parser.add_argument('--allowance', type=int, nargs='?', help='余量', default=0)
        self._parser.add_argument('--insurance', type=int, nargs='?', help='保险影响', default=0)
        self._parser.add_argument('--simple', type=int, nargs='?', help='简单只查看ev/outcome', default=0)
        self._parser.add_argument('--update-db', type=int, nargs='?', help='是否更新数据库', default=0)
        self._parser.add_argument('--aof', type=int, nargs='?', help='原数据提取', default=0)
        self._parser.add_argument('--month', type=int, nargs='?', help='以月为单位', default=0)
        self._args = self._parser.parse_args()

    def get_args(self, key):
        return getattr(self._args, key)


config = Config()






