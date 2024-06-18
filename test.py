import json

print(json.dumps(
{'command': 'aofhistory', 'players': [{'isSb': False, 'playerId': 'Q666810', 'pId': '5797668491', 'straddle': 0, 'isBb': False, 'flopInsurance': [], 'turnInsurance': [], 'cards': '3h9d', 'stack': 200000.0, 'seat': 3, 'isButton': True, 'action': 'Fold', 'ante': 20000.0}, {'isSb': True, 'playerId': '一路不逆风', 'pId': '5196571989', 'straddle': 0, 'isBb': False, 'flopInsurance': [], 'turnInsurance': [], 'cards': '', 'stack': 178000.0, 'seat': 6, 'isButton': False, 'action': 'Push', 'ante': 20000.0}, {'isSb': False, 'playerId': '梦之蓝1', 'pId': '9567280874', 'straddle': 0, 'isBb': True, 'flopInsurance': [], 'turnInsurance': [], 'cards': '', 'stack': 306380.0, 'seat': 2, 'isButton': False, 'action': 'Fold', 'ante': 20000.0}], 'flop': '', 'turn': None, 'river': None, 'blindLevel': {'blinds': [1000.0, 2000.0, 20000.0], 'straddle': 1}}


))







a = {'0': {'0': 1, '1':2}, '1':{'0': 3, '1':2}}
for _, v in a.items():
    keys = ['0', '1']
    x, y = (v.get(i) for i in keys)
    print(x, y)
