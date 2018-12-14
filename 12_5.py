# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 09:09:26 2018

"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine

'''------------------sql connection-----------------'''
pymysql.install_as_MySQLdb()
engine = create_engine('mysql://root:1995912@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('changed_1', engine, chunksize=10000)

'''------------------data cleaning 1---------------'''
#对网址进行操作（只要.html结尾的&截取问号左边的值&只要包含主网址（lawtime）的&网址中间没有midques_的）
'''for i in sql:
    d = i[['realIP', 'fullURL', 'pageTitle', 'userID', 'timestamp_format']].copy()
    d['fullURL'] = d['fullURL'].str.replace('\?.*', '')
    d = d[(d['fullURL'].str.contains('\.html')) & (d['fullURL'].str.contains('lawtime')) & (d['fullURL'].str.contains('midques_') == False)]
    d.to_sql('cleaned_one', engine, index=False, if_exists='append') #index表示将dataframe的索引是否写入数据表中'''
    
'''------------------data cleaning 2----------------'''
'''for i in sql:
    d = i[['realIP', 'fullURL', 'pageTitle', 'userID', 'timestamp_format']]
    d['pageTitle'].fillna(u'空', inplace=True)
    d = d[(d['pageTitle'].str.contains(u'快车-律师助手') == False) &\
          (d['pageTitle'].str.contains(u'咨询发布成功') == False) &\
          (d['pageTitle'].str.contains(u'免费发布法律咨询') == False) &\
          (d['pageTitle'].str.contains(u'快车-律师助手') == False) &\
          (d['pageTitle'].str.contains(u'法律快搜') == False)].copy()
    d.to_sql('cleaned_two', engine, index=False, if_exists='append')'''
    
'''-----------------data cleaning 3------------------'''
'''def dropduplicate(i):
    j = i[['realIP', 'fullURL', 'pageTitle', 'userID', 'timestamp_format']].copy()
    return j

count6 = [dropduplicate(i) for i in sql]
count6 = pd.concat(count6)
count7 = count6.drop_duplicates(['fullURL', 'userID', 'timestamp_format']) #一定要进行二次删除重复，因为不同的块中具有重复值
d.to_sql('cleaned_three', engine, index=False, if_exists='append')'''

'''-----------------data conversion------------------'''
'''l0 = 0 
l1 = 0
l2 = 0
for i in sql:
    d = i.copy()
    temp0 = len(d)
    l0 += temp0
    #获取类似于http://www.lawtime.cn***/2007020619634_2.html格式的记录的个数
    x1 = d[d['fullURL'].str.contains('_\d{0,2}.html')]
    temp1 = len(x1)
    l1 += temp1
    #获取类似于http://www.lawtime.cn***/29_1_p3.html格式的记录的个数
    x2 = d[d['fullURL'].str.contains('_\d{0,2}_\w{0,2}.html')]
    temp2 = len(x2)
    l2 += temp2
    
    x1.to_sql('l1', engine, index=False, if_exists = 'append') # 保存
    x2.to_sql('l2', engine, index=False, if_exists = 'append') # 保存

print(l0, l1, l2)'''
'''for i in sql:
    d = i.copy()
    d['fillURL'] = d['fullURL'].str.replace('_\d{0,2}_\w{0,2}.html','.html')
    d['fillURL'] = d['fullURL'].str.replace('_\d{0,2}.html','.html')
    d = d.drop_duplicates(['fullURL','userID']) #删除重复记录(删除有相同网址和相同用户ID的)【不完整】因为不同的数据块中依然有重复数
    d.to_sql('changed_1', engine, index=False, if_exists = 'append')'''
    
def dropduplicate(i): 
    j = i[['realIP','fullURL','pageTitle','userID','timestamp_format']].copy()
    return j

counts1 = [dropduplicate(i) for i in sql]
counts1 = pd.concat(counts1)
a = counts1.drop_duplicates(['fullURL','userID'])
a.to_sql('changed_2', engine, index=False, if_exists = 'append')

        