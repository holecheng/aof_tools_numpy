import collections
import requests


class ChiSquareCheck:
    __slots__ = ('group',
                 'group_key',  # 几人场
                 'matrix_dic',  # 排名矩阵
                 'total',
                 'row_dic'   # 数据字典
                 )

    def __init__(self, group, row_dic, total=None):
        self.group = group
        self.group_key = self.find_group_key(row_dic)
        self.total = total
        self.row_dic = row_dic
        self.matrix_dic = {'∑p0': collections.defaultdict(int), '∑x': collections.defaultdict(int)}
        self.covert(self.row_dic)

    def __eq__(self, other):
        group_key = self.find_group_key(other.row_dic)
        return self.group == other.group and self.group_key == group_key

    def __add__(self, other):
        row_dic = other.row_dic
        self.covert(row_dic)
        return self

    def covert(self, row_dic):
        if self.total:
            return self  # 去除total干扰
        showdown_ranks = row_dic.get('showdown_ranks')
        final_ranks = row_dic.get('final_ranks')
        if not showdown_ranks or not final_ranks:
            ans = self.run_update(row_dic)
            showdown_ranks, final_ranks = ans.get('showdown_ranks'), ans.get('final_ranks')
        ai_list = row_dic.get('ai_list')
        for rank in range(2, self.group_key):  # 至少2人场
            for i, v in enumerate(ai_list):
                if v == 1:  # 判断是不是AI
                    final_rank = final_ranks[i]
                    showdown_rank = showdown_ranks[i]
                    for k, p in enumerate(showdown_rank):
                        if p == 0:
                            continue
                        p0 = p / sum(showdown_rank)
                        self.matrix_dic[k]['∑p0'] += p0
                        if final_rank[k]:
                            self.matrix_dic[k]['∑x'] += 1

    @staticmethod
    def find_group_key(row_dic):
        return int(row_dic.get('ai_count') + row_dic.get('player_count'))

    def run_update(self, row_dic):
        url = 'https://aof-tools-tdse67xzfa-de.a.run.app/api/simulate_results'
        # url = 'http://10.140.0.15:52222/api/simulate_results'
        data_key = ['command', 'players', 'flop', 'turn', 'river', 'blindLevel']
        print({k: row_dic.get(k) for k in data_key})
        ans = self.fetch_url(url, {k: row_dic.get(k) for k in data_key}, row_dic)
        return ans

    def fetch_url(self, url, data, row):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "python-requests/2.20.1",
            "Content-Type": "application/json",
        }
        ans = requests.post(url=url, json=data, headers=headers)
        return ans.json()





