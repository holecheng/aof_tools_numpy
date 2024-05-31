import collections

import pymongo
import logging
from config_parse import config
from datetime import datetime

logger = logging.getLogger()

COLUMNS = ['river', 'nash_range', 'players', 'turn', 'reqid', 'version', 'command', 'winners', 'ev'
           'outcome', 'blindLevel', 'handNumber', 'leagueName']


class DBLoader:

    def __init__(self):
        self.query = dict()
        self._configs = config.config
        self._db_name = self._configs.get('db_name')
        self._table_name = self._configs.get('table_name')
        self.conn = None
        self.db = None

    def __enter__(self):
        self._load_data_from_db()
        self._init_query()
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
        pid_columns = {'heroIndex', 'players'}
        dic_zero = dict.fromkeys(list(set(COLUMNS) - pid_columns))
        dic_one = dict.fromkeys(pid_columns)
        dic_zero.update(dic_one)
        pid_set = get_pid_set(self.db.find(self.query, dic_zero))
        print(pid_set)
        return pid_set


def get_pid_set(result):
    pid_set = set()
    for i in result:
        line = i.copy()
        hero_index = int(line.get('heroIndex', -1))
        if hero_index != -1:
            players = line.pop('players')
            p_id = players[hero_index].get('pId')
            if p_id:
                pid_set.add(p_id)
    return pid_set


db_col = DBLoader()
