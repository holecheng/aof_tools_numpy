import numpy as np

npd = [['1', '', '5'], ['3', '3', '1'], ['2', '3', '7'], ['3', '6', ''], ['2', '8', '8'],]
npd = np.array(npd).astype(str)
npd = np.vstack((npd, np.array([1, 2, 3])))
print(npd)



