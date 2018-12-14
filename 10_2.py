# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 09:59:42 2018

"""

import numpy as np
import pandas as pd

inputfile = "F:\spyder\datamining\chapter10\demo\data\water_heater.xls"
outputfile = "F:\spyder\datamining\chapter10\\2.xls"
n = 4 #使用以后四个点的平均斜率

threshold = pd.Timedelta(minutes=5) #专家阈值，创建时间间隔对象
data = pd.read_excel(inputfile)
data[u'发生时间'] = pd.to_datetime(data[u'发生时间'], format='%Y%m%d%H%M%S')
data = data[data[u'水流量']>0]

def event_num(ts):
    d = data[u'发生时间'].diff() > threshold
    return d.sum() + 1

dt = [pd.Timedelta(minutes=i) for i in np.arange(1, 9, 0.25)]
print(dt)
h = pd.DataFrame(dt, columns=[u'阈值']) #定义阈值列
h[u'事件数'] = h[u'阈值'].apply(event_num) #计算每个阈值对应的事件个数
h[u'斜率'] = h[u'事件数'].diff()/0.25 #计算相邻两点对用的斜率
h[u'斜率指标'] = h[u'斜率'].abs().rolling(n).mean() #采用后n个斜率绝对值平均作为斜率的指标
#用idxmin返回最小值的index,由于rolling_mean自动进行的是前n个斜率的绝对值平均，
#所以结果要进行平移（-n）
#h.to_excel(outputfile)
ts = h[u'阈值'][h[u'斜率指标'].idxmin() - n]

if ts > threshold:
    ts = pd.DataFrame(minutes=4)
    
print(ts)

 