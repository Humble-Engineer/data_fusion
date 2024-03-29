import numpy as np
import matplotlib.pyplot as plt

'''模拟生成数据设置'''

base_grade = 100  # 样品的真实值，数据生成的均值μ

nose_error  = 0.2   # 设置电子鼻测量的相对误差限δ1
mouth_error = 0.05  # 设置电子舌测量的相对误差限δ2

nose_std_dev  = 5  # 设置电子鼻测量的标准差σ1
mouth_std_dev = 1  # 设置电子鼻测量的标准差σ2

data_counts = 20  # 生成数据的数量

# 设置模拟数据为正态分布或均匀分布
data_type = "normal"    # 正态分布
# data_type = "uniform"   # 均匀分布

# 固定加权法传感器1的权重
k1 = 0.4

'''用户设置部分结束'''

# 基于预设的数据分布样式生成随机数据
if data_type == "normal":

    # 正态分布：X~N(μ，σ^2)
    nose_datas  = np.random.normal(base_grade, nose_std_dev,  size=data_counts)
    mouth_datas = np.random.normal(base_grade, mouth_std_dev, size=data_counts)

else:
    # 均匀分布：X~U(μ*(1-δ),μ*(1+δ))
    nose_datas  = np.random.uniform(base_grade*(1-nose_error),  base_grade*(1+nose_error),  size=data_counts)
    mouth_datas = np.random.uniform(base_grade*(1-mouth_error), base_grade*(1+mouth_error), size=data_counts)


'''方法一,基于固定权重进行加权'''

'''计算加权后的结果'''

method1_values = k1 * nose_datas + (1-k1) * mouth_datas


'''方法二,基于卡尔曼滤波器自动加权'''

'''实时计算现有数据的方差'''
# 初始化一个列表来存储传感器1的方差
nose_variances = []
# 循环计算前n个元素的方差，n从2开始
for n in range(2, len(nose_datas)+1):
    subarray = nose_datas[:n]  # 使用切片获取前n个元素
    variance = np.var(subarray)  # 计算方差
    nose_variances.append(variance)  # 将方差添加到列表中
# print("nose_variances:", nose_variances)

# 初始化一个列表来存储传感器2的方差
mouth_variances = []
# 循环计算前n个元素的方差，n从2开始
for n in range(2, len(mouth_datas)+1):
    subarray = mouth_datas[:n]  # 使用切片获取前n个元素
    variance = np.var(subarray)  # 计算方差
    mouth_variances.append(variance)  # 将方差添加到列表中
# print("mouth_variances:", mouth_variances)

# 计算两个传感器的方差之和,作为卡尔曼增益系数k的分母
sum_variances = np.zeros(len(nose_datas)-1)
for i in range(len(nose_datas)-1):
    sum_variances[i] = nose_variances[i] + mouth_variances[i]
# print("sum_variances:", sum_variances)

'''计算卡尔曼增益系数'''
# 初始化一个列表来存储增益系数
k = np.zeros(len(nose_datas))
# 第一个数据无法计算方差,默认设置增益系数为50%
k[0] = 0.5
for i in range(len(nose_datas)-1):
    k[i+1] = mouth_variances[i] / sum_variances[i]
# print("k:", k)

'''计算加权后的结果'''
# 初始化一个列表来存储计算结果
method2_values = np.zeros(len(nose_datas))
for i in range(len(nose_datas)):
    method2_values[i] = k[i] * nose_datas[i] + (1 - k[i]) * mouth_datas[i]
# print("method2_values:", method2_values)


mean1, var1 = np.mean(nose_datas), np.var(nose_datas)
mean2, var2 = np.mean(mouth_datas), np.var(mouth_datas)

mean_method1, var_method1 = np.mean(method1_values), np.var(method1_values)
mean_method2, var_method2 = np.mean(method2_values), np.var(method2_values)

'''绘图部分'''

plt.rcParams['font.sans-serif'] = ['FangSong']  # 设置字体以便正确显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示连字符

top_color = 'red'  # 设置柱状图上半柱子的颜色
bottom_color = 'blue'  # 设置柱状图下半柱子的颜色
bar_width = 0.8  # 设置柱状图柱子的宽度
fig_size = (8, 6)  # 设置显示框的大小

# 创建一个图形和一个子图
fig, axs = plt.subplots(2, 2, figsize=fig_size)

# 假设我们有以下的名称、值和颜色
names = [str(i) for i in range(1, len(nose_datas) + 1)]

# 创建柱状图，并设置颜色  
axs[0, 0].bar(names, nose_datas, bar_width, color='blue')

# 设置x轴刻度位置  
tick_positions = [i for i, _ in enumerate(names)]  # 简单地使用枚举的索引作为x轴刻度位置  
axs[0, 0].set_xticks(tick_positions)
axs[0, 0].set_xticklabels(names)

