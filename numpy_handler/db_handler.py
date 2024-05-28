import logging

from db.db_loader import db_col


logger = logging.getLogger()


class NumpyReadDb:

    def __init__(self):
        self.db = db_col

    def init_query(self):
        # todo此处可以对处理数据进行进一步query筛选
        with self.db:
            result = self.db.run_query()
            for i, history in enumerate(result):
                logger.info('{} : {}'.format(i, history))


