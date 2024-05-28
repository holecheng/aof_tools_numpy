import logging

from db.db_loader import db_col


logger = logging.getLogger()


class NumpyReadDb:

    def __init__(self):
        self.db_cl = db_col
        if self.db_cl.db is not None:
            self.init_query()


    def init_query(self):
        # todo此处可以对处理数据进行进一步query筛选
        with self.db_cl:
            result = self.db_cl.run_query()
            for i, history in enumerate(result):
                print('{} : {}'.format(i, history))


