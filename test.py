class Hand:

    __slots__ = ('sum_ev', 'avg_ev', 'count', 'avg_outcome', 'sum_outcome', 'group', 'row_dic')

    def __init__(self, group, row_dic=None):
        self.sum_ev = self.avg_ev = self.count = self.avg_outcome = self.sum_outcome = 0
        self.group = group
        self.row_dic = row_dic

    def __eq__(self, other):
        return self.group == other.group



li = [Hand({'play_id': 99909}, {}), Hand({'play_id': 10000}, {})]
c = Hand({'play_id': 99909}, {'ev_player':2, 'outcome_player': 3})


print(Hand.__slots__)





