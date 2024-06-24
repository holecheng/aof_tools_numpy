import os
import datetime

import numpy as np
from config_parse import config


def resize_timestamp(result):
    if 'timestamp' in result:
        result['timestamp'] = datetime.datetime.fromtimestamp(result['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    return result


def to_excel_numpy(nps, df_path, suffix='all'):
    f_name = './output/' + os.path.basename(df_path).split('.')[0] + '_' + suffix
    if config.get_args('month'):
        f_name = f_name + '_month'
    if config.get_args('slide'):
        f_name = f_name + '_' + config.get_args('slide')
    if config.get_args('allowance'):
        f_name = f_name + f'_allowance_{config.get_args("allowance")}'
    with open(f_name + '.csv', 'w+', encoding='utf-8') as f:
        for i in nps:
            f.write(','.join(map(lambda x: str(round(x, 5)) if isinstance(x, float) else str(x), i)) + '\n')


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


def get_chi_square_value(matrix_dic):
    # 计算卡方自由度
    chi_square_value = 0
    for _, v in matrix_dic.items():
        # {0: {'∑p0': 106.54013410011522, '∑x': 106},
        # 1: {'∑p0': 97.40170709040343, '∑x': 102},
        # 2: {'∑p0': 201.36368602475036, '∑x': 200}, 3: {'∑p0': 45.69447278473087, '∑x': 43}}
        keys = ['∑p0', '∑x']
        p0, x = (v.get(i) for i in keys)
        chi_square_value += (p0 - x) ** 2 / p0 ** 2
    return chi_square_value
