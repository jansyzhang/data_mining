# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 17:14:16 2018

"""

import pandas as pd
from scipy.interpolate import lagrange

inputfile = 'F:\spyder\datamining\chapter6\demo\data\missing_data.xls'
outputfile = 'F:\spyder\datamining\chapter6\missing_data_process.xls'

data = pd.read_excel(inputfile, header=None)

def ployinterp_column(s, n, k=5):
    y = s[list(range(n-k, n)) + list(range(n+1, n+1+k))] #取值
    y = y[y.notnull()] #剔除空值
    print("----------------")
    print(y.index)
    print(list(y))
    return lagrange(y.index, list(y))(n) #插值并返回插值多项式,代入n得到插值结果

#逐元素判断是否插值
for i in data.columns:
    for j  in range(len(data)):
        if(data[i].isnull())[j]: #如果为空即插值
            data[i][j] = ployinterp_column(data[i], j)
            
data.to_excel(outputfile, header=None, index=False) #输出结果