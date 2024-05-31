import collections
import logging
import datetime
import time

from group.hand import Hand
from handler import get_analysis, AvgStrategy
from utils import sign_blind_level, to_excel_numpy, get_group_avg_nps
import numpy as np
from config_parse import config

from db.db_loader import db_col

logger = logging.getLogger()

IS_DIGIT_KEY = ['stack', 'ev_player', 'outcome_player', 'flop_i', 'turn_i', 'ai_count', 'player_count',
                'straddle', 'ante', 'winner', 'is_seat', 'is_turn', 'is_flop', 'is_leader', 'flop_ev', 'turn_ev']  # 可统计数据（数字类型）


def init_query():
    # todo此处可以对处理数据进行进一步query筛选
    with db_col:
        pid_set = db_col.run_pid_set()
        result = db_col.run_query()
        plyer_limit = config.get_args('player')
        flop_limit = config.get_args('flop')
        turn_limit = config.get_args('turn')
        row_key = []
        cnt = 0
        for i in result:
            if cnt == 3:
                print(i)
            else:
                cnt += 1
            line_key = ['handNumber', 'river', 'heroIndex', 'reqid', 'leagueName']
            player_key = ['pId', 'card_num', 'stack', 'seat', 'action', 'cards']
            if not row_key:
                row_key = line_key + player_key + IS_DIGIT_KEY
                yield row_key
            line = i.copy()
            hero_index = int(line.get('heroIndex', -1))
            row_dic = {k: v for k, v in line.items() if k in line_key}
            wait_update_list = player_key + IS_DIGIT_KEY
            row_dic.update(dict.fromkeys(wait_update_list, ''))
            row_dic['timestamp'] = datetime.datetime.fromtimestamp(line.get('timestamp')).strftime('%Y-%m-%d %H:%M:%S')
            row_dic['blindLevel'] = sign_blind_level(line.get('blindLevel')['blinds'])
            row_dic['is_seat'] = 1 if hero_index != -1 else 0
            row_dic['is_turn'] = 1 if line.get('turn') else 0  # 是否turn
            row_dic['is_river'] = 1 if line.get('river') else 0  # 是否存在river
            players = line.pop('players')
            outcome = float(line.pop('outcome')[hero_index]) if hero_index != -1 else 0
            ev = float(line.pop('ev')[hero_index]) if hero_index != -1 else 0
            row_dic.update({'outcome_player': outcome, 'ev_player': ev})
            if hero_index != -1:
                player = {k: v for k, v in players[hero_index].items() if k in wait_update_list}
                player_id = player.get('pId', '')
                if plyer_limit == player_id:
                    continue
                row_dic['ai_count'] = sum(1 if i.get('pId') in pid_set else 0 for i in players)
                row_dic['player_count'] = len(players)
                row_dic['is_push'] = 1 if player['action'] == 'Push' else 0
                winners = line.get('winners')
                if winners and str(player.get('pId', '')) in winners:
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
                row_dic['is_leader'] = 1 if flop_insurance or turn_insurance else 0
                player['flop_i'] = flop_insurance[0].get('betStacks', 0) if flop_insurance else 0
                player['turn_i'] = turn_insurance[0].get('betStacks', 0) if turn_insurance else 0
                if flop_limit or turn_limit:
                    if flop_limit and float(flop_limit) < player['flop_i']:
                        continue
                    if turn_limit and float(turn_limit) < player['turn_i']:
                        continue
                row_dic.update(player)

            yield row_dic


class NumpyReadDb:

    def __init__(self):
        s = time.time()
        self.result_gen = init_query()
        self.title = next(self.result_gen)
        self.hand_list = []
        self.hand_dic = {}
        group = config.get_args('group')
        if group in ['card_num', 'pId']:
            self.apply_player_id(group)
        elif group == 'blindLevel':
            self.apply_blinds_id(group)
        print('总共用时{}分'.format((time.time() - s) // 60000))
        # self.add_result()

    def apply_blinds_id(self, group):
        cnt = 0
        try:
            while True:
                row_dic = self.get_generator()
                blind_level = row_dic['blindLevel']
                if not blind_level:
                    continue
                if row_dic['ai_count'] == row_dic['player_count']:
                    continue
                cnt += 1
                hand = Hand(group, blind_level, row_dic)
                if blind_level not in self.hand_dic:
                    self.hand_dic[blind_level] = hand
                else:
                    self.hand_dic[blind_level] += hand
                if cnt and cnt % 10000 == 0:
                    print('已处理数据{} * 10000'.format(cnt // 10000))
        except Exception:
            print('数据处理完成, 总计 {}'.format(cnt))
            title = list(Hand.__slots__)
            title.remove('row_dic')
            np_ans = np.array(title)
            for _, v in self.hand_dic.items():
                np_ans = np.vstack((np_ans, np.array([getattr(v, i) for i in title])))
            self.write_excel(np_ans, config.get_args('query_time') + group)

    def get_generator(self):
        try:
            gen_data = next(self.result_gen)
            return gen_data
        except StopIteration:
            print('数据处理已完成~')
            return False

    def apply_player_id(self, group):
        cnt = 0
        try:
            while True:
                row_dic = self.get_generator()
                player_id = row_dic[group]
                if not player_id:
                    continue
                if row_dic['ai_count'] == row_dic['player_count']:
                    continue
                cnt += 1
                hand = Hand(group, player_id, row_dic)
                if player_id not in self.hand_dic:
                    self.hand_dic[player_id] = hand
                else:
                    self.hand_dic[player_id] += hand
                if cnt and cnt % 10000 == 0:
                    print('已处理数据{} * 10000'.format(cnt // 10000))
        except Exception:
            print('数据处理完成, 总计 {}'.format(cnt))
            title = list(Hand.__slots__)
            title.remove('row_dic')
            np_ans = np.array(title)
            for _, v in self.hand_dic.items():
                np_ans = np.vstack((np_ans,np.array([getattr(v, i) for i in title])))
            self.write_excel(np_ans, config.get_args('query_time') + group)

    def add_result(self):
        page = 0
        final = 1
        np_apply = []
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
                # self.write_excel(nps, str(page))
                npd = get_group_avg_nps(nps)
                np_apply.append(get_analysis(AvgStrategy(), npd))
                print('已完成处理数据第{}页'.format(page))
                if len(np_apply) > 30:
                    title = np_apply[0]
                    nps = np.vstack([title]+[c[1:,] for c in np_apply])
                    new_npd = get_group_avg_nps(nps)
                    np_apply.append(new_npd)
                # self.write_excel(np_apply, str(page) + '_{}'.format(config.get_args('types')))

    @staticmethod
    def write_excel(nps, page):
        print('正在写入处理文件~')
        to_excel_numpy(nps, 'db', page)
