import math
from functools import reduce

import matplotlib.pyplot as plt


def gen_fig_plot(sizes: int):
    ans = [sizes, sizes, 0]
    for _ in range(1, sizes ** 2 + 1):
        ans[-1] += 1
        yield reduce(lambda x, y: x*10+y, ans)


plt.figure()

gen_ans = gen_fig_plot(3)
while True:
    try:
        nas = next(gen_ans)
        plt.subplot(nas)
        plt.plot([0, 1], [0, 1])
    except:
        break
plt.show()
















'''
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
 
# 假设有以下分类变量数据
data = np.array([[48, 11, 3, 3],
                 [20, 5, 2, 1],
                 [6, 1, 1, 1],
                 [1, 1, 1, 1]])
 
# 调用chi2_contingency进行卡方检验
chi2, p, dof, expected = chi2_contingency(data)
 
# 输出卡方值、p值和自由度
print("卡方值:", chi2)
print("p值:", p)
print("自由度:", dof)
 
# 如果需要基于p值来判断是否拒绝原假设，可以设定一个显著性水平，例如0.05
alpha = 0.05
if p < alpha:
    print("拒绝原假设，数据有显著性差异")
else:
    print("不能拒绝原假设，数据无显著性差异")
'''