# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 21:54:02 2018


"""

import numpy as np
import pandas as pd

#参数初始化
inputfile = 'F:\\spyder\\datamining\\chapter5\\demo\\data\\consumption_data.xls'
k = 3#聚类类别
threshold = 2#离散点阈值
iteration = 500#聚类最大循环次数
data = pd.read_excel(inputfile, index_col='Id')#读取数据
data_zs = 1.0*(data - data.mean())/data.std()#数据标准化

from sklearn.cluster import KMeans
model = KMeans(n_clusters = k, max_iter = iteration)
model.fit(data_zs)

#标准化数据及其类别
r = pd.concat([data_zs, pd.Series(model.labels_, index = data.index)], axis = 1)
#每个样本对应的类别
r.columns = list(data.columns) + [u'聚类类别']#重命名表头

norm = []
for i in range(k):
    norm_tmp = r[['R', 'F', 'M']][r[u'聚类类别'] == i] - model.cluster_centers_[i]
    norm_tmp = norm_tmp.apply(np.linalg.norm, axis = 1)#求出绝对距离
    norm.append(norm_tmp/norm_tmp.median())#求相对距离并添加
norm = pd.concat(norm)

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']#用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False#用来正常显示正负号
norm[norm <= threshold].plot(style = 'go')#正常点

discrete_points = norm[norm > threshold]
discrete_points.plot(style = 'ro')

for i in range(len(discrete_points)):
    id = discrete_points.index[i]
    n = discrete_points.iloc[i]
    plt.annotate('%s, %0.2f' %(id, n), xy = (id, n), xytext = (id, n))

plt.xlabel(u'编号')
plt.ylabel(u'相对距离')
plt.show()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            