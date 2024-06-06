import argparse
import math
import time

from matplotlib import pyplot as plt

import pandas as pd
import os

from matplotlib.ticker import MultipleLocator

BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')


def run():
    parser = argparse.ArgumentParser(description='传递参数')
    parser.add_argument('--X', type=str, nargs='?', help='X轴', default='group_key')
    parser.add_argument('--Y', type=str, nargs='?', help='Y轴', default='avg_ev,avg_outcome')
    parser.add_argument('--f-name', type=str, nargs='?', help='文件名')
    parser.add_argument('--types', type=str, nargs='?', help='分类类型', default='group')
    parser.add_argument('--plot-type', type=str, nargs='?', help='图形类型', default='plot')
    parser.add_argument('--count-min', type=int, nargs='?', help='最小场次', default=0)
    parser.add_argument('--m', type=str, nargs='?', help='描述信息', default='')
    parser.add_argument('--save', type=int, nargs='?', help='是否需要存储', default=0)
    parser.add_argument('--sort-col', type=str, nargs='?', help='排序内容')
    args = parser.parse_args()
    df = pd.read_csv(str(os.path.join(BASE, args.f_name)))
    total = df[df[args.X] == 'total']
    df = df[df[args.X] != 'total']
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
    # fig = plt.figure()
    fig, ax = plt.subplots(1, 1)
    y_major_locator = MultipleLocator(0.1)
    x_major_locator = MultipleLocator(1)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.ylim(0, 1.0)
    plt.xlim(0, 100)
    if args.plot_type == 'plot':
        for col in y_list:
            if color:
                c = color.pop()
            else:
                c = 'k'
            plt.plot(df[args.X], df[col], marker='o', color=c, linestyle='--', linewidth=2, markersize=2)
    elif args.plot_type == 'scatter':
        x = df[args.X]
        y = df[args.Y]
        plt.scatter(x, y)
    plt.legend()
    plt.grid(True)
    plt.title('%s && %s' % (args.X, args.Y))
    if args.types == 'group':
        plt.xlabel('%s(%s)' % (total.loc[1, 'group'], total.loc[1, 'allowance']))
    else:
        plt.xlabel('%s' % args.X)
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
