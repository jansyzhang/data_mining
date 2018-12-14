# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:43:01 2018

"""
import time
from random import shuffle
import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine

'''------------------sql connection-----------------'''
pymysql.install_as_MySQLdb()
engine = create_engine('mysql://root:1995912@127.0.0.1:3306/test?charset=utf8')
data = pd.read_sql('hunyinformodel', engine)
print(data.head()) #打印head中的头5行

'''
基于物品的协同过滤推荐
'''
#定义协同推荐函数
def Jaccard(a, b):
    #计算物品相似度，仅对0-1矩阵有效
    return 1.0 * (a * b).sum() / (a + b - a * b).sum()

class Recommender():
    sim = None
    def similarity(self, x, distance):
        #计算相似度举证
        y = np.ones((len(x), len(x)))
        for i in range(len(x)):
            for j in range(len(x)):
                y[i,j] = distance(x[i],x[j])
        return y
    
    def fit(self, x, distance=Jaccard):
        #生成物品的相似度矩阵
        self.sim = self.similarity(x, distance)
        return self.sim
    
    def recommend(self, a):
        #计算用户的兴趣度
        #np.dot计算点积
        return np.dot(self.sim, a) * (1-a)
    
'''
将数据转化为0-1矩阵
'''
start0 = time.clock()
data.sort_values(by=['userID', 'fullURL'], ascending=[True, True], inplace=True)
realIP = data['userID'].value_counts().index
realIP = np.sort(realIP)
fullURL = data['fullURL'].value_counts().index
fullURL = np.sort(fullURL)

D = pd.DataFrame([], index=realIP, columns=fullURL)
for i in range(len(data)):
    a = data.iloc[i,0] #用户名
    b = data.iloc[i,1] #网址
    D.loc[a,b] = 1
D.fillna(0, inplace=True)
end0 = time.clock()
usetime0 = end0 - start0
print ('转成0、1矩阵所花费的时间为'+ str(usetime0) +'s!')

'''
交叉验证方法验证推荐
'''
df = D.copy() 
simpler = np.random.permutation(len(df)) 
df = df.take(simpler)# 打乱数据
df = df.values
df_train = df[:int(len(df)*0.9), :].T
df_test = df[int(len(df)*0.9):, :].T

'''
建立相似矩阵，训练模型
'''             
start1 = time.clock()
r = Recommender()
sim = r.fit(df_train)
end1 = time.clock()

a = pd.DataFrame(sim)
usetime1 = end1-start1
print (u'建立相似矩阵耗时'+str(usetime1)+'s!')

'''
使用测试集进行预测
'''
result = r.recommend(df_test)
result = pd.DataFrame(result)

def collaborative_result(K, recomMatrix):
    recomMatrix.fillna(0.0, inplace=True) #将
    n = range(1, K+1)
    recommends = ['xietong' + str(y) for y in n]
    currentemp = pd.DataFrame([], index=recomMatrix.columns, columns=recommends)
    
    for i in range(len(recomMatrix.columns)):
        temp = recomMatrix.sort_values(by=recomMatrix.columns[i], ascending=False)
        k = 0
        while k < K:
            currentemp.iloc[i,k] = temp.index[k]
            if temp.iloc[k,i] == 0.0:
                currentemp.iloc[i,k:K] = np.nan
                break
            k += 1
    return currentemp

xietong_result = collaborative_result(3,result)
xietong_result.to_csv('xietong_result.csv')
        



























