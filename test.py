import collections
import json

cnt = 1230

vid = 100
cnt_s = 20

def get_key(i):
    c, d = divmod(i, vid)
    if d < cnt_s:
        return f'{c}{0}'
    else:
        return f'{c}-{d // cnt_s}', f'{c}-{d // cnt_s + 1}'


dic = collections.defaultdict(list)
for i in range(cnt):
    dic[get_key(i)].append(i)

print(dic)


print(json.dumps(
    {'river': '2h', 'nash_range': [0.991, 0.674, 0.481, 0.0, 0.0, 0.0], 'players': [{'isSb': False, 'playerId': '莫欺少年有媳', 'pId': '6214406001', 'straddle': 0, 'isBb': False, 'flopInsurance': [], 'turnInsurance': [], 'cards': '3sAc', 'stack': 39995.0, 'seat': 3, 'isButton': True, 'action': 'Push', 'ante': 39995.0}, {'isSb': True, 'playerId': '一缕暖光\r\na', 'pId': '5585748659', 'straddle': 0, 'isBb': False, 'flopInsurance': [], 'turnInsurance': [{'betStacks': 0.0, 'defaultPot': False, 'potId': '356000'}, {'betStacks': 2299.0, 'defaultPot': True, 'potId': '39995'}], 'cards': '6sQd', 'stack': 356000.0, 'seat': 6, 'isButton': False, 'action': 'Push', 'ante': 40000.0}, {'isSb': False, 'playerId': '工会流弊', 'pId': '4473426006', 'straddle': 0, 'isBb': True, 'flopInsurance': [{'betStacks': 0.0, 'defaultPot': False, 'potId': '356000'}, {'betStacks': 0.0, 'defaultPot': True, 'potId': '39995'}], 'turnInsurance': [], 'cards': 'Ad4c', 'stack': 844006.0, 'seat': 1, 'isButton': False, 'action': 'Push', 'ante': 40000.0}], 'flop_ev': [0.098, -4.314, 4.216, 0.0, 0.0, 0.0], 'timestamp': 1710136830.75845, 'flop': '9d2d5s', 'heroIndex': 1, 'blindLevel': {'blinds': [2000.0, 4000.0, 40000.0], 'straddle': 1}, 'turn': 'Qh', 'reqid': 975101637, 'version': 1.0, 'command': 'aofhistory', 'handNumber': '101218315-6', 'winners': ['5585748659', '4473426006'], 'ev': [-0.19, -0.663, 0.853, 0.0, 0.0, 0.0], 'outcome': [-1.0, 9.9, -8.9, 0.0, 0.0, 0.0], 'turn_ev': [-0.714, 7.448, -6.733, 0.0, 0.0, 0.0], 'leagueName': '熊猫联盟', 'pid_case': '"{\\"case_num\\":1370754,\\"showdown_ranks\\":[[545474,646290,178990],[582318,65901,722535],[596872,636691,137191]],\\"final_ranks\\":[[0,1,0],[0,0,1],[1,0,0]]}"'}
))



