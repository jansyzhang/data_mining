# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 08:58:30 2018

"""

import pandas as pd
from random import shuffle

datafile = 'F:\\spyder\\datamining\\chapter6\\demo\\data\\model.xls'
data = pd.read_excel(datafile)
data = data.values
shuffle(data)   #随机打乱顺序

p = 0.8
train = data[:int(len(data)*p),:] #前80%为训练数据
test = data[int(len(data)*p):,:] #后20%为训练数据

from keras.models import Sequential
from keras.layers.core import Dense, Activation

netfile = 'F:\spyder\datamining\chapter6\model.h5'
net = Sequential()
net.add(Dense(10,input_dim=3))
net.add(Activation('relu'))
net.add(Dense(1,input_dim=10))
net.add(Activation('sigmoid'))
net.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

net.fit(train[:,:3], train[:,3], batch_size=10, epochs=10)
#net.save(netfile)
predict_result = net.predict_classes(train[:,:3]).reshape(len(train))

from cm_plot import *
cm_plot(train[:,3], predict_result).show()

from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt #导入作图库

predict_result2 = net.predict(train[:,:3]).reshape(len(train))
fpr, tpr, thresholds = roc_curve(train[:,3], predict_result2, pos_label=1)
#predict_result2 = net.predict(test[:,:3]).reshape(len(test))
#fpr, tpr, thresholds = roc_curve(test[:,3], predict_result2, pos_label=1)
plt.plot(fpr, tpr, linewidth=2, label='ROC of LM')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.ylim(0,1.05) #边界范围
plt.ylim(0,1.05)
plt.legend(loc=4) #图例
plt.show()































