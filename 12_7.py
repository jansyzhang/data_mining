# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:40:28 2018

"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine

'''------------------sql connection-----------------'''
pymysql.install_as_MySQLdb()
engine = create_engine('mysql://root:1995912@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('changed_2', engine, chunksize=10000)

l1 = 0
l2 = 0 
for i in sql:
    zixun = i[['userID','fullURL']][i['fullURL'].str.contains('(ask)|(askzt)')].copy()
    l1 = len(zixun) + l1
    hunyin = i[['userID','fullURL']][i['fullURL'].str.contains('hunyin')].copy()    
    l2 = len(hunyin) + l2
    zixun.to_sql('zixunformodel', engine, index=False,if_exists = 'append')
    hunyin.to_sql('hunyinformodel', engine, index=False,if_exists = 'append')
