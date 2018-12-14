import pandas as pd

def cm_plot(cm):
    import matplotlib.pyplot as plt
    plt.matshow(cm, cmap = plt.cm.Greens)
    plt.colorbar()
    for x in range(len(cm)):
        for y in range(len(cm)):
            plt.annotate(cm[x, y], xy=(x, y), horizontalalignment='center', verticalalignment='center')
    plt.ylabel('Ture label')
    plt.xlabel('Predicted label')
    
    
inputfile = 'F:\\spyder\\datamining\\chapter9\\demo\\data\\moment.csv'
outputfile1 = 'F:\\spyder\\datamining\\chapter9\\moment1.xls'
outputfile2 = 'F:\\spyder\\datamining\\chapter9\\moment2.xls'
data = pd.read_csv(inputfile, encoding = 'gbk')
data = data.values

#打乱顺序，划分训练集和测试集
from random import shuffle
shuffle(data)
data_train = data[:int(0.8*len(data)), :]
data_test = data[int(0.8*len(data)):,:]
x_train = data_train[:, 2:]*30
y_train = data_train[:, 0].astype(int)
x_test = data_test[:, 2:]*30
y_test = data_test[:, 0].astype(int)

#构建模型
from sklearn import svm
model = svm.SVC()
model.fit(x_train, y_train)

from sklearn import metrics
cm_train = metrics.confusion_matrix(y_train, model.predict(x_train))
cm_test = metrics.confusion_matrix(y_test, model.predict(x_test))
cm_plot(cm_train)
cm_plot(cm_test)

#保存结果
pd.DataFrame(cm_train, index=range(1,4), columns=range(1, 4)).to_excel(outputfile1)
pd.DataFrame(cm_test, index=range(1,5), columns=range(1, 5)).to_excel(outputfile2)

