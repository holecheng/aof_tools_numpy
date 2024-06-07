from config_parse import config


class Base(object):

    def __init__(self, group, row_dic=None, total=None):
        if hasattr(self, '__slots__'):
            for i in self.__slots__:
                self.__setattr__(i, 0)
        self.group = group  # 对应row_dic的key  date, pId
        self.row_dic = row_dic
        self.allowance = config.get_args('allowance')
        if total:
            self.group_key = 'total'
        else:
            self.group_key = self.return_group_key(row_dic)

    def return_group_key(self, row_dic):
        group_merge = ''  # 返回的键值 '1,2'
        for i in self.group.split('**'):
            if group_merge:
                group_merge += '**'
            group_merge += str(self.get_group_key(i, row_dic))
        return group_merge

    @staticmethod
    def resize_insurance(row_key):
        must_key = ['is_leader_flop', 'is_leader_turn', 'flop_i', 'turn_i']
        if not all(elem in row_key for elem in must_key):
            return ''
        return '{}{}_{}{}'.format(*[row_key[key] for key in must_key])

    def get_group_key(self, group, row_dic=None):
        group_key = row_dic[group]
        if self.allowance:
            ans_group_key = str(int(group_key) // self.allowance)
        elif config.get_args('insurance'):
            ans_group_key = str(self.resize_insurance(row_dic))
        else:
            ans_group_key = str(group_key)
        return ans_group_key


