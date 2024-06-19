import logging
import datetime
import os.path
import time

from group.blinds_group import Blinds
from group.chi_square import ChiSquareCheck
from group.hand_group import Hand

from util_lib.assert_effective import RowHand
# from handler import get_analysis, AvgStrategy
from utils import sign_blind_level, to_excel_numpy, get_group_avg_nps, get_chi_square_value
from config_parse import config

from db.db_loader import db_col

logger = logging.getLogger()

IS_DIGIT_KEY = ['stack', 'ev_player', 'outcome_player', 'flop_i', 'turn_i', 'player_count', 'is_push',
                'straddle', 'ante', 'winner', 'is_turn', 'is_flop', 'is_leader_turn', 'is_leader_flop',
                'flop_ev', 'is_river', 'turn_ev', 'seat', 'ai_count', 'ai_stack', 'compare_stack',
                'compare_player']  # 可统计数据（数字类型）


def init_query():
    # todo此处可以对处理数据进行进一步query筛选
    f = open('all_detail.csv', 'a+', newline='\n')
    with db_col:
        pid_set = db_col.pid_set
        result = db_col.run_query()
        row_key = []
        query_round = set()  # 用于统计是否该局号已被计入
        cnt = 0
        f.write('pId,handNumber,ev,outcome,timestamp\n')
        count = 0
        sum_ev = 0
        sum_outcome = 0
        for i in result:
            print(i)
            # if str(i.get('handNumber')) == '101652141-60':
            #     print(i)
            is_success, _ = RowHand().convert(i)
            if not is_success:
                continue
            if i.get('heroIndex') < 0:
                continue
            line_key = ['handNumber', 'river', 'heroIndex', 'reqid', 'leagueName', 'date', 'hours']
            player_key = ['pId', 'card_num', 'action', 'cards', 'blind_l',  'pid_case',
                          'ai_list', 'players', 'flop', 'turn', 'blindLevel']
            if not row_key:
                row_key = line_key + player_key + IS_DIGIT_KEY
                yield row_key
            line = i.copy()
            hand_num = line.get('handNumber')
            players = line.get('players')
            ai_list = [1 if i.get('pId') in pid_set else 0 for i in players]
            ai_count = sum(ai_list)
            player_count = len(players) - ai_count
            if not player_count:
                continue  # 表演赛不计入统计
            if hand_num in query_round:
                continue
            else:
                query_round.add(hand_num)
            if not i.get('pid_case'):
                db_col.run_update(i)  # 避免数据未更新
            compare_player = ai_count / player_count
            ante = line.get('blindLevel')['blinds'][-1]
            ai_stack = sum([float(i.get('stack') / ante) for i in filter(
                lambda x: x.get('pId') in pid_set, players)])
            if sum([int(i.get('stack')) / ante for i in players]) == ai_stack:
                compare_stack = 0
                cnt += 1
                print('存在异常的数据,第{}个'.format(cnt))
            else:
                compare_stack = ai_stack / (sum([int(i.get('stack')) / ante for i in players]) - ai_stack)
            for hero_index, player in enumerate(players):
                if config.get_args('player') and str(config.get_args('player')) != player.get('pId'):
                    continue
                p_id = player.get('pId')
                if not p_id or p_id not in pid_set:
                    continue  # 非AI玩家暂不分析
                row_dic = {}
                row_dic.update({i: line.get(i) for i in row_key})
                dates = datetime.datetime.fromtimestamp(i.get('timestamp')).strftime(
                    '%Y-%m-%d')
                count += 1
                sum_ev += i.get('ev')[hero_index]
                sum_outcome += i.get('outcome')[hero_index]
                f.write(f"{player.get('pId')},{i.get('handNumber')},"
                        f"{i.get('ev')[hero_index]},{i.get('outcome')[hero_index]},"
                        f"{dates}\n")
                row_dic['ai_count'] = ai_count
                row_dic['ai_list'] = ai_list
                row_dic['player_count'] = player_count
                row_dic['compare_player'] = compare_player
                row_dic['ai_stack'] = ai_stack
                row_dic['compare_stack'] = compare_stack
                outcome = line.get('outcome')[hero_index]
                ev = line.get('ev')[hero_index]
                flop_ev_list = line.get('flop_ev')
                turn_ev_list = line.get('turn_ev')
                winners = line.get('winners')
                row_dic['date'], row_dic['hours'] = datetime.datetime.fromtimestamp(line.get('timestamp')).strftime(
                    '%Y-%m-%d %H').split(' ')
                row_dic['is_turn'] = '1' if line.get('turn') else ''  # 是否turn
                row_dic['is_river'] = '1' if line.get('river') else ''  # 是否存在river
                row_dic['stack'] = int(player.get('stack')) // ante
                row_dic['blind_l'] = sign_blind_level(line.get('blindLevel')['blinds'])
                if not (line.get('heroIndex') is None):
                    row_dic['heroIndex'] = hero_index
                if flop_ev_list and turn_ev_list:
                    row_dic['flop_ev'] = flop_ev_list[hero_index]
                    row_dic['turn_ev'] = turn_ev_list[hero_index]
                else:
                    row_dic['flop_ev'] = row_dic['turn_ev'] = ''
                row_dic.update({'outcome_player': outcome, 'ev_player': ev})
                row_dic['is_push'] = '1' if player['action'] == 'Push' else ''
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
                row_dic['is_leader_flop'] = '1' if flop_insurance else ''
                row_dic['is_leader_turn'] = '1' if turn_insurance else ''
                player['flop_i'] = flop_insurance[0].get('betStacks', '0') if flop_insurance else ''
                player['turn_i'] = turn_insurance[0].get('betStacks', '0') if turn_insurance else ''
                row_dic.update({i: player.get(i) if not row_dic.get(i) else row_dic.get(i) for i in row_key})
                row_dic.update({i: float(row_dic.get(i) if row_dic.get(i) else 0) for i in IS_DIGIT_KEY})
                yield {key: row_dic.get(key, '') for key in row_key}
    if count:
        f.write((f"count,{count},sum_ev:,{sum_ev},sum_outcome:,"
                 f"{sum_outcome},avg_ev:,{sum_ev / count},avg_outcome:,{sum_outcome / count},"))
    f.write(f'处理完成总计{cnt}')
    f.close()


