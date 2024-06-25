import pandas as pd
import os
import argparse

BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')


def run():
    parser = argparse.ArgumentParser(description='传递参数')
    parser.add_argument('--f-name', type=str, nargs='?', help='文件名称', default='')
    args = parser.parse_args()
    df = pd.read_csv(str(os.path.join(BASE, args.f_name)))
    total = df[df['group_key'] == 'total'].loc[:, ['avg_ev_player', 'avg_outcome_player']]
    df = df[df['group_key'] != 'total']
    df = df.drop(columns=['diff_ev_outcome', 'sum_outcome_player', 'sum_ev_player', 'total'], axis=1)
    df.index = [i for i in range(df.shape[0])]
    av = df.loc[:, ['avg_ev_player', 'avg_outcome_player']]
    dc = []
    for i, r in av.iterrows():
        dc.append([round((r.avg_ev_player - total.avg_ev_player[1]) ** 2, 8),
                   round((r.avg_outcome_player - total.avg_outcome_player[1]) ** 2, 8)])
    dc = pd.DataFrame(dc)
    dc.columns = ['var_ev_player', 'var_outcome_player']
    ans = pd.concat([dc, df], axis=1)
    ans = pd.concat([ans, total], axis=0)
    ans.to_csv('write_csv/{}'.format(args.f_name))


if __name__ == '__main__':
    run()

