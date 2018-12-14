# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 20:20:20 2018

"""
import pandas as pd

'''inputfile = 'F:\spyder\datamining\chapter15\demo\data\huizong.csv'
outputfile = ''
data = pd.read_csv(inputfile, encoding='utf-8')
data = data[[u'评论']][data[u'品牌'] == u'美的']
#data.to_csv('meidi_jd.txt', index=False, header=False)'''

#---------------------------删除重复评论------------------------------
inputfile = 'F:\spyder\datamining\chapter15\meidi_jd.txt'
data = pd.read_csv(inputfile, encoding='utf-8', header=None)
l1 = len(data)
data = pd.DataFrame(data[0].unique())
l2 = len(data)
print("%s %s" %(l1, l2))
data.to_csv('meidi_jd_process_1.txt', index=False, header=False, encoding='utf-8')