class NumpyReadDb:

    def __init__(self):
        s = time.time()
        if config.get_args('aof'):
            self.write_origin()
        else:
            self.result_gen = init_query()
            self.title = next(self.result_gen)
            if config.get_args('simple'):
                self.title = ['group', 'group_key', 'allowance', 'avg_ev', 'avg_flop_ev',
                              'avg_turn_ev', 'avg_outcome', 'diff_ev_outcome', 'counts']
            self.format_list = [Hand, Blinds, ChiSquareCheck]
            self.group_dic = {}
            self.group = config.get_args('group')
            self.f = None
            file_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db_file', )
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
            elif self.group in ['chi_square']:
                self.get_row_result(2)
            else:
                self.get_row_result(1)
        print((time.time() - s))
        print('总共用时{}分'.format((time.time() - s) // 60))
        # self.add_result()

    def get_row_result(self, index):
        cnt = 0
        data_format = self.format_list[index]
        while True:
            row_dic = self.get_generator()
            if not row_dic:
                break
            if config.get_args('group'):
                self.apply_blinds_id(row_dic, data_format)
            if config.get_args('all'):
                self.write_to_all_excel(row_dic)
            if config.get_args('hand_detail'):
                self.write_to_hand_detail_excel(row_dic)
            cnt += 1
            if cnt and cnt % 10000 == 0:
                print('已处理数据{} * 10000'.format(cnt // 10000))
        print('数据处理完成, 总计 {}'.format(cnt))
        if self.f:
            self.f.close()
        title = list(data_format.__slots__)
        title.remove('row_dic')
        ans = [title]
        for k, v in self.group_dic.items():
            if self.group != 'chi_square':
                ans.append([round(getattr(v, i), 5) if isinstance(getattr(v, i), float)
                            else getattr(v, i) for i in title])
            else:
                matrix_dic = v.matrix_dic  # 卡方集合
                free_d = k - 1  # 自由度K-1
                avg_ev_player = v.avg_ev_player
                avg_outcome_player = v.avg_outcome_player
                diff_ev_outcome = v.diff_ev_outcome
                counts = v.counts
                chi_square_value = get_chi_square_value(matrix_dic)  # 卡方值
                print(f'{k}人场： 卡方值为{chi_square_value}, 自由度为{free_d}')
                ans.append(['chi_square', k, chi_square_value, avg_ev_player,
                            avg_outcome_player, diff_ev_outcome, free_d, counts])

        if self.group:
            self.write_excel(ans, config.get_args('query_time') + self.group.replace('**', ''))
        return

    def apply_blinds_id(self, row_dic, data_format):
        groups = data_format(self.group, row_dic)
        group_key = groups.group_key
        if group_key not in self.group_dic:
            self.group_dic[group_key] = groups
        else:
            self.group_dic[group_key] += groups
        if self.group != 'chi_square':
            total = data_format(self.group, row_dic, total=1)
            if 'total' not in self.group_dic:
                self.group_dic['total'] = total
            else:
                self.group_dic['total'] += total

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

    @staticmethod
    def write_origin():
        with db_col:
            print('正在处理')
            ans = db_col.run_query()
            print('获取数据成功')
            unique = {}
            with open('4-01-4-30.csv', 'a+', newline='\n', encoding='utf-8') as f:
                f.write('pId,handNumber,ev,outcome,timestamp\n')
                count = 0
                sum_ev = 0
                sum_outcome = 0
                cnt = 0
                for i in ans:
                    hand = RowHand()
                    is_success, _ = hand.convert(i)
                    if not is_success:
                        continue
                    if hand.handno in unique:
                        continue
                    unique[hand.handno] = 1
                    players = i.get('players')
                    ai_count = sum(1 if i.get('pId') in db_col.pid_set else 0 for i in players)
                    if ai_count == len(players):
                        continue
                    cnt += 1
                    for k, v in enumerate(players):
                        if v.get('pId') in db_col.pid_set:
                            count += 1
                            sum_ev += i.get('ev')[k]
                            sum_outcome += i.get('outcome')[k]
                            dates = datetime.datetime.fromtimestamp(i.get('timestamp')).strftime(
                                '%Y-%m-%d')
                            f.write(f"{v.get('pId')},{i.get('handNumber')},"
                                    f"{i.get('ev')[k]},{i.get('outcome')[k]},"
                                    f"{dates}\n")
                f.write(f"count:,{count},sum_ev,{sum_ev},sum_outcome,"
                        f"{sum_outcome},avg_ev,{sum_ev / count},avg_outcome,{sum_outcome / count},")
                print((f"count,{count},sum_ev:,{sum_ev},sum_outcome:,"
                       f"{sum_outcome},avg_ev:,{sum_ev / count},avg_outcome:,{sum_outcome / count},"))
                print(f'处理完成总计{cnt}')
