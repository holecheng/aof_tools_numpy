import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np

# 假设有如下的观察频率分布
observed = pd.DataFrame([
    [0.8, 0.8, 0.8],
    [0.4, 0.5, 0.5],
    [0.3, 0.2, 0.2]
])
# 执行卡方检验
# 第一个返回值是卡方统计量，第二个返回值是p值
chi2, p, dof, expected = chi2_contingency(observed.values)

# 输出结果
print(f"卡方统计量: {chi2}")  # ∑(观察频数 - 期望频数)
print(f"p值: {p}")  #
print(f"自由度: {dof}") # 自由度  行-1 * 列-1
print(f"期望频率: \n{expected}")  # 期望频率 行总频数*列总频数/总频数
npd = np.array(((observed**2 - expected**2) / observed).apply(np.abs))
print(npd)
print(npd.sum())

# 根据p值判断是否拒绝原假设
if p < 0.05:
    print("拒绝原假设，观察频率分布不独立。")
else:
    print("接受原假设，观察频率分布独立")
