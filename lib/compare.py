huan = []
cheng = []


with open('4-01-4-30.csv', 'r', encoding='utf-8') as f:
    for i in f.readlines():
        if i.split(',')[-1].strip() != '2024-04-01' and i.split(',')[-1].strip() != 'timestamp':
            break
        cheng.append(i)

with open('all_detail.csv', 'r', encoding='utf-8') as f:
    for i in f.readlines():
        if i.split(',')[-1].strip() != '2024-04-01' and i.split(',')[-1].strip() != 'timestamp':
            break
        huan.append(i)

diff = []
for i in cheng:
    if i not in huan:
        diff.append(i)

print(len(diff))

for i in diff:
    print(i)



