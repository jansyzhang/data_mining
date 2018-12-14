# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 11:54:14 2018

"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine
import numpy as np

'''------------------sql connection-----------------'''
pymysql.install_as_MySQLdb()
engine = create_engine('mysql://root:1995912@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('changed_2', engine, chunksize=10000)

def count_knowledge(i):
    j = i[['fullURL']].copy()
    j['type'] = 'else'
    j['type'][j['fullURL'].str.contains('(info)|(faguizt)')] = 'zhishi'
    j['type'][j['fullURL'].str.contains('(ask)|(askzt)')] = 'zixun'
    return j 

counts2 = [count_knowledge(i) for i in sql]
counts2 = pd.concat(counts2)
a = counts2['type'].value_counts()
b = pd.DataFrame(a)
b.columns = ['num']
b.index.name = 'type'
b['per'] = b['num'] / b['num'].sum() * 100
print(b)

c = counts2[counts2['type'] == 'zhishi']
d = c[c['fullURL'].str.contains('info')]
d['iszsk'] = 'else'
d['iszsk'][d['fullURL'].str.contains('info')] = 'infoelsezsk'
d['iszsk'][d['fullURL'].str.contains('zhishiku')] = 'zsk'
print(d['iszsk'].value_counts())

import re
# 对于http://www.lawtime.cn/info/jiaotong/jtsgcl/2011070996791.html类型的网址进行这样匹配,获取二级类别名称"jiaotong"
pattern = re.compile('/info/(.*?)/',re.S)
e = d[d['iszsk'] == 'infoelsezsk']
for i in range(len(e)):
    e.iloc[i,2] = re.findall(pattern, e.iloc[i,0])[0]
print (e.head())
 
# 对于http://www.lawtime.cn/zhishiku/laodong/info/***.html类型的网址进行这样匹配,获取二级类别名称"laodong"
# 由于还有一类是http://www.lawtime.cn/zhishiku/laodong/***.html，所以使用'zhishiku/(.*?)/'进行匹配
pattern1 = re.compile('zhishiku/(.*?)/',re.S)
f = d[d['iszsk'] == 'zsk']
for i in range(len(f)):
#     print i 
    f.iloc[i,2] = re.findall(pattern1, f.iloc[i,0])[0]
print (f.head())

e.columns = ['fullURL', 'type1', 'type2']
f.columns = ['fullURL', 'type1', 'type2']
g = pd.concat([e,f])
h = g['type2'].value_counts()
detailtypes = h.index
for i in range(len(detailtypes)):
    x = g[g['type2'] == h.index[i]]
    '''x.to_sql(h.index[i], engine, index=False, if_exists='append')'''

q = e.copy()
q['type3'] = np.nan
resultype3 = pd.DataFrame([],columns=q.columns)
for i in range(len(h.index)):
    pattern2 = re.compile('/info/'+h.index[i]+'/(.*?)/',re.S)
    current = q[q['type2'] == h.index[i]]
    print (current.head())
    for j in range(len(current)):
        findresult = re.findall(pattern2, current.iloc[j,0])
        if findresult == []: # 若匹配结果是空，则将空值进行赋值给三级类别
            current.iloc[j,3] = np.nan
        else:
            current.iloc[j,3] = findresult[0]
    resultype3 = pd.concat([resultype3,current])# 将处理后的数据拼接
resultype3.head()

resultype3.set_index('fullURL',inplace=True)
print(resultype3.head(10))

j = resultype3[resultype3['type2'] == 'hunyin']['type3'].value_counts()
print (len(j)) # 145
j.head()

Type3nums = resultype3.pivot_table(index = ['type2','type3'], aggfunc = 'count')
# 方式2: Type3nums = resultype3.groupby([resultype3['type2'],resultype3['type3']]).count()
r = Type3nums.reset_index().sort_values(by=['type2','type1'],ascending=[True,False])
r.set_index(['type2','type3'],inplace = True)
#保存的表名命名格式为“2_2_k此表功能名称”，此表表示生成的第1张表格，功能为Type3nums：得出所有三级类别
r.to_excel('2_2_3Type3nums.xlsx')




