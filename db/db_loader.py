import pymongo
import logging
from config_parse import config
from datetime import datetime


logger = logging.getLogger()


class DBLoader:

    def __init__(self):
        self.query = dict()
        self._db_name = config.get_args('db_name')
        self._table_name = config.get_args('table_name')
        self.db = None

    def __enter__(self):
        self._load_data_from_db()
        self._init_query()
        logger.info("query:{}".format(self.query))

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.close()

    def _load_data_from_db(self):
        if config.get_args('mode') != 'db':
            return ''
        configs = config.config
        conn = pymongo.MongoClient(host=configs["db_host"])
        try:
            if configs.get('password') and configs.get('root'):
                conn.authenticate(configs.get('root'), configs.get('password'))
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


db_col = DBLoader()



