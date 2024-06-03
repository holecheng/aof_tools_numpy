from datetime import datetime
from strategy import Strategy
from config_parse import config
import numpy as np

from utils import remove_null_data


# class GroupStrategy(Strategy):
#     def cleaning(self, data: pd.DataFrame, group=0, args=None, group_type='mean') -> pd.DataFrame:
#         # todo 建议暂时用一行分组，不然显示图片会出问题 暂时不用此策略
#         domain = {}
#         if not isinstance(group, list):
#             group = [group]
#         args = args if args else [data.columns[1]]
#         for arg in args:
#             domain.update({arg: group_type})
#
#         print(data.columns, group)
#         data = data.groupby('card_num', as_index=False).agg(domain)
#         print(data)
#         # data['card_num'] = data.apply(lambda x: x['card_num'] + '(' + str(x['count']) + ')', axis=1)
#         # show_pds(data, group[0], args)
#         return data


class TimeStrategy(Strategy):
    # 针对时间做数据清洗
    def cleaning(self, data):
        select_time = config.get_args('select_time').strip()
        start = end = None
        if select_time:
            start, end = config.get_args('select_time').strip().split(',')
            if not end:
                end = datetime.now().strftime("%Y-%m-%d")
        print('正在处理 {} 到 {} 时间内的数据'.format(start, end))
        return data


class PlayerStrategy(Strategy):
    # 针对时间做数据清洗
    def cleaning(self, data):
        player_id = config.get_config('player')
        print('正在搜索玩家id:{}的游戏数据'.format(player_id))
        return data


class AvgStrategy(Strategy):
    def cleaning(self, nps):
        return self.get_group_avg(nps)

    @staticmethod
    def get_group_avg(npd: np.ndarray):
        npd = remove_null_data(npd)
        npt = npd[0]
        groups = npd[1:, 0].astype(str)
        npd = npd[1:, 1:].astype(float)
        npd = npd[~np.isnan(npd).any(axis=1)]
        unique_g = np.unique(groups)
        mean_values = []
        for group in unique_g:
            if config.get_args('types') == 'avg':
                mean_values.append(np.mean(npd[groups == group], axis=0))
            else:
                mean_values.append(np.sum(npd[groups == group], axis=0))
        ans = np.vstack(mean_values).astype(str)
        print(unique_g.shape, ans.shape)
        ans = np.hstack((unique_g.reshape(-1, 1), ans))
        return np.vstack((npt, ans))


class InsuranceStrategy(Strategy):
    def cleaning(self, data):
        turn, flop = config.get_config('turn'), config.get_config('flop')
        turn, flop = int(turn) if turn else None, int(flop) if turn else None
        print('正在搜索购买保险的对局: turn下限{}， flop下限{}的游戏对局'.format(turn, flop))
        data = data[data['turn_insurance'].notnull() | data['flop_insurance'].notna()]
        if turn:
            data = data[(data['turn_insurance'].notnull() & data['turn_insurance'] > turn) | data['flop_insurance']]
        if flop:
            data = data[(data['flop_insurance'].notnull() & data['flop_insurance'] > flop) | data['turn_insurance']]
        return data


# class NpAnalysis:
#     def __init__(self, strategy: Strategy, nps):
#         self.strategy = strategy
#         self.nps = nps
#
#     def clean_pds(self):
#         return self.strategy.cleaning(self.nps)


# def get_analysis(strategy: Strategy, nps) -> np.ndarray:
#     return NpAnalysis(strategy, nps).clean_pds()










