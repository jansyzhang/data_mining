# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 10:20:58 2018


"""

import pandas as pd



#奖励逻辑回归模型
'''filename = 'F:\\spyder\\datamining\\chapter5\\demo\\data\\bankloan.xls'
data = pd.read_excel(filename)
x = data.iloc[:,:8].values
y = data.iloc[:,8].values

from sklearn.linear_model import LogisticRegression as LR
from sklearn.linear_model import RandomizedLogisticRegression as RLR
#使用稳定性选择方法中的随机逻辑回归进行特征筛选。
rlr = RLR()#建立随机逻辑回归模型，筛选变量
rlr.fit(x,y)#训练模型
rlr.get_support()#获取特征筛选结果，也可以通过。score_方法获取各个特征的分数
print(u'通过随机逻辑回归模型筛选特征结束')
#join() 表示连接，使用逗号，括号内必须是一个对象。如果有多个就编程元组，或是列表
print(u'有效特征为：%s'%','.join(data.columns[:8][rlr.get_support()]))
x = data[data.columns[:8][rlr.get_support()].values]#筛选好特征

print(x)
lr = LR()#建立逻辑货柜模型
lr.fit(x,y)
print(u'逻辑回归模型训练结束')
print(u'模型的平均正确率为：%s'% lr.score(x,y))#给出模型的平均正确率。'''

#建立基于信息熵的决策树模型
filename = 'F:\\spyder\\datamining\\chapter5\\demo\\data\\sales_data.xls'
data = pd.read_excel(filename, index_col = u'序号')#导入数据
#数据是类别标签，要将它转化为数据
#用1表示好，是，高，用-1表示坏，否，低
data[data == u'好'] = 1
data[data == u'是'] = 1
data[data == u'高'] = 1
data[data != 1] = -1   
x = data.iloc[:,:3].values.astype(int)
y = data.iloc[:,3].values.astype(int)

'''from sklearn.tree import DecisionTreeClassifier as DTC
dtc = DTC(criterion = 'entropy') #建立决策树模型，基于信息熵
dtc.fit(x,y)
#导入相关函数，可视化决策树
#导出的相关结果是一个dot文件，需要安装Graphviz才能将它转换为pdf或者png
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO
with open("tree.dot", 'w') as f:
    f = export_graphviz(dtc, feature_names = x.columns, out_file = f)'''

import os
os.environ['KERAS_BACKEND']='tensorflow'
from keras.models import Sequential
from keras.layers.core import Dense, Activation

model = Sequential() #建立模型
model.add(Dense(3,10))
model.add(Activation('relu'))
model.add(Dense(10,1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', class_model='binary')
model.fit(x, y, batch_size=10, epochs = 1000)
yp = model.predict_classes(x).reshape(len(y))


from sklearn.metrics import confusion_matrix #导入混淆矩阵函数
import matplotlib.pyplot as plt #导入作图库
cm = confusion_matrix(y, yp) #混淆矩阵 
plt.matshow(cm, cmap=plt.cm.Greens) #画混淆矩阵图，配色风格使用cm.Greens，更多风格请参考官网。
plt.colorbar() #颜色标签
for x in range(len(cm)): #数据标签
    for y in range(len(cm)):
        plt.annotate(cm[x,y], xy=(x, y), horizontalalignment='center', verticalalignment='center') 
plt.ylabel('True label') #坐标轴标签
plt.xlabel('Predicted label') #坐标轴标签
plt.show()

















                 