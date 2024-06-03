
def row():
    for i in range(10):
        yield i

def c():
    cnt = 0
    while True:
        print(1)
        row_dic = next(row())
        if cnt and cnt % 10000 == 0:
            print('已处理数据{} * 10000'.format(cnt // 10000))
        yield row_dic


row_dic = c()
print(row_dic)
