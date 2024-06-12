from group.group_base import Base


class Blinds(Base):
    __slots__ = ('group',  # 组
                 'group_key',  # 分组值
                 'allowance',
                 'avg_ev_player',  # 平均的期望
                 'avg_outcome_player',  # 实际期望
                 'diff_ev_outcome',  # 结果期望差
                 'avg_flop_ev',  # 第一轮三张牌之后的期望（均值）
                 'avg_turn_ev',  # turn牌发出来的期望（均值）
                 'avg_ai_stack',  # 场内ai所持砝码
                 'avg_compare_stack',  # 场内ai所持砝码对比对方所持砝码
                 'counts',  # 总对局数-同一局按AI出现次数计
                 'turn_count',  # 分发到第一张牌的总场次  turn-counts 因为发了turn一定会继续下去所以计算一个
                 'sum_ev_player',
                 'sum_outcome_player',
                 'sum_flop_ev',
                 'sum_turn_ev',
                 'sum_ai_stack',
                 'compare_stack',
                 'row_dic',
                 )

    def __init__(self, group, row_dic=None, total=None):
        super().__init__(group=group, row_dic=row_dic, total=total)
        self._init_row_dic()

    def _init_row_dic(self):
        self.counts = 1
        self.covert(self.row_dic, 'init')
        return self

    def __eq__(self, other):
        return self.group == other.group and self.return_group_key(other.row_dic) == self.group_key

    def __add__(self, other):
        row_dic = other.row_dic
        self.counts += 1
        self.covert(row_dic)
        return self

    def covert(self, row_dic, types='add'):
        print(row_dic)
        if types == 'add':
            if row_dic['is_turn']:
                self.turn_count += 1
                self.add_or_init('flop_ev', row_dic, counts=self.turn_count)
                self.add_or_init('turn_ev', row_dic, counts=self.turn_count)
            self.add_or_init('ev_player', row_dic)
            self.add_or_init('outcome_player', row_dic)
            self.add_or_init('ai_stack', row_dic)
            self.add_or_init('compare_stack', row_dic)
        else:
            if row_dic['is_turn']:
                self.turn_count += 1
                self.add_or_init('flop_ev', row_dic, types='init')
                self.add_or_init('turn_ev', row_dic, types='init')
            self.add_or_init('ev_player', row_dic, types='init')
            self.add_or_init('outcome_player', row_dic, types='init')
            self.add_or_init('ai_stack', row_dic, types='init')
            self.add_or_init('compare_stack', row_dic, types='init')
        setattr(self, 'diff_ev_outcome', self.avg_outcome_player - self.avg_ev_player)

    def add_or_init(self, suffix, row_dic, types='add', counts=None):
        if not counts:
            counts = self.counts
        if types == 'add':
            setattr(self, 'sum_' + suffix, getattr(self, 'avg_' + suffix) + float(row_dic[suffix]))
            setattr(self, 'avg_' + suffix, self.avg_get(getattr(self, 'sum_' + suffix), counts))
        else:
            setattr(self, 'avg_'+suffix, float(row_dic[suffix]))
            setattr(self, 'sum_' + suffix, float(row_dic[suffix]))

    @staticmethod
    def avg_get(sum_c, count):
        return float(sum_c) / float(count)
