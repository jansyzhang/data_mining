# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 10:56:56 2018


"""

import pandas as pd

from apriori import *

inputfile = 'F:\\spyder\\datamining\\chapter5\\demo\\data\\menu_orders.xls'
outputfile = 'F:\\spyder\\datamining\\chapter5\\apriori_rules.xls'
data = pd.read_excel(inputfile, header=None)

print(u'\n转换原始数据至0-1矩阵...')
ct = lambda x : pd.Series(1, index=x[pd.notnull(x)])#转换0-1矩阵的过渡函数
b = map(ct, data.values)
data = pd.DataFrame(list(b)).fillna(0)#实现矩阵转换，空值使用0填充
print(u'\n转换完毕')
del b

'''support = 0.2#最小支持度
confidence = 0.5#最小置信度
ms = '---' #连接符，用来区分不同的元素
find_rule(data, support, confidence, ms).to_excel(outputfile)'''
