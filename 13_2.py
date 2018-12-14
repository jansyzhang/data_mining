# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 11:31:52 2018

"""

import pandas as pd
inputfile = 'F:\spyder\datamining\chapter13\data_GM11.xls'
outputfile = 'revenue.xls'
modelfile = '1-net.model'

data = pd.read_excel(inputfile)
feature = ['x1', 'x2', 'x3', 'x4', 'x5', 'x7']

data_train = data.loc[range(1994, 2014)].copy()
data_mean = data_train.mean()
data_std = data_train.std()
data_train = (data_train - data_mean) / data_std #数据标准化
x_train = data_train[feature].values
y_train = data_train['y'].values
                    
from keras.models import Sequential
from keras.layers.core import Dense, Activation

model = Sequential()
model.add(Dense(output_dim=12, input_dim=6))
model.add(Activation('relu')) #用relu函数作为激活函数，能够大幅度提供准确度
model.add(Dense(output_dim=1, input_dim=12))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(x_train, y_train, nb_epoch=10000, batch_size=16)


#预测
x = ((data[feature] - data_mean[feature])/data_std[feature]).as_matrix()
data[u'y_pred'] = model.predict(x) * data_std['y'] + data_mean['y']
data.to_excel(outputfile)

import matplotlib.pyplot as plt
p = data[['y', 'y_pred']].plot(subplots=True, style=['b-o','r-*'])
plt.show()