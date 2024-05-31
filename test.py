class Hand:

    __slots__ = ('sum_ev', 'avg_ev', 'count', 'avg_outcome', 'sum_outcome', 'group', 'row_dic')

    def __init__(self, group, row_dic=None):
        for i in self.__slots__:
            self.__setattr__(i, 0)
        self.group = group
        self.row_dic = row_dic

    def __eq__(self, other):
        return self.group == other.group

    def __setattr__(self, key, value):
        if not hasattr(self, key):
            value = 0
        super().__setattr__(key, value)


print(Hand(1, 2).avg_ev)







a = [1, 2, 4]
b = [1, 2]
c = dict.fromkeys(list(set(a)-set(b)), 0)
c.update(dict.fromkeys(b, 1))
print(c)




