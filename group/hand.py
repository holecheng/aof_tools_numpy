
class Hand:
    __slots__ = ('group', 'group_key', 'sum_ev', 'avg_ev',
                 'sum_outcome', 'avg_outcome', 'counts', 'row_dic',
                 'sum_is_turn', 'avg_is_turn', 'sum_is_flop', 'avg_is_flop',
                 'sum_is_seat', 'avg_is_seat', 'sum_is_push', 'avg_is_push',
                 'all_counts', 'leader_counts'

                 )

    def __init__(self, group, group_key, row_dic=None):
        self.sum_ev = self.avg_ev = self.all_counts = self.leader_counts \
            = self.counts = self.avg_outcome = self.sum_outcome = 0
        self.group = group
        self.group_key = group_key
        self.row_dic = row_dic

    def __eq__(self, other):
        return self.group == other.group and self.group_key == other.group_key

    def __add__(self, other):
        self.all_counts += 1  # 总场次
        row_dic = other.row_dic
        self.leader_counts += row_dic.get('is_leader')  # 领先总场次
        self.sum_is_turn += row_dic.get('sum_is_turn')
        self.sum_is_flop += row_dic.get('sum_is_flop')
        self.avg_is_flop = self.avg_get(self.sum_is_flop, self.leader_counts)
        self.avg_is_turn = self.avg_get(self.sum_is_turn, self.leader_counts)
        ev_player = row_dic.get('ev_player')
        outcome_player = row_dic.get('outcome_player')
        self.sum_is_seat += row_dic.get('is_seat')
        self.avg_is_seat = self.avg_get(self.sum_is_seat, self.all_counts)
        if ev_player or outcome_player:
            return self
        self.counts += 1  # 有效落座场次
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




