huan = []
cheng = []


with open('4-01-4-30.csv', 'r', encoding='utf-8') as f:
    for i in f.readlines():
        cheng.append(i.strip().split(',')[0:2])

with open('ass_all.csv', 'r', encoding='utf-8') as f:
    for i in f.readlines():
        huan.append(i.strip().split(',')[0:2])

for i in huan:
    if i not in cheng:
        print(','.join(i))




