# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 16:17:44 2018

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

threshold = pd.Timedelta(minutes=4)
inputfile = "F:\spyder\datamining\chapter10\demo\data\water_heater.xls"
outputfile = "F:\spyder\datamining\chapter10\\1.xls"
data = pd.read_excel(inputfile)

data[u'发生时间'] = pd.to_datetime(data[u'发生时间'], format='%Y%m%d%H%M%S')
data = data[data[u'水流量']>0]
#相邻时间做差分，比较是否大于阈值
d = data[u'发生时间'].diff() > threshold
print(d)
data[u'事件编号'] = d.cumsum() + 1 #通过累积的方式求事件编号


#data.to_excel(outputfile)
        