# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 17:17:42 2018

"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine

'''------------------sql connection-----------------'''
pymysql.install_as_MySQLdb()
engine = create_engine('mysql://root:1995912@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata', engine, chunksize=10000)

'''-------------------data clean--------------------'''
for i in sql:
    d = i[['realIP', 'fullURL']] #只要是网址列
    d = d[d['fullURL'].str.contains('\.html')].copy()
    #保存到数据库的cleaned_gzdata表中
    d.to_sql('cleaned_gzdata', engine, index=False, if_exists='append')