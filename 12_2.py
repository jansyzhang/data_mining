# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 10:54:17 2018

"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine

'''------------------sql connection-----------------'''
pymysql.install_as_MySQLdb()
engine = create_engine('mysql://root:1995912@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize=10000)

'''-------------------web type analysis---------------'''
#value_counts确认数据出现的频率
'''counts = [i['fullURLId'].value_counts() for i in sql] #逐块统计  
counts = pd.concat(counts).groupby(level=0).sum() #合并统计结果，把相同的统计项合并（即按index分组并求和）
counts = counts.reset_index()#重新设置index,将原来的index作为counts的一列
counts.columns = ['index', 'num'] #重新设置列名，主要是第二列，默认是0
counts['type'] = counts['index'].str.extract('(\d{3})')
print(counts)
counts_ = counts[['type', 'num']].groupby('type').sum() #按照类别合并
counts_.sort_values('num', ascending = False) #降序排列'''

'''-------------------intellectual content--------------'''
def count107(i):
    j = i[['fullURL']][i['fullURLId'].str.contains('107')].copy() #找出类别包含107的网址
    j['type'] = None #添加空例
    j['type'][j['fullURL'].str.contains('info/.+?/')] = u'知识首页'
    j['type'][j['fullURL'].str.contains('info/.+?/.+?')] = u'知识列表页'
    j['type'][j['fullURL'].str.contains('/\d+?_*\d+?\.html')] = u'知识内容页'
    return j['type'].value_counts()

counts2 = [count107(i) for i in sql]
counts2 = pd.concat(counts2).groupby(level=0).sum()
print(counts2)