# 显示当前数据集的均值和方差
if data_type == "normal":
    axs[0, 0].text(0.75, 1.2, f'实际均值: {mean1:.1f}\n实际方差: {var1:.1f}\n预设方差: {np.square(nose_std_dev):d}', transform=axs[0, 0].transAxes, fontsize=8, va='top')
else:
    axs[0, 0].text(0.75, 1.2, f'实际均值: {mean1:.1f}\n实际方差: {var1:.1f}\n预设误差限: {100*nose_error:.1f}%', transform=axs[0, 0].transAxes, fontsize=8, va='top') 

axs[0, 0].set_title('电子鼻直接读数')
axs[0, 0].set_xlabel('测量次数')
axs[0, 0].set_ylabel('测量结果')

# 创建柱状图，并设置颜色
axs[0, 1].bar(names, mouth_datas, bar_width, color='red')

# 设置x轴刻度位置  
tick_positions = [i for i, _ in enumerate(names)]  # 简单地使用枚举的索引作为x轴刻度位置  
axs[0, 1].set_xticks(tick_positions)
axs[0, 1].set_xticklabels(names) 

# 显示当前数据集的均值和方差
if data_type == "normal":
    axs[0, 1].text(0.75, 1.2, f'实际均值: {mean2:.1f}\n实际方差: {var2:.1f}\n预设方差: {np.square(mouth_std_dev):d}', transform=axs[0, 1].transAxes, fontsize=8, va='top')
else:
    axs[0, 1].text(0.75, 1.2, f'实际均值: {mean2:.1f}\n实际方差: {var2:.1f}\n预设误差限: {100*mouth_error:.1f}%', transform=axs[0, 1].transAxes, fontsize=8, va='top') 


axs[0, 1].set_title('电子舌直接读数')
axs[0, 1].set_xlabel('测量次数')
axs[0, 1].set_ylabel('测量结果')

# 循环遍历每个条形
for i, (name, value) in enumerate(zip(names, method1_values)):
    # 计算蓝色部分的高度
    blue_height = value * k1
    # 计算红色部分的高度
    red_height = value - blue_height
    # 计算条形的x位置（考虑条形宽度和间距）
    x_pos = i - (len(names) - 1) * bar_width / 2
    # 绘制底部的条形（蓝色部分）
    axs[1, 0].bar(x_pos, [blue_height], bar_width, color=bottom_color)
    # 绘制顶部的条形（红色部分），并稍微调整其底部位置
    axs[1, 0].bar(x_pos, [red_height], bar_width, bottom=blue_height, color=top_color)

# 设置x轴的位置和标签
axs[1, 0].set_xticks([i - (len(names) - 1) * bar_width / 2 for i in range(len(names))])
axs[1, 0].set_xticklabels(names)

# 显示当前数据集的均值和方差
axs[1, 0].text(0.75, 1.2, f'实际均值: {mean_method1:.1f}\n实际方差: {var_method1:.1f}\n预设权重: {k1:.2f}', transform=axs[1, 0].transAxes, fontsize=8, va='top') 

axs[1, 0].set_title('固定权重加权')
axs[1, 0].set_xlabel('测量次数')
axs[1, 0].set_ylabel('数据融合结果')

# 循环遍历每个条形
for i, (name, value) in enumerate(zip(names, method2_values)):
    # 计算蓝色部分的高度
    blue_height = k[i] * value
    # 计算红色部分的高度
    red_height = value - blue_height
    # 计算条形的x位置（考虑条形宽度和间距）
    x_pos = i - (len(names) - 1) * bar_width / 2
    # 绘制底部的条形（蓝色部分）
    axs[1, 1].bar(x_pos, [blue_height], bar_width, color=bottom_color)
    # 绘制顶部的条形（红色部分），并稍微调整其底部位置
    axs[1, 1].bar(x_pos, [red_height], bar_width, bottom=blue_height, color=top_color)

# 设置x轴的位置和标签
axs[1, 1].set_xticks([i - (len(names) - 1) * bar_width / 2 for i in range(len(names))])
axs[1, 1].set_xticklabels(names)

# 显示当前数据集的均值和方差
axs[1, 1].text(0.75, 1.2, f'实际均值: {mean_method2:.1f}\n实际方差: {var_method2:.1f}\n最终权重: {k[data_counts-1]:.2f}', transform=axs[1, 1].transAxes, fontsize=8, va='top') 

axs[1, 1].set_title('滤波器自动加权')
axs[1, 1].set_xlabel('测量次数')
axs[1, 1].set_ylabel('数据融合结果')

# 显示图形
plt.tight_layout()
plt.show()
