# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 11:39:49 2018


"""

import pandas as pd

#参数初始化
discfile = 'F:\\spyder\\datamining\\chapter5\\demo\\data\\arima_data.xls'
forecastnum = 5

#读取数据，指定日期为指标，pandas自动将日期列识别为Datetime格式
data = pd.read_excel(discfile, index_col = u'日期')

#时序图
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']#用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False#用来正常显示正负号
data.plot()
plt.show()

#自相关图
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(data).show()

#平稳性检测
from statsmodels.tsa.stattools import adfuller as ADF
print(u'原始序列的ADF检验结果为：', ADF(data[u'销量']))
#返回值依次为adf, pvalue, usedlag, nobs, critical values, icbest, regresults, resstore

#差分后的结果
D_data = data.diff().dropna()
D_data.columns = [u'销量差分']
D_data.plot()#时序图
plt.show()
plot_acf(D_data).show()#自相关图

from statsmodels.graphics.tsaplots import plot_pacf
plot_pacf(D_data).show()#偏自相关图
print(u'差分序列的ADF检验结果为：', ADF(D_data[u'销量差分']))#平稳性检测

#白噪声检验
from statsmodels.stats.diagnostic import acorr_ljungbox
print(u'差分序列的白噪声检验结果为：', acorr_ljungbox(D_data, lags=1))#返回统计量和p值

#定阶
from statsmodels.tsa.arima_model import ARIMA
pmax = int(len(D_data)/10)#一般阶数不超过length/10
qmax = int(len(D_data)/10)  
bic_matrix = []#bic矩阵
for p in range(pmax+1):
    tmp = []
    for q in range(qmax+1):
        try:
            tmp.append(ARIMA(data, (p,1,q)).fit().bic)
        except:
            tmp.append(None)
    bic_matrix.append(tmp)
    
bic_matrix = pd.DataFrame(bic_matrix)
p, q = bic_matrix.stack().idxmin()#先用stack展平，然后用idxmin找出最小的位置
print(u'BIC最小的p值和q值为：%s, %s' %(p, q))
model = ARIMA(data, (p,1,q)).fit()#建立ARIMA(0,1,1)模型
print(model.summary2())#给出一份报告模型报告
print(model.forecast(5))#做5天的预测，返回预测结果，标准误差，置信区间


































