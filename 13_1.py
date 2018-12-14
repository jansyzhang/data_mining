# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 16:25:15 2018

"""

import numpy as np
import pandas as pd

inputfile = 'F:\spyder\datamining\chapter13\demo\data\data1.csv'
data = pd.read_csv(inputfile)
'''
#------------------原始数据概括性度量---------------------
r = [data.min(), data.max(), data.mean(), data.std()] #依次计算最小值，最大值，均值，标准差
r = pd.DataFrame(r, index=['Min', 'Max', 'Mean', 'STD']).T
#print(np.round(r, 2))
#------------------原始数据求解Pearson相关系数-------------
pear = data.corr(method='pearson')
#print(np.round(pear, 2))
#------------------Adaptive-Lasso变量选择-----------------
from sklearn.linear_model import Lasso
model =  Lasso(alpha=0.1)
model.fit(data.iloc[:,0:13],data['y'])
#model.coef_.to_csv('1.csv')
#np.savetxt('1.xls',model.coef_)
'''
#------------------地方财政收入灰色预测--------------------
from GM11 import GM11 
data.index = range(1994, 2014)
print(data.index)
data.loc[2014] = None
data.loc[2015] = None
l = ['x1', 'x2', 'x3', 'x4', 'x5', 'x7']
for i in l:
    # f[0] ##获得灰色预测函数,  f[-1] # 获得小残差概率(p),  f[-2] # 获得后验比差值(c)
    f = GM11(data[i].loc[1992:2013].values)[0]
    data[i][2014] = f(len(data) - 1)    #2014年预测结果
    data[i][2015] = f(len(data)) #2015年预测结果
    data[i] = data[i].round(2)
#data[l+['y']].to_excel('data_GM11.xls')   
 