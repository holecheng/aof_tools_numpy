huan = set()
cheng = set()


with open('4-01-4-30.csv', 'r', encoding='utf-8') as f:
    for i in f.readlines():
        cheng.add(','.join(i.strip().split(',')[0:2]))

with open('ass_all.csv', 'r', encoding='utf-8') as f:
    for i in f.readlines():
        huan.add(','.join(i.strip().split(',')[0:2]))


print(len(huan - cheng))
print(len(cheng - huan))





