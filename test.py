import argparse
parser = argparse.ArgumentParser(description='传递参数')
parser.add_argument('--query-time', type=str, nargs='?', help='数据库连接方式')
a = parser.parse_args()
print(a)