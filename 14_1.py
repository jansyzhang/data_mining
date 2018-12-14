# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 11:46:18 2018

"""

import pandas as pd

inputfile = 'F:\\spyder\\datamining\\chapter14\\demo\\data\\business_circle.xls'
data = pd.read_excel(inputfile, index_col=u'基站编号')

data = (data - data.min()) / (data.max() - data.min()) #离差标准化，最大最小标准化
data = data.reset_index()

#data.to_excel('3.xls', index=False)
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram #使用层次聚类函数

Z = linkage(data, method='ward', metric='euclidean') #画出谱系图
P = dendrogram(Z, 0)
plt.show()
#通过谱系图，可以很清楚的看到，可以把聚类类别数取为3类

from sklearn.cluster import AgglomerativeClustering #导入层次聚类函数
model = AgglomerativeClustering(n_clusters=3, linkage='ward')
model.fit(data) 

#详细输出原始数据及其类别
r = pd.concat([data, pd.Series(model.labels_, index=data.index)], axis=1)
r.columns = list(data.columns) + [u'聚类类别'] #重命名表头
print(r.columns)

plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用正常显示负号

style = ['ro-', 'go-', 'bo-']
xlables = [u'工作日人均停留时间', u'凌晨人均停留时间', u'周末人均停留时间', u'日均人流量']
pic_output = 'type_' #聚类图文件名前缀

for i in range(3):
    plt.figure()
    tmp = r[r[u'聚类类别'] == i].iloc[:,1:5] #提取每一类
    print(tmp.columns)
    for j in range(len(tmp)):
        plt.plot(range(1, 5), tmp.iloc[j], style[i])
    
    plt.xticks(range(1,5), xlables, rotation=20) #坐标标签
    plt.subplots_adjust(bottom=0.15) #调整底部
    plt.show()
    plt.savefig(u'%s%s.png' %(pic_output, i)) #保存图片
    

