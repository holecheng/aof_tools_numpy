

cnt = 12300

vid = 1000
cnt_s = 200


c,  d = divmod(cnt, vid)
print(c, d)  # 12 300

if d < cnt_s:
    print(f'{c}{0}')
else:
    print(f'{c}-{d // cnt_s}', f'{c}-{d // cnt_s + 1}')



