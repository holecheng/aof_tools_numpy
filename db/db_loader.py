import collections
import json

import pymongo
import logging

import redis
import requests

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
        self.r = None

    def __enter__(self):
        self._load_data_from_db()
        self._init_query()
        logger.info("处理查询数据:{}".format(self.query))
        self._init_redis()
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
        player_hash = {}
        gt_lt = self.query.copy()
        if gt_lt['timestamp'].get('$gt'):
            st = gt_lt['timestamp'].get('$gt')
            if self.r.get('update_pid_set_st') and st < float(self.r.get('update_pid_set_st')):
                gt_lt['timestamp']['$gt'] = float(self.r.get('update_pid_set_st'))
        if gt_lt['timestamp'].get('$lt'):
            et = gt_lt['timestamp'].get('$lt')
            if self.r.get('update_pid_set_et') and et < float(self.r.get('update_pid_set_et')):
                gt_lt['timestamp']['$lt'] = float(self.r.get('update_pid_set_et'))
        cnt = 0
        pid_dic = json.loads(self.r.get('pid_set'))
        print(f'缓存更新数据：{gt_lt}')
        for i in self.db.find(gt_lt):
            hero_index = int(i.get('heroIndex', -1))
            if hero_index < 0:
                continue
            players = i.get('players')
            player = players[hero_index]
            player_id = player.get('pId')
            if player_id not in player_hash:
                player_hash[player_id] = {"name": player["playerId"], "first_time": i["timestamp"]}
            if player_hash[player_id]["first_time"] > i["timestamp"]:
                player_hash[player_id]["first_time"] = i["timestamp"]
            cnt += 1
            if cnt != 0 and cnt % 10000 == 0:
                print(f'已扫描{cnt // 10000}*10000数据')
        pid_dic.update(player_hash)
        self.r.set('pid_set', json.dumps(pid_dic, ensure_ascii=False, indent=2), ex=60 * 1000 * 60 * 24)  # 半永久
        print('设置完毕！！！！！！')
        if gt_lt['timestamp'].get('$lt'):
            self.r.set('update_pid_set_et', max(float(self.get_with_default('update_pid_set_et', 0)),
                                                float(gt_lt['timestamp'].get('$lt', 0))))
        if gt_lt['timestamp'].get('$gt'):
            self.r.set('update_pid_set_st', max(float(self.get_with_default('update_pid_set_st', 0)),
                                                float(gt_lt['timestamp'].get('$gt', 0))))
        return pid_dic

    def get_with_default(self, key, default=None):
        try:
            return self.r.get(key) or default
        except redis.exceptions.RedisError:
            return default

    def insert_players(self, ids, dic=None):
        if dic is None:
            print('插入数据有误    #_id')
            return
        else:
            self.db.update_many({'_id': ids}, {'$set': dic})

    def _init_redis(self):
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)
        if self.r.get('pid_set') and not config.get_args('enable_r'):
            print('已获取AI PID信息')
            pid_set = self.r.get('pid_set')
            player_hash = json.loads(pid_set)
        else:
            print('正在设置AI PID信息')
            player_hash = self.run_pid_set()
        self.pid_set = player_hash

    def run_update(self, row_dic):
        url = 'https://aof-tools-tdse67xzfa-de.a.run.app/api/simulate_results'
        # url = 'http://10.140.0.15:52222/api/simulate_results'
        data_key = ['command', 'players', 'flop', 'turn', 'river', 'blindLevel']
        ans = self.fetch_url(url, {k: row_dic.get(k, '') for k in data_key})
        if ans:
            filters = {'_id': row_dic['_id']}
            updates = {"$set": {"pid_case": json.dumps(ans)}}
            result = self.db.update_one(filters, updates)
            print(f"Updated {result.matched_count} document(s) with {result.modified_count} modification(s), "
                  f"{row_dic['_id']}")

    @staticmethod
    def fetch_url(url, data):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "python-requests/2.20.1",
            "Content-Type": "application/json",
        }
        if not data.get('turn'):
            return
        ans = requests.post(url=url, json=data, headers=headers)
        return ans.json()


db_col = DBLoader()
