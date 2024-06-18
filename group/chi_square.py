import json

from group.group_base import AddSystem


class ChiSquareCheck(AddSystem):
    __slots__ = ('group',
                 'group_key',  # 几人场
                 'matrix_dic',  # 排名矩阵
                 'avg_ev_player',
                 'avg_outcome_player',
                 'diff_ev_outcome',
                 'total',
                 'counts',  # 符合条件的计数
                 'sum_ev_player',
                 'sum_outcome_player',
                 'row_dic'   # 数据字典
                 )

    def __init__(self, group, row_dic, total=None):
        super().__init__()
        if hasattr(self, '__slots__'):
            for i in self.__slots__:
                self.__setattr__(i, 0)
        self.group = group
        self.group_key = self.find_group_key(row_dic)
        self.total = total
        self.row_dic = row_dic
        self.matrix_dic = {}
        self.covert(self.row_dic, types='init')

    def __eq__(self, other):
        group_key = self.find_group_key(other.row_dic)
        return self.group == other.group and self.group_key == group_key

    def __add__(self, other):
        row_dic = other.row_dic
        self.covert(row_dic)
        return self

    def covert(self, row_dic, types=None):
        if not row_dic.get('turn'):
            return self
        pid_case = row_dic.get('pid_case')
        if not pid_case or pid_case == 'null':
            return self  # 没有数据不计入
        if not isinstance(pid_case, dict):
            pid_case = json.loads(pid_case)
        try:
            final_ranks = pid_case.get('final_ranks')
            showdown_ranks = pid_case.get('showdown_ranks')
        except Exception:
            return self  # 没有数据不计入
        self.counts += 1
        if types:
            self.add_or_init('ev_player', row_dic, types='init')
            self.add_or_init('outcome_player', row_dic, types='init')
        else:
            self.add_or_init('ev_player', row_dic)
            self.add_or_init('outcome_player', row_dic)
        self.diff_ev_outcome = self.avg_outcome_player - self.avg_ev_player
        ai_list = row_dic.get('ai_list')
        for i, v in enumerate(ai_list):
            if v == 1:  # 判断是不是AI
                final_rank = final_ranks[i]
                showdown_rank = showdown_ranks[i]
                for k, p in enumerate(showdown_rank):
                    if p == 0:
                        continue
                    if not self.matrix_dic.get(k):
                        self.matrix_dic[k] = {'∑p0': 0, '∑x': 0}
                    p0 = p / sum(showdown_rank)
                    self.matrix_dic[k]['∑p0'] += p0
                    if final_rank[k]:
                        self.matrix_dic[k]['∑x'] += 1

    @staticmethod
    def find_group_key(row_dic):
        return int(row_dic.get('ai_count') + row_dic.get('player_count'))






