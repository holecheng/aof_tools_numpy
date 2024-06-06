huan = []
cheng = []


with open('../output/2024-04-01,2024-04-02hand_detail.csv', 'r') as f:
    for i in f.readlines():
        q, p = i.strip().split(',')
        cheng.append((q, p))

with open('game.csv', 'r') as f:
    for i in f.readlines():
        p, q = i.replace('\n', '').strip().split(',')
        huan.append((q, p))

diff = []
for i in huan:
    if i not in cheng:
        diff.append(i)

print(len(diff))
for i in diff:
    print(i)

diff2 = []
for i in cheng:
    if i not in huan:
        diff2.append(i)

print(len(diff2))
for i in diff2:
    print(i)


