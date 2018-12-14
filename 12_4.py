# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 17:47:05 2018

"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine

'''------------------sql connection-----------------'''
pymysql.install_as_MySQLdb()
engine = create_engine('mysql://root:1995912@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('cleaned_gzdata', engine, chunksize=10000)

'''for i in sql:
    d = i.copy()
    #将下划线后面部分去掉，规范为标准化网址
    d['fullURL'] = d['fullURL'].str.replace('_\d{0,2}.html', '.html')
    d = d.drop_duplicates() #删除重复记录
    d.to_sql('cleaned_gzdata', engine, index=False, if_exists='append')'''
    

