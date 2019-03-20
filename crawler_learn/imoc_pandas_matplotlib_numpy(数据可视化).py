'''
教程地址：
    https://mp.weixin.qq.com/s/1JfztEbsYEY-s5weE_x4OA

'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# matplotlib不会每次启动时都重新扫描所有的字体文件并创建字体索引列表，
# 因此在复制完字体文件之后，需要运行下面的语句以重新创建字体索引列表
from matplotlib.font_manager import _rebuild

_rebuild()

data = pd.read_csv(
    "/Users/fan/Develop/Own_Workspace/Workspace_Python/PycharmProjects/2019_pycharm_python_test/crawler_learn/imoocc.csv")
data_num = data.sort_values(by='学习人数', ascending=False)

data_name = data_num['课程名称']
data_number = data_num['学习人数']

fig = plt.figure(figsize=(10, 6))
plt.style.use('ggplot')  # 绘图风格
plt.rcParams['font.sans-serif'] = ['SimHei']  # rcParams设置字体，把字体设置为支持中文的字体
plt.rcParams['axes.unicode_minus'] = False  # 使负号正常显示在坐标轴上

plt.bar(range(15), data_number[:15], width=0.8, align='center', color='steelblue', alpha=0.8)
plt.ylabel('title')
plt.title(u'课程的人数排名')
plt.xticks(range(15), data_name[:15])
fig.autofmt_xdate(rotation=45)
plt.show()

# 再来对慕课网上实战课程的讲师所包含的课程数量来做一个排名显示：
tea_count = data_num['讲师'].value_counts()
plt.style.use('ggplot')  # 绘图风格
plt.barh(range(10), list(reversed(tea_count[:10])), align='center', color='steelblue', alpha=0.8)
plt.xlabel('讲师课程数量')
plt.title('讲师课程的数量排名')
plt.yticks(range(10), reversed(tea_count.keys()[:10]))
plt.xlim([0, 10])
plt.show()

# 所含课程数量最多的讲师是 Michael__PK，我们可以看看他的所有课程都是什么。运行代码
data.loc[data['讲师'] == 'liuyubobobo']

# 对每个类别所含的课程数量做个排名，看看慕课网上在哪方面的课程数量会多一点，用饼图来作可视化
from random import randint

cls_count = data_num['课程类别'].value_counts()
cls_value = cls_count.map(lambda x: x / (len(cls_count)))
# 给每一种类别随机设定一种颜色
sample_list = '1234556789abcdef'
color_list = []
for _ in range(len(cls_count)):
    color = '#'
    for x in range(6):
        each = sample_list[randint(0, 15)]
        color += each
    color_list.append(color)

plt.figure(figsize=(9, 9))
plt.style.use('ggplot')

# 中文乱码和坐标轴负号的处理
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 将横纵坐标轴标准化处理，保证饼图是一个正圆，否则为椭圆
plt.axes(aspect='equal')

plt.xlim(0, 4)
plt.ylim(0, 4)

plt.pie(x=cls_value, explode=None, labels=cls_count.keys(), colors=color_list, autopct='%.1f%%',  # 一位浮点数
        pctdistance=0.8,  # 饼距离
        shadow=False,  # 阴影
        labeldistance=1.25,  # 标签离中心距离
        startangle=180,  # 初始角度
        radius=1.5,  # 半径
        counterclock=False,  # 不逆时针
        wedgeprops={'linewidth': 1.5, 'edgecolor': 'green'},  # 线条样式
        textprops={'fontsize': 12, 'color': 'k'},  # 字体样式
        center=(2, 1.8),
        frame=1)  # 显示背景框架

plt.xticks(())  # 把轴的刻度显示为空
plt.yticks(())

plt.title('每个类别占所有课程的比例')
plt.show()
