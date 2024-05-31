class Hand:

    __slots__ = ['sum_ev', 'avg_ev', 'count', 'avg_outcome', 'sum_outcome', 'row_dic']

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



'''

{'_id': ObjectId('663d98886c4025e6df5356f3'), 
'river': '9s', 
'nash_range': [0.644, 0.481, 0.452, 0.0, 0.0, 0.0],
 'players': [{'isSb': False, 'playerId': 'ˇ花语', 'pId': '5253215520', 
 'straddle': 0, 'isBb': False, 'flopInsurance': [], 
 'turnInsurance': [], 'cards': 'AdJh', 'stack': 368000.0, 'seat': 2,
  'isButton': True, 'action': 'Push', 'ante': 40000.0}, 
  {'isSb': True, 'playerId': '磨磨叽叽oοО', 'pId': '5220073261', 'straddle': 0, 'isBb': False, 'flopInsurance': [], 'turnInsurance': [], 'cards': '3hAh', 'stack': 300000.0, 'seat': 6, 'isButton': False, 'action': 'Push', 'ante': 40000.0}, {'isSb': False, 'playerId': '半兽人', 'pId': '4905466665', 'straddle': 0, 'isBb': True, 'flopInsurance': [], 'turnInsurance': [], 'cards': '', 'stack': 196000.0, 'seat': 1, 'isButton': False, 'action': 'Fold', 'ante': 40000.0}], 
  'flop_ev': [7.722, -6.622, -1.1, 0.0, 0.0, 0.0], 'timestamp': 1715312776.240593, 'flop': '9cJs5h', 'heroIndex': 0, 
  'blindLevel': {'blinds': [2000.0, 4000.0, 40000.0], 'straddle': 1}, 'turn': '8s', 'reqid': 254975021, 'version': 1.0, 'command': 'aofhistory', 'handNumber': '102437994-78', 'winners': ['5253215520'], 'ev': [3.568, -2.468, -1.1, 0.0, 0.0, 0.0], 'outcome': [8.6, -7.5, -1.1, 0.0, 0.0, 0.0], 'turn_ev': [8.6, -7.5, -1.1, 0.0, 0.0, 0.0], 'leagueName': '熊猫联盟'}

'''





