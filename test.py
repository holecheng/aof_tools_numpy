import numpy as np

npd = [['1', '', '5'], ['3', '3', '1'], ['2', '3', '7'], ['3', '6', ''], ['2', '8', '8'],]
npd = np.array(npd).astype(str)
str_data = np.char.strip(npd)
non_empty_rows = np.all(npd != '', axis=1)
filtered_data = str_data[non_empty_rows]
print(filtered_data)



