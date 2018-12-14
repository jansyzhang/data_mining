# -*- coding: utf-8 -*-

import matplotlib.image as mpimg
import numpy as np
import os
import pandas as pd

#计算颜色矩特征
def img2vector(filename):
	returnvect = np.zeros((1, 9))
	fr = mpimg.imread(filename)
	l_max = fr.shape[0]//2+50
	l_min = fr.shape[0]//2-50
	w_max = fr.shape[0]//2+50
	w_min = fr.shape[0]//2-50
	water = fr[l_min:l_max, w_min:w_max, :].reshape(1, 10000, 3)
	for i in range(3):
		this = water[:,:,i]/255
		returnvect[0,i] = np.mean(this)#一阶矩
		returnvect[0,3+i]=np.sqrt(np.mean(np.square(this-returnvect[0,i])))#二阶矩
		returnvect[0,6+i]=np.cbrt(np.mean(np.power(this-returnvect[0,i], 3)))#三阶矩
	return returnvect 

#计算每个图片的特征
trainfilelist=os.listdir('F:\\spyder\\datamining\\chapter9\\test\\data\\images')#读取目录下文件列表
m=len(trainfilelist)#计算文件数目
labels=np.zeros((1,m))
train=np.zeros((1,m))
trainingMat=np.zeros((m,9))

for i in range(m):
	filenamestr=trainfilelist[i] #获取当前文件名，例1_1.jpg
	filestr=filenamestr.split('.')[0]  #按照.划分，取前一部分
	classnumstr=int(filestr.split('_')[0])#按照_划分，后一部分为该类图片中的序列
	picture_num = int(filestr.split('_')[1])
	labels[0,i]=classnumstr               #前一部分为该图片的标签
	train[0,i]=picture_num
	trainingMat[i,:]=img2vector('F:\\spyder\\datamining\\chapter9\\test\\data\\images\\%s' % filenamestr) #构成数组
	
#保存
d=np.concatenate((labels.T,train.T,trainingMat),axis=1)#连接数组
dataframe=pd.DataFrame(d,columns=['label','num','R_1','G_1','B_2','R_2','G_2','B_2','R_3','G_3','B_3'])
dataframe.to_csv('F:\\spyder\\datamining\\chapter9\\moment.csv',header=None,index=None)#保存文件	
		