import collections


class ChiSquareCheck:
    __slots__ = ('group',
                 'group_key',  # 几人场
                 'matrix_dic',  # 排名矩阵
                 'row_dic'   # 数据字典
                 )

    def __init__(self, group, row_dic):
        self.group = group
        self.group_key = self.find_group_key(row_dic)
        self.row_dic = row_dic
        self.matrix_dic = {'∑p0': collections.defaultdict(int), '∑x': collections.defaultdict(int)}
        self.covert(self.row_dic)

    def __eq__(self, other):
        group_key = self.find_group_key(other.row_dic)
        return self.group == other.group and self.group_key == group_key

    def __add__(self, other):
        row_dic = other.row_dic
        self.covert(row_dic)
        return self

    def covert(self, row_dic):
        showdown_ranks = row_dic.get('showdown_ranks')
        final_ranks = row_dic.get('final_ranks')
        ai_list = row_dic.get('ai_list')
        print(self.group_key)
        for rank in range(self.group_key):
            for i, v in enumerate(ai_list.split(',')):
                if v == '1':  # 判断是不是AI
                    final_rank = final_ranks[i]
                    showdown_rank = showdown_ranks[i]
                    for k, p in enumerate(showdown_rank):
                        if p == 0:
                            continue
                        p0 = p / sum(showdown_rank)
                        self.matrix_dic[k]['∑p0'] += p0
                        if final_rank[k]:
                            self.matrix_dic[k]['∑x'] += 1

    @staticmethod
    def find_group_key(row_dic):
        return row_dic.get('ai_count') + row_dic.get('player_count')





