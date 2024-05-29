import os
import asyncio
import json
import datetime
import numpy as np
import pandas as pd
from handler import TimeStrategy
from utils import sign_blind_level


class NumpyReadFile:

    def __init__(self, out_files):
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        self.tasks = []
        self.out_files = out_files
        self.whole_list = []
        self.get_whole_file()
        self.results = None
        self.result = None
        self.results = loop.run_until_complete(asyncio.gather(*self.tasks))

    def get_whole_file(self):
        if os.path.exists(self.out_files):
            for root, dirs, files in os.walk(self.out_files):
                for file in files:
                    if file.startswith('aof'):
                        self.whole_list.append(os.path.join(root, file))
                    else:
                        print('无效文件{}'.format(files))
        else:
            print('{}不是有效文件'.format(self.out_files))
        self.run_asyncio_numpy_read_file()

    def run_asyncio_numpy_read_file(self):
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [read_numpy(df_path) for df_path in self.whole_list]
        self.results = loop.run_until_complete(asyncio.gather(*tasks))
        self.result = self.generate_result()

    def apply_handler(self):
        if self.results is not None:
            self.handler_to_strategy_apply(TimeStrategy)

    def generate_result(self):
        if self.results is not None:
            for i in range(len(self.results)):
                result = self.results[i]
                df_path = self.whole_list[i]
                if not result:
                    print('{}: 该文件没有返回值'.format(df_path))
                    continue
                yield result, df_path

    def handler_to_strategy_apply(self, strategy):
        pass

    async def write_numpy(self, result, df_path):
        ans_data = result[1:]
        await self.to_excel_numpy(ans_data, df_path, result[0])

    async def to_excel_numpy(self, nps, df_path, title, suffix='all'):
        df = pd.DataFrame(nps)
        df.columns = title
        self.tasks.append(df.to_excel('./output/' + os.path.basename(df_path).split('.')[0] + '_'
                                      + suffix + '.xlsx', sheet_name='data', index=False))


async def read_numpy(file_path: str) -> np.ndarray:
    numpy_data = []
    title = []
    dic = {'card_list': [], 'pid_list': [], 'hero_index': None,
           'flop_insurance': None, 'turn_insurance': None, 'leader_index': None,
           'card_leader': False, 'pid': None, 'card': None}
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as json_file:
            for line in json_file:
                line = json.loads(line)
                if not title:
                    title = list(line.keys()) + ['card_num', 'card', 'ev_player', 'outcome_player', 'pid',
                                                 'card_leader', 'ai_count', 'flop_insurance', 'turn_insurance']
                    numpy_data.append(title)  # 将列放入数组中，处理时候可以无视
                row_data = []
                for i in list(line.keys()):
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
                numpy_data.append(row_data)
            np_data = np.array(numpy_data)
            return np_data


