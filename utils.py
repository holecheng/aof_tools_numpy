import os
import datetime
import pandas as pd
import numba as nb
import numpy as np
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


@nb.jit
def get_group_avg(nps):
    title = nps[0]
    nps = nps[1:]
    group_i = nps.index(config.get_args('group'))
    group_np = nps[: group_i]
    unique_values = np.unique(group_np)
    col = config.get_args('col').split(',')
    col_list = [group_i] + [title.index(i) for i in col]
    grouped_avg = np.zeros((len(unique_values), len(col) + 1))
    for i, val in enumerate(unique_values):
        for j, index in enumerate(col_list):
            if j == group_i:
                grouped_avg[i][j] = val
            else:
                grouped_avg[i][j] = np.mean(nps[:, index], axis=0)
    return grouped_avg


def sign_blind_level(blinds: list) -> str:
    '''
    将底池级别转化
    :param blinds:
    :return:
    '''
    return '_'.join(map(lambda x: str(int(x // 100)), blinds))







