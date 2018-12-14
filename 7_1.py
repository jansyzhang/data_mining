# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 17:12:37 2018

"""


import pandas as pd
import numpy as np

datafile = "F:\\spyder\\datamining\\chapter7\\demo\\data\\air_data.csv"
'''resultfile = "F:\\spyder\\datamining\\chapter7\\explore.xls"

data = pd.read_csv(datafile, encoding='utf-8')
#对数据的基本描述，percentiles参数是指定计算多少的分位数表（eg.1/4分位数，中位数）
explore = data.describe(percentiles=[], include='all').T
explore['null'] = len(data) - explore['count'] #describe函数自动计算非空值数，空值数需要手动计算

explore = explore[['null', 'max', 'min']]
explore.column = [u'空值数', u'最大值', u'最小值'] #表头重命名

explore.to_excel(resultfile)'''

#cleanedfile = 'F:\\spyder\\datamining\\chapter7\\data_cleaned.xls'

data = pd.read_csv(datafile, encoding='utf-8')

data = data[data['SUM_YR_1'].notnull()&data['SUM_YR_2'].notnull()]#票价非空值才保留
#只保留票价非零的，或者平均折扣率与飞行公里数同时为0的记录
index1 = data['SUM_YR_1'] != 0 
index2 = data['SUM_YR_2'] != 0
index3 = (data['SEG_KM_SUM'] == 0) & (data['avg_discount'] == 0)
data = data[index1|index2|index3]

#data.to_excel(cleanedfile)
data = data[['FFP_DATE','LOAD_TIME','FLIGHT_COUNT','avg_discount','SEG_KM_SUM','LAST_TO_END']]

#data['L'] = data['LOAD_TIME'] - data['FFP_DATE']
d_ffp = pd.to_datetime(data['FFP_DATE'])
d_load = pd.to_datetime(data['LOAD_TIME'])
res = d_load - d_ffp
data2=data.copy()
data2['L'] = res.map(lambda x: x / np.timedelta64(30 * 24 * 60, 'm'))
data2['R'] = data['LAST_TO_END']
data2['F'] = data['FLIGHT_COUNT']
data2['M'] = data['SEG_KM_SUM']
data2['C'] = data['avg_discount']
data3 = data2[['L', 'R', 'F', 'M', 'C']]

data3 = (data3 - data3.mean(axis=0))/(data3.std(axis=0))
data3.columns = ['z'+i for i in data3.columns] #表头重命名

zscoredfile = "F:\\spyder\\datamining\\chapter7\\zscoreddata.xls"
data3.to_excel(zscoredfile, index=False)







