import collections
import json

import pymongo
import logging

import redis

from config_parse import config
from datetime import datetime

logger = logging.getLogger()

COLUMNS = ['river', 'nash_range', 'players', 'turn', 'reqid', 'version', 'command', 'winners', 'ev',
           'outcome', 'blindLevel', 'handNumber', 'leagueName']


class DBLoader:

    def __init__(self):
        self.query = dict()
        self._configs = config.config
        self._db_name = self._configs.get('db_name')
        self._table_name = self._configs.get('table_name')
        self.conn = None
        self.db = None
        self.pid_set = None

    def __enter__(self):
        self._load_data_from_db()
        self._init_query()
        self._init_redis()
        logger.info("query:{}".format(self.query))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db is not None:
            self.conn.close()

    def _load_data_from_db(self):
        if config.get_args('mode') != 'db':
            return
        self.conn = pymongo.MongoClient(host=self._configs["db_host"])
        try:
            if self._configs.get('password') and self._configs.get('root'):
                self.conn.authenticate(self._configs.get('root'), self._configs.get('password'))
            # self.db = hasattr(hasattr(conn, self._db_name), self._table_name)
            self.db = self.conn.aof.history
            print("db连接成功")
        except Exception as e:
            print(e)
            raise 'db连接有误'

    def _init_query(self):
        if config.get_args('query_time'):
            start_timestamp, end_timestamp = config.get_args('query_time').split(',')
            if start_timestamp.strip() or end_timestamp.strip():
                self.query['timestamp'] = collections.defaultdict(dict)
                if start_timestamp.strip():
                    self.query['timestamp'].update({'$gt': datetime.strptime(start_timestamp.strip(),
                                                                             "%Y-%m-%d").timestamp()})
                if end_timestamp.strip():
                    self.query['timestamp'].update({'$lt': datetime.strptime(end_timestamp.strip(),
                                                                             "%Y-%m-%d").timestamp()})

    def run_query(self):
        return self.db.find(self.query)

    def run_pid_set(self):
        pid_set = set()
        for i in self.db.find(self.query):
            hero_index = int(i.get('heroIndex', -1))
            if hero_index != -1:
                players = i.pop('players')
                p_id = players[hero_index].get('pId')
                if p_id:
                    pid_set.add(p_id)
        return pid_set

    def insert_players(self, ids, dic=None):
        if dic is None:
            print('插入数据有误    #_id')
            return
        else:
            self.db.update_many({'_id': ids}, {'$set': dic})

    def _init_redis(self):
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        if r.get('pid_set') and not config.get_args('enable_r'):
            print('已获取AI PID信息')
            pid_set = r.get('pid_set')
            pid_set = set(json.loads(pid_set))
        else:
            print('正在设置AI PID信息')
            pid_set = self.run_pid_set()
            r.set('pid_set', json.dumps(list(pid_set)), ex=60*60*24)
            print('设置完毕！！！！！！')
        self.pid_set = pid_set


db_col = DBLoader()
