
class Hand:
    __slots__ = ('group', 'group_key', 'sum_ev', 'avg_ev',
                 'sum_outcome', 'avg_outcome', 'counts', 'row_dic',
                 'sum_is_turn', 'avg_is_turn', 'sum_is_river', 'avg_is_flop',
                 'sum_is_seat', 'avg_is_seat', 'sum_is_push', 'avg_is_push',
                 'all_counts', 'leader_counts', 'sum_flop_i', 'sum_turn_i',
                 'avg_flop_i', 'avg_turn_i', 'no_insurance'
                 )

    def __init__(self, group, group_key, row_dic=None):
        self.sum_ev = self.avg_ev = self.sum_outcome = self.avg_outcome = self.counts = self.sum_is_turn = 0
        self.avg_is_turn = self.sum_is_river = self.avg_is_flop = self.sum_is_seat = self.avg_is_seat = 0
        self.sum_is_push = self.avg_is_push = self.all_counts = self.leader_counts = 0
        self.sum_flop_i = self.sum_turn_i = self.avg_flop_i = self.avg_turn_i = self.no_insurance = 0
        self.group = group
        self.group_key = group_key
        self.row_dic = row_dic

    def __eq__(self, other):
        return self.group == other.group and self.group_key == other.group_key

    def __add__(self, other):
        self.all_counts += 1  # 总场次
        row_dic = other.row_dic
        self.sum_is_seat += row_dic.get('is_seat')
        self.avg_is_seat = self.avg_get(self.sum_is_seat, self.all_counts)
        if not row_dic.get('is_seat'):
            return self
        self.counts += 1  # 有效落座场次
        self.sum_is_turn += row_dic.get('is_turn')  # 是否turn
        self.sum_is_river += row_dic.get('is_river')  # 是否存在river
        self.avg_is_flop = self.avg_get(self.sum_is_river, self.counts)
        self.avg_is_turn = self.avg_get(self.sum_is_turn, self.counts)
        self.leader_counts += row_dic.get('is_leader')  # 领先总场次
        if row_dic.get('is_leader'):
            flop_i = row_dic.get('flop_i')
            turn_i = row_dic.get('turn_i')
            self.sum_flop_i += flop_i
            self.sum_turn_i += turn_i
            if not any([turn_i, flop_i]):
                self.no_insurance += 1  # 未买保险场次
            self.avg_flop_i = self.avg_get(self.sum_flop_i, self.leader_counts)
            self.avg_turn_i = self.avg_get(self.sum_turn_i, self.leader_counts)
        ev_player = row_dic.get('ev_player')
        outcome_player = row_dic.get('outcome_player')
        self.sum_ev += float(ev_player)
        self.sum_is_push += row_dic.get('is_push')
        self.sum_outcome += float(outcome_player)
        self.avg_is_push = self.avg_get(self.sum_is_push, self.counts)
        self.avg_ev = self.avg_get(self.sum_ev, self.counts)
        self.avg_outcome = self.avg_get(self.sum_outcome, self.counts)
        return self

    @staticmethod
    def avg_get(sum_c, count):
        return float(sum_c/ count)




