import pandas as pd
import os
import argparse

BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')


def run():
    parser = argparse.ArgumentParser(description='传递参数')
    parser.add_argument('--f-name', type=str, nargs='?', help='文件名称', default='')
    args = parser.parse_args()
    df = pd.read_csv(str(os.path.join(BASE, args.f_name)))
    av = df.iloc[1:, [4, 5]].var(axis=0, numeric_only=True)
    print(av)


if __name__ == '__main__':
    run()

