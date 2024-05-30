import numpy as np

npd = [[1, 4, 5], [2, 3, 1], [2, 3, None], [2, None, 1]]
npd = np.array(npd)
print(npd[np.any(npd[:, [1, 2]])])
