import os
import datetime


def resize_timestamp(result):
    if 'timestamp' in result:
        result['timestamp'] = datetime.datetime.fromtimestamp(result['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    return result


def sign_blind_level(blinds: list) -> str:
    '''
    将底池级别转化
    :param blinds:
    :return:
    '''
    return '_'.join(map(lambda x: str(int(x // 100)), blinds))







