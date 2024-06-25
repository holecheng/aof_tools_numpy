from group.group_base import AddSystem, Base
from config_parse import config


class EvOutcomeBase(AddSystem):
    __slots__ = ('group',
                 'group_key',  # 几人场
                 'avg_ev_player',
                 'avg_outcome_player',
                 'diff_ev_outcome',
                 'counts',  # 符合条件的计数
                 'sum_ev_player',
                 'sum_outcome_player',
                 'total',
                 'row_dic'  # 数据字典
                 )

    def __init__(self, group, row_dic=None, total=None):
        super().__init__()
        if hasattr(self, '__slots__'):
            for i in self.__slots__:
                self.__setattr__(i, 0)
        self.group = group
        self.group_key = self.find_group_key(row_dic)
        self.row_dic = row_dic
        self.total = total
        self._init_row_dic()

    def __str__(self):
        return f'group_key； {self.group_key}， group； {self.group}'
        
    def __eq__(self, other):
        if self.total:
            return True
        return self.group == other.group and self.group_key == self.find_group_key(other.row_dic)

    def _init_row_dic(self):
        self.counts = 1
        self.covert(self.row_dic, 'init')
        return self
    
    def covert(self, row_dic, types=None):
        if types:
            self.add_or_init('ev_player', row_dic, types='init')
            self.add_or_init('outcome_player', row_dic, types='init')
        else:
            self.add_or_init('ev_player', row_dic)
            self.add_or_init('outcome_player', row_dic)
        self.diff_ev_outcome = self.avg_outcome_player - self.avg_ev_player

    def __add__(self, other):
        row_dic = other.row_dic
        self.covert(row_dic)
        return self

    @staticmethod
    def find_group_key(row_dic):
        if config.get_args('slide'):
            interval, appended = map(int, config.get_args('slide').strip().split(','))   # 10000， 4000
            if not interval:
                print('错误的分区')
                exit(0)
            cnt_id = row_dic['cnt_id']
            c, d = map(int, divmod(cnt_id, interval))
            if d < appended:
                key_list = [f'{c}-{0}']
            else:
                key_list = [f'{c}-{d // appended}', f'{c}-{d // appended + 1}']
            return '..'.join(key_list)
        else:
            return None
