import argparse
import math
import time

from matplotlib import pyplot as plt, ticker

import pandas as pd
import os

from matplotlib.ticker import MultipleLocator

BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')


def run():
    parser = argparse.ArgumentParser(description='传递参数')
    parser.add_argument('--X', type=str, nargs='?', help='X轴', default='group_key')
    parser.add_argument('--Y', type=str, nargs='?', help='Y轴', default='avg_ev_player,avg_outcome_player')
    parser.add_argument('--f-name', type=str, nargs='?', help='文件名')
    parser.add_argument('--types', type=str, nargs='?', help='分类类型', default='group')
    parser.add_argument('--plot-type', type=str, nargs='?', help='图形类型', default='plot')
    parser.add_argument('--count-min', type=int, nargs='?', help='最小场次', default=0)
    parser.add_argument('--Y-min', type=float, nargs='?', help='最小Y值', default=0)
    parser.add_argument('--m', type=str, nargs='?', help='描述信息', default='')
    parser.add_argument('--save', type=int, nargs='?', help='是否需要存储', default=0)
    parser.add_argument('--sort-col', type=str, nargs='?', help='排序内容')
    parser.add_argument('--x-ticks', type=int, nargs='?', help='是否需要显示X轴', default=1)
    parser.add_argument('--endswith', type=str, nargs='?', help='是否需要显示X轴', default='')
    args = parser.parse_args()
    time_inv = args.f_name.split('_')[1]
    df = pd.read_csv(str(os.path.join(BASE, args.f_name)))
    df = df[df[args.X] != 'total']
    if args.endswith:
        df = df[df[args.X].endswith(args.endswith)]
    if args.count_min:
        df = df[df['counts'] >= args.count_min]
    try:
        df[args.X] = df[args.X].astype(int)
    except Exception as e:
        pass
    if args.sort_col:
        df = df.sort_values(by=args.sort_col)
    else:
        df = df.sort_values(by=args.X)
    color = ['r', 'b', 'c', 'g', 'k', 'm', 'y']
    y_list = args.Y.strip().split(',')
    if len(y_list) == 1 and args.Y_min:
        df = df[df[y_list[0]] > args.Y_min]
    # fig = plt.figure()
    fig, ax = plt.subplots(1, 1)
    # y_major_locator = MultipleLocator(10)
    # x_major_locator = MultipleLocator(10)
    # ax = plt.gca()
    # ax.xaxis.set_major_locator(x_major_locator)
    # ax.yaxis.set_major_locator(y_major_locator)
    # plt.ylim(0, 10)
    if args.plot_type == 'plot':
        xlt = 40 if df.shape[0] > 40 else df.shape[0]
        plt.xlim(0, xlt)
        for col in y_list:
            if color:
                c = color.pop()
            else:
                c = 'k'
            plt.plot(df[args.X], df[col], label=col, marker='o', color=c, linestyle='--', linewidth=2, markersize=2)
        for i in df.index[:xlt]:
            plt.text(df.loc[:, args.X][i], df.loc[:, y_list[0]][i], df.loc[:, 'counts'][i])
        if args.x_ticks:
            plt.xticks(df['group_key'][:xlt], rotation=90)
    elif args.plot_type == 'scatter':
        ax.xaxis.set_major_locator(ticker.MultipleLocator(2500))
        x = df[args.X]
        y = df[args.Y]
        plt.scatter(x, y)
        # if args.x_ticks:
        #     plt.xticks(df['group_key'], rotation=90)
    plt.legend()
    plt.grid(True)
    plt.title('%s' % time_inv)
    total = df[df['group_key'] == 'total']
    if args.types == 'group':
        plt.xlabel('%s(%s)' % (total['group'], total['allowance']))
    else:
        plt.xlabel('%s' % args.X)
    plt.ylabel('%s' % args.Y)
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
    if args.save:
        message = args.m or time.time()
        plt.savefig('save_img/{}.jpg'.format(message))
    plt.show()
    plt.close()


# def gen_fig_plot(fig, sizes):
#     ans = [1, 1, 0]
#     for i in range(1, sizes + 1):
#         if ans != sizes:
#             ans[2] += 1
#             yield fig.add_subplot(*ans)
#         else:
#             ans[2] = 1
#             if ans[1] != sizes:
#                 ans[1] += 1
#             else:
#                 ans[1] = 1
#                 ans[0] += 1
#             yield fig.add_subplot(*ans)


# def autolabel(rects):
#     for rect in rects:
#         height = rect.get_height()
#         plt.text(rect.get_x() + rect.get_width() / 2. - 0.2, 1.03 * height, '%s' % float(height))


if __name__ == '__main__':
    run()
