import collections
import logging
import datetime
import os.path
import time

from group.blinds import Blinds
from group.hand import Hand
from collections import defaultdict
# from handler import get_analysis, AvgStrategy
from utils import sign_blind_level, to_excel_numpy, get_group_avg_nps
from config_parse import config

from db.db_loader import db_col

logger = logging.getLogger()

IS_DIGIT_KEY = ['stack', 'ev_player', 'outcome_player', 'flop_i', 'turn_i', 'player_count',
                'straddle', 'ante', 'winner', 'is_turn', 'is_flop', 'is_leader', 'flop_ev',
                'turn_ev']  # 可统计数据（数字类型）


def init_query():
    # todo此处可以对处理数据进行进一步query筛选
    with db_col:
        pid_set = db_col.run_pid_set()
        result = db_col.run_query()
        row_key = []
        query_round = set()  # 用于统计是否该局号已被计入
        for i in result:
            line_key = ['handNumber', 'river', 'heroIndex', 'reqid', 'leagueName']
            player_key = ['pId', 'card_num', 'action', 'cards']
            if not row_key:
                row_key = line_key + player_key + IS_DIGIT_KEY
                yield row_key
            line = i.copy()
            hand_num = line.get('handNumber')
            if hand_num in query_round:
                continue
            else:
                query_round.add(hand_num)
            players = line.pop('players')
            ai_count = sum(1 if i.get('pId') in pid_set else 0 for i in players)
            player_count = len(players)
            if ai_count == player_count:
                continue  # 表演赛不计入统计
            for hero_index, player in enumerate(players):
                row_dic = collections.defaultdict(str)
                p_id = player.get('pId')
                if not p_id or p_id not in pid_set:
                    continue  # 非AI玩家暂不分析
                row_dic.update({i: line.get(i) for i in row_key})
                outcome = line.pop('outcome')[hero_index]
                ev = line.pop('ev')[hero_index]
                flop_ev_list = line.get('flop_ev')
                turn_ev_list = line.get('turn_ev')
                if flop_ev_list and turn_ev_list:
                    row_dic['flop_ev'] = line.pop('flop_ev')[hero_index]
                    row_dic['turn_ev'] = line.pop('turn_ev')[hero_index]
                else:
                    row_dic['flop_ev'] = row_dic['turn_ev'] = ''
                row_dic.update({'outcome_player': outcome, 'ev_player': ev})
                row_dic['is_push'] = '1' if player['action'] == 'Push' else ''
                winners = line.get('winners')
                if winners and str(player.get('pId', '')) in winners:
                    row_dic['winner'] = '1'
                else:
                    row_dic['winner'] = '0'
                card = player.get('cards', '')
                if card:
                    a, b = max(card[0], card[2]), min(card[0], card[2])
                    player['card_num'] = '%s%s' % (a, b)
                else:
                    player['card_num'] = ''
                flop_insurance = players[hero_index].get('flopInsurance')
                turn_insurance = players[hero_index].get('turnInsurance')
                row_dic['is_leader'] = '1' if flop_insurance or turn_insurance else ''
                player['flop_i'] = flop_insurance[0].get('betStacks', '0') if flop_insurance else ''
                player['turn_i'] = turn_insurance[0].get('betStacks', '0') if turn_insurance else ''
                row_dic.update({i: player.get(i) if not row_dic.get(i) else row_dic.get(i) for i in row_key})
                row_dic['timestamp'] = datetime.datetime.fromtimestamp(line.get('timestamp')).strftime(
                    '%Y-%m-%d %H:%M:%S')
                row_dic['blindLevel'] = sign_blind_level(line.get('blindLevel')['blinds'])
                row_dic['is_turn'] = '1' if line.get('turn') else ''  # 是否turn
                row_dic['is_river'] = '1' if line.get('river') else ''  # 是否存在river
                row_dic.update({i: float(row_dic.get(i) if row_dic.get(i) else 0) for i in IS_DIGIT_KEY})
                new_row = {key: row_dic.get(key, '') for key in row_key}
                yield new_row


