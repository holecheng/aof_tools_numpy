from config_parse import config
from utils import resize_insurance


class Blinds:
    __slots__ = ('group',  # 组
                 'group_key',  # 分组值
                 'allowance',
                 'avg_ev',  # 平均的期望
                 'avg_outcome',  # 实际期望
                 'diff_ev_outcome',  # 结果期望差
                 'avg_flop_ev',  # 第一轮三张牌之后的期望（均值）
                 'avg_turn_ev',  # turn牌发出来的期望（均值）
                 'avg_sum_stack',  # 场内ai所持砝码
                 'avg_compare_stack',  # 场内ai所持砝码对比对方所持砝码
                 # 'avg_stack', '',
                 'counts',  # 总对局数-同一局按AI出现次数计
                 'turn_count',  # 分发到第一张牌的总场次  turn-counts 因为发了turn一定会继续下去所以计算一个
                 # 'flop_count',  # 分发三张牌的场次  flop-counts
                 'sum_ev',
                 'sum_outcome',
                 'sum_flop_ev',
                 'sum_turn_ev',
                 'sum_rounds',
                 'row_dic',
                 )

    def __init__(self, group, group_key, row_dic=None):
        for i in self.__slots__:
            self.__setattr__(i, 0)
        self.counts = 1
        self.group = group
        self.row_dic = row_dic
        self.allowance = config.get_args('allowance')
        print('余量计算为'.format(self.allowance))
        self.group_key = self._get_group_key(group_key)
        self._init_row_dic()

    def _init_row_dic(self):
        row_dic = self.row_dic
        self.counts = 1
        self.covert(row_dic, 'init')
        return self

    def __eq__(self, other):
        other_group_key = self._get_group_key(other.group_key, other.row_dic)
        return self.group == other.group and self.group_key == other_group_key

    def __add__(self, other):
        row_dic = other.row_dic
        self.counts += 1
        self.covert(row_dic)
        return self

    def _get_group_key(self, group_key, row_dic=None):
        if group_key == 'total':
            return group_key
        if self.allowance:
            ans_group_key = int(group_key) // self.allowance
        elif config.get_args('insurance'):
            ans_group_key = resize_insurance(row_dic)
        else:
            ans_group_key = int(group_key)
        return ans_group_key

    def covert(self, row_dic, types='add'):
        ev_player = row_dic.get('ev_player')
        outcome_player = row_dic.get('outcome_player')
        flop_ev_player = row_dic.get('flop_ev_player', 0)
        turn_ev_player = row_dic.get('turn_ev_player', 0)
        if types == 'add':
            if row_dic['is_turn']:
                self.turn_count += 1
                self.sum_flop_ev += float(flop_ev_player)
                self.sum_turn_ev += float(turn_ev_player)
                self.avg_flop_ev = self.avg_get(self.sum_ev, self.turn_count)
                self.avg_turn_ev = self.avg_get(self.sum_outcome, self.turn_count)
            else:
                self.sum_ev += float(ev_player)
                self.sum_outcome += float(outcome_player)
                self.avg_ev = self.avg_get(self.sum_ev, self.counts)
                self.avg_outcome = self.avg_get(self.sum_outcome, self.counts)
        else:
            if row_dic['is_turn']:
                self.turn_count += 1
                self.avg_flop_ev = self.sum_flop_ev = float(flop_ev_player)
                self.avg_turn_ev = self.sum_turn_ev = float(turn_ev_player)
            self.avg_ev = self.sum_ev = float(ev_player)
            self.avg_outcome = self.sum_outcome = float(outcome_player)
        self.diff_ev_outcome = self.avg_outcome - self.avg_ev

    @staticmethod
    def avg_get(sum_c, count):
        return float(sum_c) / float(count)
