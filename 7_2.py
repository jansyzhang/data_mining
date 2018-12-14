# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 20:40:00 2018

"""

import pandas as pd
from sklearn.cluster import KMeans 

inputfile = 'F:\\spyder\\datamining\\chapter7\\zscoreddata.xls'
k = 5

data = pd.read_excel(inputfile)

kmodel = KMeans(n_clusters=k)
kmodel.fit(data)

r1 = pd.Series(kmodel.labels_).value_counts()
r2 = pd.DataFrame(kmodel.cluster_centers_)
r = pd.concat([r2,r1], axis=1)
r.columns = list(data.columns) + ['类别数目']
print(r)

'''r = pd.concat([data, pd.Series(kmodel.labels_, index=data.index)], axis=1)
r.columns = list(data.columns) + ['聚类类别']
print(kmodel.cluster_centers_)
print(kmodel.labels_)'''
outputfile = "F:\\spyder\\datamining\\chapter7\\result.xls"
r.to_excel(outputfile)














