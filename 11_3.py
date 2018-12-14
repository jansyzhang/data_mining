# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 16:12:06 2018

"""

import pandas as pd

file = 'F:\spyder\datamining\chapter11\demo\data\predictdata.xls'
data = pd.read_excel(file)

abs_ = (data['预测值'] - data['实际值']).abs()
mae_ = abs_.mean() #mae
rmse_ = ((abs_ ** 2)).mean() ** 0.5 #rmse
mape_ = (abs_ / data[u'实际值']).mean() #mape

print(u'平均绝对误差为：%0.4f, \n均方根误差为：%0.4f, \n平均绝对百分误差为：%0.6f' %(mae_, rmse_, mape_))