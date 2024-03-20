
import numpy as np  
import matplotlib.pyplot as plt  
  
# 创建一些示例数据  
np.random.seed(0)  
data1 = np.random.randn(100)  
data2 = np.random.randn(100) + 2  
  
# 计算均值和方差  
mean1, var1 = np.mean(data1), np.var(data1)  
mean2, var2 = np.mean(data2), np.var(data2)  
  
# 创建子图  
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))  
  
# 绘制直方图  
axs[0].hist(data1, bins=20, alpha=0.7, color='g')  
axs[1].hist(data2, bins=20, alpha=0.7, color='b')  
  
# 在子图上标注均值和方差  
axs[0].text(0.05, 0.95, f'Mean: {mean1:.2f}\nVar: {var1:.2f}', transform=axs[0].transAxes, fontsize=12, va='top')  
axs[1].text(0.05, 0.95, f'Mean: {mean2:.2f}\nVar: {var2:.2f}', transform=axs[1].transAxes, fontsize=12, va='top')  
  
# 设置标题和标签  
axs[0].set_title('Data 1')  
axs[1].set_title('Data 2')  
  
# 显示图形  
plt.tight_layout()  
plt.show()

