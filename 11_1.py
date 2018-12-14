# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 19:20:23 2018

"""

import pandas as pd

discfile = 'F:\spyder\datamining\chapter11\demo\data\discdata.xls'
transformeddata = 'F:\spyder\datamining\chapter11\discdata.xls'

data = pd.read_excel(discfile)
data = data[data['TARGET_ID'] == 184].copy()

data_group = data.groupby('COLLECTTIME')
def attr_trans(x):
    result = pd.Series(index=['SYS_NAME', 'CWXT_DB:184:C:\\', 'CWXT_DB:184:D:\\', 'COLLECTTIME'])
    result['SYS_NAME'] = x['SYS_NAME'].iloc[0]
    result['COLLECTTIME'] = x['COLLECTTIME'].iloc[0]
    result['CWXT_DB:184:C:\\'] = x['VALUE'].iloc[0]
    result['CWXT_DB:184:D:\\'] = x['VALUE'].iloc[1]
    return result

data_processed = data_group.apply(attr_trans) #逐组处理
data_processed.to_excel(transformeddata, index=False)