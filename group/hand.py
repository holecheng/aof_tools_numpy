class Hand:
    __slots__ = ('group', 'group_key', 'avg_ev',
                 'avg_flop_ev',  # 第一轮三张牌之后的期望（均值）
                 'avg_turn_ev',  # turn牌发出来的期望（均值）
                 'avg_outcome',
                 'diff_ev_outcome',
                 'avg_flop_i', 'avg_turn_i', 'avg_leader_counts',
                 'avg_is_push', 'avg_is_turn', 'avg_is_flop', 'counts', 'row_dic',
                 'leader_counts', 'sum_flop_i', 'sum_turn_i', 'sum_ev',
                 'sum_flop_ev',
                 'sum_turn_ev',
                 'no_insurance', 'sum_outcome', 'sum_is_turn',
                 'sum_is_river', 'sum_is_push',
                 )

    def __init__(self, group, group_key, row_dic=None):
        for i in self.__slots__:
            self.__setattr__(i, 0)
        self.group = group
        self.group_key = group_key
        self.row_dic = row_dic
        self._init_row_dic()

    def _init_row_dic(self):
        self.counts = 1
        if self.row_dic['is_turn']:
            self.sum_is_turn = 1
            flop_ev_player = self.row_dic.get('flop_ev_player', 0)
            turn_ev_player = self.row_dic.get('turn_ev_player', 0)
            self.avg_flop_ev = self.sum_flop_ev = float(flop_ev_player)
            self.avg_turn_ev = self.sum_turn_ev = float(turn_ev_player)
        if self.row_dic.get('is_leader'):
            self.leader_counts = 1
            flop_i = self.row_dic.get('flop_i')
            turn_i = self.row_dic.get('turn_i')
            self.sum_flop_i = flop_i
            self.avg_flop_i = flop_i
            self.avg_turn_i = turn_i
            self.sum_turn_i = turn_i
            if not any([turn_i, flop_i]):
                self.no_insurance += 1  # 未买保险场次
        ev_player = self.row_dic.get('ev_player')
        outcome_player = self.row_dic.get('outcome_player')
        self.avg_is_push = self.sum_is_push = self.row_dic.get('is_push')
        self.avg_ev = self.sum_ev = float(ev_player)
        self.avg_outcome = self.sum_outcome = float(outcome_player)
        self.diff_ev_outcome = self.avg_outcome - self.avg_ev

    def __eq__(self, other):
        return self.group == other.group and self.group_key == other.group_key

    def __add__(self, other):
        row_dic = other.row_dic
        self.counts += 1  # 有效落座场次
        self.sum_is_turn += row_dic.get('is_turn')  # 是否turn
        self.sum_is_river += row_dic.get('is_river')  # 是否存在river
        self.avg_is_flop = self.avg_get(self.sum_is_river, self.counts)
        self.avg_is_turn = self.avg_get(self.sum_is_turn, self.counts)
        self.leader_counts += row_dic.get('is_leader')  # 领先总场次
        if row_dic['is_turn']:
            self.sum_is_turn += 1
            flop_ev_player = row_dic.get('flop_ev_player', 0)
            turn_ev_player = row_dic.get('turn_ev_player', 0)
            self.sum_flop_ev += float(flop_ev_player)
            self.sum_turn_ev += float(turn_ev_player)
            self.avg_flop_ev = self.avg_get(self.sum_ev, self.sum_is_turn)
            self.avg_turn_ev = self.avg_get(self.sum_outcome, self.sum_is_turn)
        if row_dic.get('is_leader'):
            flop_i = row_dic.get('flop_i')
            turn_i = row_dic.get('turn_i')
            self.sum_flop_i += flop_i
            self.sum_turn_i += turn_i
            if not any([turn_i, flop_i]):
                self.no_insurance += 1  # 未买保险场次
                self.avg_leader_counts = self.avg_get(self.no_insurance, self.sum_is_turn)
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
        self.diff_ev_outcome = self.avg_outcome - self.avg_ev
        return self

    @staticmethod
    def avg_get(sum_c, count):
        return float(sum_c) / float(count)
