'''


{'_id': ObjectId('660a0eed17188830a8dccbad'), 'river': 'Th', 'nash_range': [0.689, 0.472, 0.342, 0.0, 0.0, 0.0], 'players': [{'isSb': False, 'playerId': '我想找个对象了.', 'pId': '5797501911', 'straddle': 0, 'isBb': False, 'flopInsurance': [], 'turnInsurance': [], 'cards': 'Kh3s', 'stack': 137000.0, 'seat': 1, 'isButton': True, 'action': 'Push', 'ante': 20000.0}, {'isSb': True, 'playerId': '梦之蓝1', 'pId': '9567280874', 'straddle': 0, 'isBb': False, 'flopInsurance': [{'betStacks': 0.0, 'defaultPot': False, 'potId': '200000'}], 'turnInsurance': [{'betStacks': 0.0, 'defaultPot': False, 'potId': '200000'}], 'cards': '6sKc', 'stack': 200000.0, 'seat': 2, 'isButton': False, 'action': 'Push', 'ante': 20000.0}, {'isSb': False, 'playerId': '最熟悉的陌生伦', 'pId': '6095018817', 'straddle': 0, 'isBb': True, 'flopInsurance': [], 'turnInsurance': [], 'cards': 'Ts8s', 'stack': 683000.0, 'seat': 4, 'isButton': False, 'action': 'Push', 'ante': 20000.0}], 'flop_ev': [-2.64, -1.524, 4.164, 0.0, 0.0, 0.0], 'timestamp': 1711935213.239057, 'flop': 'AcJh9d', 'heroIndex': 2, 'blindLevel': {'blinds': [1000.0, 2000.0, 20000.0], 'straddle': 1}, 'turn': '5h', 'reqid': 156031767, 'version': 1.0, 'command': 'aofhistory', 'handNumber': '101652141-60', 'winners': ['6095018817'], 'ev': [-2.533, -0.466, 2.999, 0.0, 0.0, 0.0], 'outcome': [-6.85, -10.0, 16.85, 0.0, 0.0, 0.0], 'turn_ev': [-1.957, 3.007, -1.05, 0.0, 0.0, 0.0], 'leagueName': '熊猫联盟', 'pid_case': '{"case_num":1370754,"showdown_ranks":[[393644,671743,305367],[535411,683493,151850],[659309,71765,639680]],"final_ranks":[[0,1,0],[1,0,0],[0,0,1]]}'}


'''
import json

print(json.dumps(
{'river': None, 'nash_range': [0.253, 1.0, 0.0, 0.0, 0.0, 0.0], 'players': [{'isSb': True, 'playerId': '怙棘\r\nS', 'pId': '5055205826', 'straddle': 0, 'isBb': False, 'flopInsurance': [], 'turnInsurance': [], 'cards': '', 'stack': 100000.0, 'seat': 3, 'isButton': True, 'action': 'Fold', 'ante': 10000.0}, {'isSb': False, 'playerId': '上帝的士兵', 'pId': '8410922871', 'straddle': 0, 'isBb': True, 'flopInsurance': [], 'turnInsurance': [], 'cards': '', 'stack': 398482.0, 'seat': 6, 'isButton': False, 'action': 'Push', 'ante': 10000.0}], 'timestamp': 1712331672.066345, 'flop': '', 'heroIndex': -1, 'blindLevel': {'blinds': [500.0, 1000.0, 10000.0], 'straddle': 1}, 'turn': None, 'reqid': 648968394, 'version': 1.0, 'command': 'aofhistory', 'winners': ['8410922871'], 'ev': [-1.05, 1.05, 0.0, 0.0, 0.0, 0.0], 'outcome': [-1.05, 1.05, 0.0, 0.0, 0.0, 0.0], 'handNumber': '101748712-44', 'leagueName': '熊猫联盟'}

))