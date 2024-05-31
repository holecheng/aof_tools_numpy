class Blinds:

    __slots__ = ('group',  # 组
                 'group_key',  # 分组值
                 'avg_ev',   # 平均的期望
                 'avg_outcome',  # 实际期望
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
                 'query_round',
                 'row_dic',
                 'round_count',  # 总对局数---同一对局计算一次
                 )

    def __init__(self, group, group_key, row_dic=None):
        for i in self.__slots__:
            self.__setattr__(i, 0)
        self.query_round = set()  # 用于统计是否该局号已被计入
        self.group = group
        self.group_key = group_key
        self.row_dic = row_dic

    def __eq__(self, other):
        return self.group == other.group and self.group_key == other.group_key

    def __add__(self, other):
        row_dic = other.row_dic
        if not row_dic.get('is_seat'):
            return self
        hand_number = row_dic['handNumber']
        has_record = 1
        if hand_number not in self.query_round:
            self.query_round.add(hand_number)
            has_record = 0  # 代表本次局内数据已经被记录。在统计部分数据时候不需要处理
        self.counts += 1
        self.round_count += has_record
        if not row_dic.get('is_seat'):
            return self
        if row_dic['is_turn']:
            self.turn_count += 1
            flop_ev_player = row_dic.get('flop_ev_player', 0)
            turn_ev_player = row_dic.get('turn_ev_player', 0)
            self.sum_flop_ev += round(float(flop_ev_player), 5)
            self.sum_turn_ev += round(float(turn_ev_player), 5)
            self.avg_flop_ev = self.avg_get(self.sum_ev, self.turn_count)
            self.avg_turn_ev = self.avg_get(self.sum_outcome, self.turn_count)
        ev_player = row_dic.get('ev_player')
        outcome_player = row_dic.get('outcome_player')
        self.sum_ev += round(float(ev_player), 5)
        self.sum_outcome += round(float(outcome_player), 5)
        self.avg_ev = self.avg_get(self.sum_ev, self.counts)
        self.avg_outcome = self.avg_get(self.sum_outcome, self.counts)

    @staticmethod
    def avg_get(sum_c, count):
        return round(float(sum_c / count), 5)