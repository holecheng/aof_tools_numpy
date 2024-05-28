import pymongo
import logging
from config_parse import config
from datetime import datetime


logger = logging.getLogger()


class DBLoader:

    def __init__(self):
        self.query = dict()
        self.configs = config.config
        self._db_name = self.configs.get('db_name')
        self._table_name = self.configs.get('table_name')
        self.db = None

    def __enter__(self):
        self._load_data_from_db()
        self._init_query()
        logger.info("query:{}".format(self.query))

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.close()

    def _load_data_from_db(self):
        print(config.get_args('mode'))
        if config.get_args('mode') != 'db':
            return
        conn = pymongo.MongoClient(host=self.configs["db_host"])
        try:
            if self.configs.get('password') and self.configs.get('root'):
                conn.authenticate(self.configs.get('root'), self.configs.get('password'))
            self.db = hasattr(hasattr(conn, self._db_name), self._table_name)
            logger.info("db连接成功")
        except Exception as e:
            logger.error(e)
            raise 'db连接有误'

    def _init_query(self):
        if config.get_args('query_time'):
            start_timestamp, end_timestamp = config.get_args('query_time')

            self.query['timestamp'] = {'$gt': datetime.strptime(start_timestamp, "%Y-%m-%d %H:%M:%S").timestamp(),
                                       '$lt': datetime.strptime(end_timestamp, "%Y-%m-%d %H:%M:%S").timestamp()}

    def run_query(self):
        return self.db.find(self.query)




