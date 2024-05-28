import logging

from db.db_loader import DBLoader


logger = logging.getLogger()


def init_query():
    # todo此处可以对处理数据进行进一步query筛选
    with DBLoader() as db:
        result = db.run_query()
        for i, history in enumerate(result):
            print('{} : {}'.format(i, history))
    return ''


class NumpyReadDb:

    def __init__(self):
        result = init_query()


