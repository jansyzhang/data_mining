# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 10:36:46 2018

"""

import pandas as pd
from sklearn.cluster import KMeans

datafile = "F:\\spyder\\datamining\\chapter8\\demo\\data\\data.xls"
processfile = "F:\\spyder\\datamining\\chapter8\\1.xls"
typelabel = {u'肝气郁结证型系数':'A',
             u'热毒蕴结证型系数':'B', 
             u'冲任失调证型系数':'C',
             u'气血两虚证型系数':'D',
             u'脾胃虚弱证型系数':'E',
             u'肝肾阴虚证型系数':'F'}
k = 4

#读取数据并进行聚类分析
data = pd.read_excel(datafile)
keys = list(typelabel.keys())
values = list(typelabel.values())
result = pd.DataFrame()

#判断是否在主窗口运行
#if __name__ == '__main__':
for i in range(len(keys)):
    #调用KMeans算法进行离散化
    print(u'正在运行"%s"的聚类...' % keys[i])
    kmodel = KMeans(n_clusters=k)
    kmodel.fit(data[[keys[i]]].values)
        
    #r1 = pd.DataFrame(kmodel.cluster_centers_, columns=[typelabel[keys[i]]])#聚类中心
    r1 = pd.DataFrame(kmodel.cluster_centers_, columns=[typelabel[keys[i]]])#eg:A cluster_centers 
    r2 = pd.Series(kmodel.labels_).value_counts()#分类统计
    r2 = pd.DataFrame(r2, columns=[typelabel[keys[i]]+'n'])#eg:An labels_count 
    r = pd.concat([r1, r2], axis=1).sort_values(typelabel[keys[i]]) #匹配聚类中心和类别数目
    r.index = [1, 2, 3, 4]
        
    
    '''将原来的聚类中心改为边界点'''
    #计算相邻两列的均值，以此作为边界点
    r[typelabel[keys[i]]] = r[typelabel[keys[i]]].rolling(2).mean()
    r[typelabel[keys[i]]][1] = 0
    result = result.append(r.T)
        
result = result.sort_index() #以index排序
# result.to_excel(processfile)

result_ = result.iloc[::2, :]
result_count = result.iloc[1::2, :]

 # 提取要建模的各证型
data_ = data[[keys[i] for i in range(len(keys))]] 
#聚类指标A1,A2......
strabc = pd.DataFrame()
for i in range(len(keys)):
    strabcd = [values[i] + '%s' % (j + 1) for j in range(k)]
    strabcd = pd.DataFrame(strabcd, columns=[values[i]])# columns=[values[i]],columns须是list，要转化加[],[values[]]
    strabc = strabc.append(strabcd.T)
    
#print(strabc)

#转换值到指标，为避免潜在的错误，新建一个DataFrame接收转换后的指标矩阵
data_new = pd.DataFrame()

for i in range(len(result_)):
    index1 = data[keys[i]] < result_.iloc[i, 1]
    index2 = (result_.iloc[i, 1] < data[keys[i]]) & (data[keys[i]] < result_.iloc[i, 2])
    index3 = (result_.iloc[i, 2] < data[keys[i]]) & (data[keys[i]] < result_.iloc[i, 3])
    index4 = (result_.iloc[i, 3] < data[keys[i]])
    
    data_n = index1.copy() #仅为生成data_n
    data_n[index1 == True] = strabc.iloc[i, 0]
    data_n[index2 == True] = strabc.iloc[i, 1]
    data_n[index3 == True] = strabc.iloc[i, 2]
    data_n[index4 == True] = strabc.iloc[i, 3]
    
    data_new = pd.concat([data_new, data_n], axis=1)
   
data_model = pd.concat([data_new, data['TNM分期']], axis=1)
print(data_model)

import time
from apriori import *

#inputfile = 'F:\\spyder\\datamining\\chapter8\\demo\\data\\apriori.txt'
#data = pd.read_csv(inputfile, header=None, dtype=object)
 
start = time.clock()
print(u'转换数据至0-1矩阵...')

#转换为0-1矩阵的过度函数，即将标签数据转换为1
ct = lambda x : pd.Series(1, index=x[pd.notnull(x)])
b = map(ct, data_model.values)
print (b)
c = list(b)
print(c)
data_model = pd.DataFrame(c).fillna(0)
print(data_model)
end = time.clock()
print(u'转换完毕，用时：%0.2f秒' % (end-start))
del b

support = 0.06 #最小支持度
confidence = 0.75 #最小置信度
ms = '---' 
find_rule(data_model, support, confidence, ms)

































        
        
        
        
        
        
        
        
        
        
        
        
        
        