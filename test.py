import numpy as np

npd = [[1, np.nan, 5], [2, 3, 1], [2, 3, 7], [2, 8, np.nan]]
npd = np.array(npd)
a = npd[1].tolist()
for i in npd[1]:
    print(i, type(i))
    print(i == 1)

