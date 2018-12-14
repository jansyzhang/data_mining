# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 11:28:52 2018


"""

import pandas as pd
'''catering_sale = 'F:\spyder\datamining\chapter3\demo\data\catering_sale.xls'
data = pd.read_excel(catering_sale, index_col = u'日期') #指定日期为索引列
#print(data.describe())

#绘制箱型图
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']#用来显示中文标签
plt.rcParams['axes.unicode_minus'] = False;
            
plt.figure()
p = data.boxplot(return_type='dict')#画箱线图
#flies为异常值的标签
x = p['fliers'][0].get_xdata()
y = p['fliers'][0].get_ydata()
y.sort()

#用annotate添加注释
#其中有些相近的点，注解会出现重叠，难以看清，需要一些技巧来控制。
#以下参数都是经过调试的，需要具体问题具体调试。
# 第一个参数是注释的内容
# xy设置箭头尖的坐标
# xytext设置注释内容显示的起始位置

for i in range(len(x)): 
  if i>0:
    plt.annotate(y[i], xy = (x[i],y[i]), xytext=(x[i]+0.05 -0.8/(y[i]-y[i-1]),y[i]))
  else:
    plt.annotate(y[i], xy = (x[i],y[i]), xytext=(x[i]+0.08,y[i]))

plt.show() #展示箱线图'''

#数据统计量计算
'''data = data[(data[u'销量'] > 400)&(data[u'销量'] < 5000)]#过滤异常数据
statistics = data.describe()#保存基本统计量
#loc[]通过行标签索引数据
statistics.loc['range'] = statistics.loc['max'] - statistics.loc['min']#极差
statistics.loc['var'] = statistics.loc['std']/statistics.loc['mean']#变异系数
statistics.loc['dis'] = statistics.loc['75%'] - statistics.loc['25%']#四分数间距
print(statistics)'''

#菜品盈利帕累托图
'''dish_profit = 'F:\spyder\datamining\chapter3\demo\data\catering_dish_profit.xls'
data = pd.read_excel(dish_profit,index = u'菜品名')
data = data[u'盈利'].copy()

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

plt.figure()
data.plot(kind = 'bar')
plt.ylabel(u'盈利（元）')
#求累加次数
p = 1.0*data.cumsum()/data.sum()
p.plot(color = 'r', secondary_y = True, style = '-o',linewidth = 2)
plt.annotate(format(p[6], '.4%'), xy = (6, p[6]), xytext=(6*0.9, p[6]*0.9), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2")) #添加注释，即85%处的标记。这里包括了指定箭头样式。
plt.ylabel(u'盈利（比例）')
plt.show()'''

#相关性分析
'''catering_sale = 'F:\spyder\datamining\chapter3\demo\data\catering_sale_all.xls'
data = pd.read_excel(catering_sale, index_col = u'日期') #指定日期为索引列
print(data.corr())#相关系数矩阵，即给出任意两款菜式之间的相关系数
#print(data.corr()[u'百合酱蒸凤爪'])#只显示“百合酱蒸凤爪”与其他菜式的相关系数
print(data[u'百合酱蒸凤爪'].corr(data[u'翡翠蒸香茜饺'])) #计算“百合酱蒸凤爪”与“翡翠蒸香茜饺”的相关系数'''

import matplotlib.pyplot as plt
labels = 'Frogs','Hogs','Dogs','Logs'#定义标签
sizes = [15,30,45,10]#每一块的比例
colors = ['yellowgreen','gold','lightskyblue','lightcoral']#每一块的颜色
explode = (0,0.1,0,0)#突出显示，仅仅突出第二块
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')#显示为圆（避免比例压缩为椭元）
plt.show()
     
