import collections

cnt = 1230

vid = 100
cnt_s = 20


def get_key(i):
    c, d = divmod(i, vid)
    if d < cnt_s:
        return f'{c}{0}'
    else:
        return f'{c}-{d // cnt_s}', f'{c}-{d // cnt_s + 1}'


dic = collections.defaultdict(list)
for i in range(cnt):
    dic[get_key(i)].append(i)

print(dic)



