import json


class ChiSquareCheck:
    __slots__ = ('group',
                 'group_key',  # 几人场
                 'matrix_dic',  # 排名矩阵
                 'total',
                 'row_dic'   # 数据字典
                 )

    def __init__(self, group, row_dic, total=None):
        self.group = group
        self.group_key = self.find_group_key(row_dic)
        self.total = total
        self.row_dic = row_dic
        self.matrix_dic = {}
        self.covert(self.row_dic)

    def __eq__(self, other):
        group_key = self.find_group_key(other.row_dic)
        return self.group == other.group and self.group_key == group_key

    def __add__(self, other):
        row_dic = other.row_dic
        self.covert(row_dic)
        return self

    def covert(self, row_dic):
        if self.total:
            return self  # 去除total干扰
        pid_case = row_dic.get('pid_case')
        pid_case = json.loads(pid_case)
        if not pid_case:
            return self  # 没有数据不计入
        final_ranks = pid_case.get('final_ranks')
        showdown_ranks = pid_case.get('showdown_ranks')
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






