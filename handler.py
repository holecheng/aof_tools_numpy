from datetime import datetime
from strategy import Strategy
from config_parse import config
import numpy as np

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
    def cleaning(self, nps: np.ndarray):
        return self.get_group_avg(nps)

    @staticmethod
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


class NpAnalysis:
    def __init__(self, strategy: Strategy, nps):
        self.strategy = strategy
        self.nps = nps

    def clean_pds(self):
        return self.strategy.cleaning(self.nps)


def get_analysis(strategy: Strategy, nps):
    return NpAnalysis(strategy, nps).clean_pds()