class NumpyReadDb:

    def __init__(self):
        s = time.time()
        self.result_gen = init_query()
        self.title = next(self.result_gen)
        self.format_list = [Blinds, Hand]
        self.group_dic = {}
        self.group = config.get_args('group')
        file_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db_file',)
        if config.get_args('all'):
            file_path = os.path.join(file_dir, config.get_args('query_time') + 'all.csv')
            self.f = open(file_path, 'a+', encoding='utf-8')
            if os.path.exists(file_path):
                self.f.truncate(0)
            self.f.write(','.join(self.title) + '\n')
        if config.get_args('hand_detail'):
            file_path = os.path.join(file_dir, config.get_args('query_time') + 'hand_detail.csv')
            self.f = open(file_path, 'a+', encoding='utf-8')
            if os.path.exists(file_path):
                self.f.truncate(0)
            self.f.write(','.join(self.title) + '\n')
        if self.group in ['card_num', 'pId']:
            self.get_row_result(0)
        if self.group == 'blindLevel':
            self.get_row_result(1)
        print('总共用时{}分'.format((time.time() - s) // 60000))
        # self.add_result()

    def get_row_result(self, index):
        cnt = 0
        data_format = self.format_list[index]
        # try:
        while True:
            row_dic = self.get_generator()
            self.apply_blinds_id(row_dic, data_format)
            if config.get_args('all'):
                self.write_to_all_excel(row_dic)
            if config.get_args('hand_detail'):
                self.write_to_hand_detail_excel(row_dic)
            cnt += 1
            if cnt and cnt % 10000 == 0:
                print('已处理数据{} * 10000'.format(cnt // 10000))
        # except Exception as e:
        #     print(e)
        #     print('数据处理完成, 总计 {}'.format(cnt))
        #     if self.f:
        #         self.f.close()
        #     title = list(data_format.__slots__)
        #     title.remove('row_dic')
        #     ans = [title]
        #     for _, v in self.group_dic.items():
        #         ans.append([round(getattr(v, i), 5) if isinstance(getattr(v, i), float)
        #                     else getattr(v, i) for i in title])
        #     self.write_excel(ans, config.get_args('query_time') + self.group)
        #     return

    def apply_blinds_id(self, row_dic, data_format):
        print(row_dic)
        group = row_dic[self.group]
        groups = data_format(self.group, group, row_dic)
        group_key = groups.group_key
        if group_key not in self.group_dic:
            self.group_dic[group_key] = groups
        else:
            self.group_dic[group_key] += groups

    def get_generator(self):
        try:
            gen_data = next(self.result_gen)
            return gen_data
        except StopIteration:
            print('数据处理已完成~')
            return False

    @staticmethod
    def write_excel(nps, page):
        print('正在写入处理文件~')
        to_excel_numpy(nps, 'db', page)

    def write_to_all_excel(self, row_dic):
        row = [str(row_dic[k]) for k in self.title]
        self.f.write(','.join(row) + '\n')

    def write_to_hand_detail_excel(self, row_dic):
        row = [str(row_dic[k]) for k in ['pId', 'handNumber']]
        self.f.write(','.join(row) + '\n')

    # def add_result(self):
    #     page = 0
    #     final = 1
    #     np_apply = []
    #     while final:
    #         nps = [self.title]
    #         page_row = 10000
    #         while page_row:
    #             row_dic = self.get_generator()
    #             if row_dic:
    #                 page_row -= 1
    #                 nps.append([row_dic[i] for i in self.title])
    #             else:
    #                 final = 0
    #                 print('数据处理完毕！')
    #                 break
    #         else:
    #             page += 1
    #             # self.write_excel(nps, str(page))
    #             npd = get_group_avg_nps(nps)
    #             np_apply.append(get_analysis(AvgStrategy(), npd))
    #             print('已完成处理数据第{}页'.format(page))
    #             if len(np_apply) > 30:
    #                 title = np_apply[0]
    #                 nps = np.vstack([title]+[c[1:,] for c in np_apply])
    #                 new_npd = get_group_avg_nps(nps)
    #                 np_apply.append(new_npd)
    #             # self.write_excel(np_apply, str(page) + '_{}'.format(config.get_args('types')))

