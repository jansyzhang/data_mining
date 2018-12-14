# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 09:55:23 2018

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

from sklearn.tree import DecisionTreeClassifier

treefile = 'F:\\spyder\\datamining\\chapter6\\tree.pkl'
tree = DecisionTreeClassifier()
tree.fit(train[:,:3], train[:,3])

#保存模型
from sklearn.externals import joblib
joblib.dump(tree, treefile)


from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt #导入作图库

predict_result2 = tree.predict_proba(test[:,:3])[:,1]
fpr, tpr, thresholds = roc_curve(test[:,3], predict_result2, pos_label=1)
plt.plot(fpr, tpr, linewidth=2, label='ROC of C')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.ylim(0,1.05) #边界范围
plt.ylim(0,1.05)
plt.legend(loc=4) #图例
plt.show()