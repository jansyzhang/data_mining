# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 21:24:39 2018

"""

import pandas as pd
from sqlalchemy import create_engine

import pymysql
pymysql.install_as_MySQLdb()


'''
用create_engine建立连接，连接的格式为“数据库+程序名+账号：密码@地址：端口/数据库名？最后指定编码为utf8”
all_gzdata是表名， engine是连接数据库引擎， chunksize指定每次读取1万条记录
第一步连接数据库并读取的过程在每一步统计时都要重新运行一遍，否则会报错sql（容器）没有定义。
'''

engine = create_engine('mysql://root:1995912@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize=10000)

#----------------------------step1 statistics--------------------------------------------------
'''counts = [ i['fullURLId'].value_counts() for i in sql] #逐块统计
print(counts)
counts = pd.concat(counts).groupby(level=0).sum() #合并统计结果，把相同的统计项合并（即按index分组并求和）
counts = counts.reset_index() #重新设置index，将原来的index作为counts的一列。
counts.columns = ['index', 'num'] #重新设置列名，主要是第二列，默认为0
counts['type'] = counts['index'].str.extract('(\d{3})') #提取前三个数字作为类别id
counts_ = counts[['type', 'num']].groupby('type').sum() #按类别合并
counts_.sort_values('num', ascending = False) #降序排列'''

#--------------------------- step2 statistics------------------------------------------------
#统计107类别的情况
def count107(i): #自定义统计函数
  j = i[['fullURL']][i['fullURLId'].str.contains('107')].copy() #找出类别包含107的网址
  j['type'] = None #添加空列
  j['type'][j['fullURL'].str.contains('info/.+?/')] = u'知识首页'
  j['type'][j['fullURL'].str.contains('info/.+?/.+?')] = u'知识列表页'
  j['type'][j['fullURL'].str.contains('/\d+?_*\d+?\.html')] = u'知识内容页'
  return j['type'].value_counts()

counts2 = [count107(i) for i in sql] #逐块统计
counts2 = pd.concat(counts2).groupby(level=0).sum() #合并统计结果
print(counts2)

#--------------------------step3 statistics-------------------------------------------------
#统计点击次数
'''c = [i['realIP'].value_counts() for i in sql] #分块统计各个IP的出现次数
count3 = pd.concat(c).groupby(level = 0).sum() #合并统计结果，level=0表示按index分组
count3 = pd.DataFrame(count3) #Series转为DataFrame
count3[1] = 1 #添加一列，全为1
count3.groupby(0).sum() #统计各个“不同的点击次数”分别出现的次数
print(count3.groupby(0).sum())'''
