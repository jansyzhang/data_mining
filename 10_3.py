# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 11:36:30 2018

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''data exploring'''

inputfile = "F:\spyder\datamining\chapter10\demo\data\water_heater.xls"
data = pd.read_excel(inputfile)

data[u'发生时间'] = pd.to_datetime(data[u'发生时间'], format='%Y%m%d%H%M%S')
data = data[data[u'水流量']>0]
'''Pandas计算出的时间间隔数据的类型是np.timedelta64,
 不是Python标准库中的timedelta类型，因此没有total_minutes()函数，
 需要除以np.timedelta64的1分钟来计算间隔了多少分钟。'''
data[u'用水停顿时间间隔'] = data[u'发生时间'].diff() / np.timedelta64(1, 'm') #计算间隔了多少分钟
data = data.fillna(0)

'''step1: check maximum, minimum of each column'''
data_explore = data.describe().T
print(data_explore)
data_explore['null'] = len(data) - data_explore['count'] # numbers of nulls
explore = data_explore[['min', 'max', 'null']]
explore.columns = [u'最小值', u'最大值', u'空值数']
print(explore)

'''step2: Discretization and surface division'''
Ti = list(data[u'用水停顿时间间隔']) #将要面元化的数据转化为一维列表
timegaplist = [0.0, 0.1, 0.2, 0.3, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 2100] #确定划分区间
cats = pd.cut(Ti, timegaplist, right=False) #包括区间左端，类似于[0， 0.1)，(默认则包含又端点)
x = pd.value_counts(cats)
'''
nplace参数的理解：
修改一个对象时：
inplace=True：不创建新的对象，直接对原始对象进行修改；
inplace=False：对数据进行修改，创建并返回新的对象承载其修改结果。
'''
x.sort_index(inplace=True)
dx = pd.DataFrame(x, columns=['num'])
dx['fn'] = dx['num'] / sum(dx['num'])
dx['cumfn'] = dx['num'].cumsum() / sum(dx['num'])
f1 = lambda x : '%.2f%%' % (x * 100)
dx[['f']] = dx[['fn']].applymap(f1)
print(dx)

'''绘制水停顿时间间隔频率分布直方图'''
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
dx['fn'].plot(kind='bar')
plt.ylabel(u'频率/组距')
plt.xlabel(u'时间间隔（分钟）')
p = 1.0 *dx['fn'].cumsum() / dx['fn'].sum()
dx['cumfn'].plot(color='r', secondary_y=True, style='-o', linewidth=2)
#添加注释，即85%处的标记。这里包括了指定箭头样式。
plt.annotate(format((p[4]), '.4%'), xy = (7, p[4]), xytext=(7*0.9, p[4]*0.95), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2")) 

plt.title(u'用水停顿时间间隔频率分布直方图')
plt.grid(axis='y',linestyle='--')

#fig.autofmt_xdate() #自动根据标签长度进行旋转
#此语句完成功能同上,但是可以自定义旋转角度
for label in ax.xaxis.get_ticklabels():   
       label.set_rotation(60)
plt.show()

#data = or_data.drop(or_data.columns[[0,5,9]],axis=1) # 删掉不相关属性

'''step3: 用水事件阈值寻优模型'''
timedeltalist = np.arange(2.25,8.25,0.25)
# 从2.25到8.25间，以间隔为0.25，确定阈值即，阈值范围为[2.25,2.5,2.75,3,...,7.75,8]
counts = [] # 记录不同阈值下的事件个数
for i in range(len(timedeltalist)):
    threshold = pd.Timedelta(minutes = timedeltalist[i])#阈值为四分钟
    d = data[u'发生时间'].diff() > threshold #  # 相邻时间做差分，比较是否大于阈值
    data[u'事件编号'] = d.cumsum() + 1 # 通过累积求和的方式为事件编号
    temp = data[u'事件编号'].max()
    counts.append(temp)
coun = pd.Series(counts, index=timedeltalist)

# 画频率分布直方图
#将阈值与对应的事件数绘制成频率分布直方图，以确定最优阈值
 
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']= False
plt.rc('figure', figsize=(8,6))
np.set_printoptions(precision=4) #保留小数点后4位
fig = plt.figure()
fig.set(alpha=0.2)#设置图标透明度
ax = fig.add_subplot(1,1,1)
# coun.plot(linestyle='-.',color='r',marker='<')
coun.plot(style='-.r*')#同上
ax.locator_params('x',nbins = int(len(coun)/2)+1)  # (****)locator_params进行对坐标轴刻度的调整，通过nbins设置坐标轴一共平均分为几份
ax.set_xlabel(u'用水事件间隔阈值(分钟)')
ax.set_ylabel(u'事件数（个）')
ax.grid(axis='y',linestyle='--') # (****)
plt.savefig('threshold_numofCase.jpg')
plt.show()    

