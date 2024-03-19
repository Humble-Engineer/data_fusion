import numpy as np
import matplotlib.pyplot as plt


'''模拟生成数据设置'''

base_grade = 2       #样品的真实值（数据生成的基准值）
nose_error = 0.2     #模拟电子鼻的测量误差
mouth_error = 0.05   #模拟电子舌的测量误差

data_counts = 10     #生成数据数量

'''修改以上参数即可'''


# 设置字体以便正确显示中文
plt.rcParams['font.sans-serif'] = ['FangSong']
# 正确显示连字符
plt.rcParams['axes.unicode_minus'] = False

top_color = 'red'
bottom_color = 'blue'
bar_width = 0.8
fig_size = (8,6)

# 模拟生成随机数据
nose_datas = np.random.uniform(base_grade*(1-nose_error), base_grade*(1+nose_error), size=data_counts)
mouth_datas = np.random.uniform(base_grade*(1-mouth_error), base_grade*(1+mouth_error), size=data_counts)

print(nose_datas)
print(mouth_datas)

# 基于固定权重进行加权结果
method1_values = 0.4*nose_datas + 0.6*mouth_datas


# 初始化一个列表来存储每个阶段的方差
nose_variances = []
nose_variances.append(0.5)  # 将方差添加到列表中

# 循环计算前n个元素的方差，n从2开始，直到数组的长度
for n in range(2, len(nose_datas) + 1):
       subarray = nose_datas[:n]  # 使用切片获取前n个元素
       variance = np.var(subarray)  # 计算方差
       nose_variances.append(variance)  # 将方差添加到列表中

print("nose_variances:", nose_variances)


# 初始化一个列表来存储每个阶段的方差
mouth_variances = []
mouth_variances.append(0.5)  # 将方差添加到列表中

# 循环计算前n个元素的方差，n从2开始，直到数组的长度
for n in range(2, len(mouth_datas) + 1):
       subarray = mouth_datas[:n]  # 使用切片获取前n个元素
       variance = np.var(subarray)  # 计算方差
       mouth_variances.append(variance)  # 将方差添加到列表中

print("mouth_variances:", mouth_variances)

sum_variances = np.zeros(len(nose_datas))
for i in range(len(nose_datas)):
       sum_variances[i] = nose_variances[i] + mouth_variances[i]
print("sum_variances:", sum_variances)

k = np.zeros(len(nose_datas))
for i in range(len(nose_datas)):
       k[i] = mouth_variances[i]/sum_variances[i]
print("k:", k)

method2_values = np.zeros(len(nose_datas))
for i in range(len(nose_datas)):
       method2_values[i] = k[i]*nose_datas[i] + (1-k[i])*mouth_datas[i]
print("method2_values:", method2_values)



# 创建一个图形和一个子图
fig, axs = plt.subplots(2, 2, figsize=fig_size)


# 假设我们有以下的名称、值和颜色
names = [str(i) for i in range(1, len(nose_datas)+1)]

# 创建柱状图，并设置颜色  
axs[0,0].bar(names, nose_datas, bar_width, color='blue')  
  
# 设置x轴刻度位置  
tick_positions = [i for i, _ in enumerate(names)]  # 简单地使用枚举的索引作为x轴刻度位置  
axs[0,0].set_xticks(tick_positions)
axs[0,0].set_xticklabels(names)

axs[0,0].set_title('电子鼻直接读数')
axs[0,0].set_xlabel('测量次数')
axs[0,0].set_ylabel('测量结果')



# 创建柱状图，并设置颜色  
axs[0,1].bar(names, mouth_datas, bar_width, color='red')  
  
# 设置x轴刻度位置  
tick_positions = [i for i, _ in enumerate(names)]  # 简单地使用枚举的索引作为x轴刻度位置  
axs[0,1].set_xticks(tick_positions)
axs[0,1].set_xticklabels(names)

axs[0,1].set_title('电子舌直接读数')
axs[0,1].set_xlabel('测量次数')
axs[0,1].set_ylabel('测量结果')



# 循环遍历每个条形
for i, (name, value) in enumerate(zip(names, method1_values)):
    # 计算蓝色部分的高度（占40%）
    blue_height = value * 0.4
    # 计算红色部分的高度（占剩余的60%）
    red_height = value - blue_height
    # 计算条形的x位置（考虑条形宽度和间距）
    x_pos = i - (len(names) - 1) * bar_width / 2
    # 绘制底部的条形（蓝色部分）
    axs[1,0].bar(x_pos, [blue_height], bar_width, color=bottom_color)
    # 绘制顶部的条形（红色部分），并稍微调整其底部位置
    axs[1,0].bar(x_pos, [red_height], bar_width, bottom=blue_height, color=top_color)

# 设置x轴的位置和标签
axs[1,0].set_xticks([i - (len(names) - 1) * bar_width / 2 for i in range(len(names))])
axs[1,0].set_xticklabels(names)

axs[1,0].set_title('自定义参数固定加权')
axs[1,0].set_xlabel('测量次数')
axs[1,0].set_ylabel('数据融合结果')


# 循环遍历每个条形
for i, (name, value) in enumerate(zip(names, method2_values)):
    # 计算蓝色部分的高度（占40%）
    blue_height = k[i]*value
    # 计算红色部分的高度（占剩余的60%）
    red_height = value - blue_height
    # 计算条形的x位置（考虑条形宽度和间距）
    x_pos = i - (len(names) - 1) * bar_width / 2
    # 绘制底部的条形（蓝色部分）
    axs[1,1].bar(x_pos, [blue_height], bar_width, color=bottom_color)
    # 绘制顶部的条形（红色部分），并稍微调整其底部位置
    axs[1,1].bar(x_pos, [red_height], bar_width, bottom=blue_height, color=top_color)

# 设置x轴的位置和标签
axs[1,1].set_xticks([i - (len(names) - 1) * bar_width / 2 for i in range(len(names))])
axs[1,1].set_xticklabels(names)

axs[1,1].set_title('卡尔曼滤波器自动加权')
axs[1,1].set_xlabel('测量次数')
axs[1,1].set_ylabel('数据融合结果')


# 显示图形
plt.tight_layout()
plt.show()