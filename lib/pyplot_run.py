import argparse
import math

from matplotlib import pyplot as plt

import pandas as pd
import os

BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')


def run():
    parser = argparse.ArgumentParser(description='传递参数')
    parser.add_argument('--X', type=str, nargs='?', help='X轴', default='group_key')
    parser.add_argument('--Y', type=str, nargs='?', help='Y轴', default='avg_ev,avg_outcome')
    parser.add_argument('--f-name', type=str, nargs='?', help='文件名')
    parser.add_argument('--types', type=str, nargs='?', help='图形类型', default='plot')
    parser.add_argument('--count-min', type=int, nargs='?', help='最小场次', default=0)
    args = parser.parse_args()
    df = pd.read_csv(str(os.path.join(BASE, args.f_name)))
    total = df[df[args.X] == 'total']
    df = df[df[args.X] != 'total']
    if args.count_min:
        df = df[df['counts'] >= args.count_min]
    df[args.X] = df[args.X].astype(int)
    df = df.sort_values(by=args.X)
    color = ['r', 'b', 'c', 'g', 'k', 'm', 'y']
    y_list = args.Y.strip().split(',')
    if args.types == 'plot':
        for col in y_list:
            if color:
                c = color.pop()
            else:
                c = 'k'
            plt.plot(df[args.X], df[col], marker='o', color=c, linestyle='--', linewidth=2, markersize=8)
        plt.legend()
        plt.grid(True)
    elif args.types == 'bar':
        sizes = math.ceil(len(args.Y.strip().split(',')))
        fig_s = (12, 8)
        fig = plt.figure(figsize=fig_s)
        plot_gen = gen_fig_plot(fig, sizes)
        for col in y_list:
            a1 = next(plot_gen)
            a1.bar(df[args.X], df[col], label=col)
        autolabel(plot_gen)
    plt.title('%s && %s' % (args.X, args.Y))
    plt.xlabel('%s(%s)' % (total.loc[1, 'group'], total.loc[1, 'allowance']))
    plt.ylabel('avg')
    # 设置字体为宋体
    plt.rcParams['font.family'] = ['serif']  # 设置字体为有衬线字体（宋体是有衬线字体之一）
    plt.rcParams['font.serif'] = ['SimSun']  # 设置有衬线字体为宋体
    ## 下面的是设置字体为黑体
    # plt.rcParams['font.family'] = ['sans-serif'] # 设置字体为无衬线字体（黑体是无衬线字体之一）
    # plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置无衬线字体为黑体

    # 设置公式格式
    plt.rcParams['mathtext.fontset'] = 'stix'

    # 正常显示负号
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 18  # 设 置字体字号
    plt.rcParams['xtick.labelsize'] = 16  # 设置横坐标轴字体字号
    plt.rcParams['ytick.labelsize'] = 16  # 设置纵坐标轴字体字号

    # 设置刻度朝里，我喜欢朝里，默认的朝外感觉有点丑
    plt.tick_params(which="major", direction='in', length=5, bottom=True, left=True)
    plt.show()


def gen_fig_plot(fig, sizes):
    ans = [1, 1, 0]
    for i in range(1, sizes + 1):
        if ans != sizes:
            ans[2] += 1
            yield fig.add_subplot(*ans)
        else:
            ans[2] = 1
            if ans[1] != sizes:
                ans[1] += 1
            else:
                ans[1] = 1
                ans[0] += 1
            yield fig.add_subplot(*ans)


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2. - 0.2, 1.03 * height, '%s' % float(height))


if __name__ == '__main__':
    run()
