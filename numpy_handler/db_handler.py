import logging
import json
import datetime
from utils import sign_blind_level, to_excel_numpy
import numpy as np

from db.db_loader import db_col


logger = logging.getLogger()


def init_query():
    # todo此处可以对处理数据进行进一步query筛选
    with db_col:
        result = db_col.run_query()
        numpy_data = []
        title = []
        dic = {'card_list': [], 'pid_list': [], 'hero_index': None,
               'flop_insurance': None, 'turn_insurance': None, 'leader_index': None,
               'card_leader': False, 'pid': None, 'card': None}
        print('文件总长度{}'.format(result.count()))
        for line in result:
            if not title:
                title = list(line.keys()) + ['card_num', 'card', 'ev_player', 'outcome_player', 'pid',
                                             'card_leader', 'ai_count', 'flop_insurance', 'turn_insurance']
                numpy_data.append(title)  # 将列放入数组中，处理时候可以无视
            row_data = []
            for i in line.keys():
                ai_count = 0
                if i == 'players':
                    players = line[i]
                    for p in range(len(players)):
                        player = players[p]
                        # 有牌处理 无牌
                        dic['card_list'].append(player.get('cards'))
                        dic['pid_list'].append(player.get('pId'))
                        flop_insurance = player.get('flopInsurance')
                        turn_insurance = player.get('turnInsurance')
                        if flop_insurance and flop_insurance[0].get('betStacks') > 0:
                            dic['flop_insurance'] = flop_insurance[0].get('betStacks')
                            dic['leader_index'] = int(p)
                        if turn_insurance and turn_insurance[0].get('betStacks') > 0:
                            dic['turn_insurance'] = turn_insurance[0].get('betStacks')
                            dic['leader_index'] = int(p)  # todo 如果需要排除异常数据在此处理
                if i == 'timestamp':
                    row_data.append(datetime.datetime.fromtimestamp(line.get(i)).strftime('%Y-%m-%d %H:%M:%S'))
                elif i == 'blindLevel':
                    row_data.append(sign_blind_level(line.get(i)['blinds']))
                elif isinstance(line.get(i), (str, int, float)):
                    row_data.append(line.get(i))
                else:
                    row_data.append('')
                if i == 'heroIndex':
                    dic['hero_index'] = line.get(i)
                    if line.get(i) != -1:
                        ai_count += 1
                        dic['card'] = dic['card_list'][line.get(i)]
                        dic['pid'] = dic['pid_list'][line.get(i)]
                        if line.get(i) == dic['leader_index']:
                            dic['card_leader'] = True
                elif i in ['ev', 'outcome']:
                    hero_index = dic.get('hero_index', '')
                    dic[i] = float(line.get(i)[hero_index]) if hero_index != -1 else ''
            card = dic.get('card')
            if card:
                a, b = max(card[0], card[2]), min(card[0], card[2])
                row_data.append('%s%s' % (a, b))
            else:
                row_data.append('')
            row_data += [card, dic['ev'], dic['outcome'], dic['pid'], dic['card_leader'], ai_count]
            if dic['card_leader']:
                row_data += [dic['turn_insurance'], dic['flop_insurance'], ]
            else:
                row_data += ['', '']
            yield row_data


class NumpyReadDb:

    def __init__(self):
        self.result_gen = init_query()
        self.title = next(self.result_gen)

    def add_result(self):
        nps = []
        while True:
            try:
                row = next(self.result_gen)
                nps.append(row)
            except StopIteration:
                print('已完成~')
                break
        self.write_excel(nps)

    def write_excel(self, nps, types='whole'):
        print('正在写入处理文件~')
        to_excel_numpy(nps, 'db', self.title)












