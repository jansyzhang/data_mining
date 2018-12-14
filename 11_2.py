# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 11:17:38 2018

"""

import pandas as pd

discfile = "F:\spyder\datamining\chapter11\demo\data\discdata_processed.xls"

data = pd.read_excel(discfile)
data = data.iloc[:len(data)-5]

'''--------------------平稳性检测--------------------------------'''
from statsmodels.tsa.stattools import adfuller as ADF

diff = 0;
adf = ADF(data['CWXT_DB:184:D:\\'])
#adf[1]为p值，p值小于0.05认为是平稳的
while adf[1] >= 0.05:
    diff = diff + 1
    adf = ADF(data['CWXT_DB:184:D:\\'].diff(diff).dropna()) #dropna()删除缺失的数据

print(u'原始序列经过%s阶差分后归于平稳，p值为%s' %(diff, adf[1]))

'''--------------------白噪声检测---------------------------------'''
#经过平稳性检验，确实差分为1
from statsmodels.stats.diagnostic import acorr_ljungbox

#检验原始序列
[[lb], [p]] = acorr_ljungbox(data['CWXT_DB:184:D:\\'], lags=1)
if p < 0.05:
    print(u'原始序列为非白噪声序列，对应的p值为：%s' %p)
else:
    print(u'原始序列为白噪声序列，对应的p值为：%s' %p)
#检验差分序列
[[lb], [p]] = acorr_ljungbox(data['CWXT_DB:184:D:\\'].diff().dropna(), lags=1)
if p < 0.05:
    print(u'一阶差分序列为非白噪声序列，对应的p值为：%s' %p)
else:
    print(u'一阶差分序列为白噪声序列，对应的p值为：%s' %p)    

'''--------------------参数估计------------------------------------'''
from statsmodels.tsa.arima_model import ARIMA
xdata = data['CWXT_DB:184:D:\\']
#定阶
pmax = int(len(xdata)/10) #一般阶数不超过length/10
qmax = int(len(xdata)/10) #一般结束不超过length/10

bic_matrix = [] #bic矩阵
for p in range(pmax+1):
    tmp = []          
    for q in range(qmax+1):
        #存在部分报错，所以用try来跳过报错
        try:
            tmp.append(ARIMA(xdata, (p, 0, q)).fit().bic)
        except:
            tmp.append(None)
    bic_matrix.append(tmp)

bic_matrix = pd.DataFrame(bic_matrix) #从中可以找到最小值
p, q = bic_matrix.stack().idxmin() #先用stack展平，然后用idxmin找出最小值位置
print(u'BIC最小的p值和q值为：%s, %s' %(p, q))

'''------------------------模型检验----------------------------------'''
lagnum = 12 #残差的延迟个数
arima = ARIMA(xdata, (1, 0, 0)).fit() #建立训练模型
xdata_pred = arima.predict() #预测
pred_error = (xdata_pred - xdata).dropna() #计算残差
lb, p = acorr_ljungbox(data['CWXT_DB:184:D:\\'].diff().dropna(), lags=1)
h = (p < 0.05).sum() #p值小于0.05，认为是非白噪声
if h > 0:
    print(u'模型不符合白噪声检验')
else:
    print(u'模型符合白噪声检验')    

       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        