
class Hand:
    __slots__ = ('group', 'group_key', 'sum_ev', 'avg_ev',
                 'sum_outcome', 'avg_outcome', 'counts', 'row_dic',
                 )

    def __init__(self, group, group_key, row_dic=None):
        self.sum_ev = self.avg_ev = self.counts = self.avg_outcome = self.sum_outcome = 0
        self.group = group
        self.group_key = group_key
        self.row_dic = row_dic

    def __eq__(self, other):
        return self.group == other.group and self.group_key == other.group_key

    def __add__(self, other):
        self.counts += 1
        row_dic = other.row_dic
        ev_player = row_dic.get('ev_player')
        outcome_player = row_dic.get('outcome_player')
        if ev_player or outcome_player:
            return self
        self.sum_ev += float(ev_player)
        self.sum_outcome += float(outcome_player)
        self.avg_ev = float(self.sum_ev / self.counts)
        self.avg_outcome = float(self.sum_ev / self.counts)
        return self
        




