class Hand:

    __slots__ = ('sum_ev', 'avg_ev', 'count', 'avg_outcome', 'sum_outcome', 'group', 'row_dic')

    def __init__(self, group, row_dic=None):

        self.group = group
        self.row_dic = row_dic

    def __eq__(self, other):
        return self.group == other.group






a = [1, 2, 4]
b = [1, 2]
c = dict.fromkeys(list(set(a)-set(b)), 0)
c.update(dict.fromkeys(b, 1))
print(c)




