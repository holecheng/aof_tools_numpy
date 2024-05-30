import logging
import datetime
import time

from handler import get_analysis, AvgStrategy
from utils import sign_blind_level, to_excel_numpy, get_group_avg_nps
import numpy as np
from config_parse import config

from db.db_loader import db_col

logger = logging.getLogger()


def init_query():
    # todo此处可以对处理数据进行进一步query筛选
    with db_col:
        result = db_col.run_query()
        plyer_limit = config.get_args('player')
        flop_limit = config.get_args('flop')
        turn_limit = config.get_args('turn')
        row_key = []
        for i in result:
            line_key = ['handNumber', 'river', 'heroIndex', 'reqid', 'leagueName', 'pId', 'cards']
            player_key = ['pId', 'card_num', 'stack', 'seat', 'action']
            is_digit_value_key = ['stack', 'ev_player', 'outcome_player', 'flop_i', 'turn_i',
                                  'straddle', 'ante', 'winner', 'is_seat', 'is_turn', 'is_flop']  # 可统计数据（数字类型）
            if not row_key:
                row_key = line_key + player_key + is_digit_value_key
                yield row_key
            line = i.copy()
            row_dic = {k: v for k, v in line.items() if k in line_key}
            row_dic.update(dict.fromkeys(player_key+is_digit_value_key))
            row_dic['timestamp'] = datetime.datetime.fromtimestamp(line.get('timestamp')).strftime('%Y-%m-%d %H:%M:%S')
            row_dic['blindLevel'] = sign_blind_level(line.get('blindLevel')['blinds'])
            hero_index = int(line.get('heroIndex'))
            row_dic['is_seat'] = 1 if hero_index == -1 else 0
            row_dic['is_turn'] = 1 if line.get('turn') else 0
            row_dic['is_flop'] = 1 if line.get('flop') else 0
            players = line.pop('players')
            outcome = int(line.pop('outcome')[hero_index]) if hero_index == -1 else np.nan
            ev = int(line.pop('ev')[hero_index]) if hero_index == -1 else np.nan
            row_dic.update({'outcome_player': outcome, 'ev_player': ev})
            if hero_index != -1:
                player = {k: v for k, v in players[hero_index].items() if k in player_key+is_digit_value_key}
                row_dic['is_push'] = 1 if row_dic['action'] == 'Push' else 0
                if plyer_limit == str(player.get('pId')):
                    continue
                winners = line.get('winners')
                if str(player.get('pId')) in winners:
                    row_dic['winner'] = 1
                else:
                    row_dic['winner'] = 0
                card = player.get('cards', '')
                if card:
                    a, b = max(card[0], card[2]), min(card[0], card[2])
                    player['card_num'] = '%s%s' % (a, b)
                else:
                    player['card_num'] = ''
                flop_insurance = players[hero_index].get('flopInsurance')
                turn_insurance = players[hero_index].get('turnInsurance')
                player['flop_i'] = flop_insurance[0].get('betStacks') if flop_insurance else ''
                player['turn_i'] = turn_insurance[0].get('betStacks') if turn_insurance else ''
                if flop_limit or turn_limit:
                    if flop_limit and int(flop_limit) < player['flop']:
                        continue
                    if turn_limit and int(turn_limit) < player['turn']:
                        continue
                row_dic.update(player)

            yield row_dic


class NumpyReadDb:

    def __init__(self):
        s = time.time()
        self.result_gen = init_query()
        self.title = next(self.result_gen)
        self.add_result()
        print(time.time() - s)

    def get_generator(self):
        try:
            gen_data = next(self.result_gen)
            return gen_data
        except StopIteration:
            print('数据处理已完成~')
            return False

    def add_result(self):
        page = 0
        final = 1
        while final:
            nps = [self.title]
            page_row = 10000
            while page_row:
                row_dic = self.get_generator()
                if row_dic:
                    page_row -= 1
                    nps.append([row_dic[i] for i in self.title])
                else:
                    final = 0
                    print('数据处理完毕！')
                    break
            else:
                page += 1
                self.write_excel(nps, str(page))
                npd = get_group_avg_nps(nps)
                np_apply = get_analysis(AvgStrategy(), npd)
                # self.write_excel(np_apply, str(page) + '_avg')
                print('已完成处理数据第{}页'.format(page))

    def write_excel(self, nps, page):
        print('正在写入处理文件~')
        to_excel_numpy(nps, 'db', self.title, page)
