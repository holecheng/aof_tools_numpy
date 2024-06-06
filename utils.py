import os
import datetime

import numpy as np
from config_parse import config


def resize_timestamp(result):
    if 'timestamp' in result:
        result['timestamp'] = datetime.datetime.fromtimestamp(result['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    return result


def to_excel_numpy(nps, df_path, suffix='all'):
    with open('./output/' + os.path.basename(df_path).split('.')[0] + '_' + suffix + '.csv', 'w+', encoding='utf-8') as f:
        for i in nps:
            f.write(','.join(map(str, i)) + '\n')


def sign_blind_level(blinds: list) -> str:
    '''
    将底池级别转化
    :param blinds:
    :return:
    '''
    return '_'.join(map(lambda x: str(int(x // 100)), blinds))


def get_group_avg_nps(nps):
    title = nps[0]
    col = config.get_args('col').split(',')
    group_i = title.index(config.get_args('group'))
    col_list = [group_i] + [title.index(i) for i in col]
    npd = np.array(nps)
    return npd[:, col_list]


def remove_null_data(npd):
    try:
        npd = np.array(npd).astype(str)
        str_data = np.char.strip(npd)
        non_empty_rows = np.all(npd != '', axis=1)
        return str_data[non_empty_rows]
    except Exception as e:
        print('无法去空处理')
        return npd


def time_format_time(formats='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.fromtimestamp(1711929600.0).strftime(formats)


def resize_insurance(row_key):
    must_key = ['is_leader_flop', 'is_leader_turn', 'flop_i', 'turn_i']
    if not all(elem in row_key for elem in must_key):
        return ''
    return '{}{}_{}{}'.format(*[row_key[key] for key in must_key])


def get_group_key(group_key, row_dic=None):
    allowance = config.get_args('allowance')
    if group_key == 'total':
        return group_key
    if allowance:
        ans_group_key = int(group_key) // allowance
    elif config.get_args('insurance'):
        ans_group_key = resize_insurance(row_dic)
    else:
        ans_group_key = int(group_key)
    return allowance, ans_group_key



















