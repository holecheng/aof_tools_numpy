import os
import datetime

import numpy as np
import pandas as pd
import numba as nb
from config_parse import config


def resize_timestamp(result):
    if 'timestamp' in result:
        result['timestamp'] = datetime.datetime.fromtimestamp(result['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    return result


def to_excel_numpy(nps, df_path, title, suffix='all'):
    df = pd.DataFrame(nps)
    df.columns = title
    df.to_excel('./output/' + os.path.basename(df_path).split('.')[0] + '_'
                + suffix + '.xlsx', sheet_name='data', index=False)


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
        print('无法去0处理')
        return npd











