import numpy as np

npd = [[1, 4, 5], [2, 3, 1], [2, 3, 7], [2, 8, 1]]
npd = np.array(npd)
groups = npd[:, 0]
print(type(groups))
ns = []
for i, group in enumerate(np.unique(groups)):
    print("Group", i + 1)
    print(npd[groups == group][:, 1:])
    # print(11111, np.mean(npd[groups == group][:, 1:], axis=0))
    ns.append(np.mean(npd[groups == group][:, 1:], axis=0))

ans = np.vstack(ns)
print(ans)

