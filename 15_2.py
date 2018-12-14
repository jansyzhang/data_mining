# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 17:47:06 2018

"""

import pandas as pd
import jieba

#---------------------------删除前缀评分代码------------------------------------
'''
inputfile1 = 'F:\\spyder\\datamining\\chapter15\\demo\\data\\meidi_jd_process_end_负面情感结果.txt'
inputfile2 = 'F:\\spyder\\datamining\\chapter15\\demo\\data\\meidi_jd_process_end_正面情感结果.txt'

#输入文件的路径中包含中文时，需要添加属性 engine='python'
data1 = pd.read_csv(inputfile1, encoding='utf-8', header=None, engine='python')
data2 = pd.read_csv(inputfile2, encoding='utf-8', header=None, engine='python')
#使用正则表达式修改数据
data1 = pd.DataFrame(data1[0].str.replace('.*?\d+?\\t ',''))
data2 = pd.DataFrame(data2[0].str.replace('.*?\d+?\\t ',''))

data1.to_csv('meidi_jd_neg', index=False, header=False, encoding='utf-8')
data2.to_csv('meidi_jd_pos', index=False, header=False, encoding='utf-8')
'''
#----------------------------对文档进行分词-------------------------------------
'''
inputfile1 = 'meidi_jd_neg.txt'
inputfile2 = 'meidi_jd_pos.txt'

data1 = pd.read_csv(inputfile1, encoding='utf-8', header=None)
data2 = pd.read_csv(inputfile2, encoding='utf-8', header=None)

mycut = lambda s : ''.join(jieba.cut(s)) #自定义简单的分词函数，以空格（” “）为分隔符将字符串进行连接
data1 = data1[0].apply(mycut)
data2 = data2[0].apply(mycut)

data1.to_csv('meidi_jd_neg_cut.txt', index=False, header=False, encoding='utf-8')
data2.to_csv('meidi_jd_pos_cut.txt', index=False, header=False, encoding='utf-8')
'''  
#----------------------------LDA模型-------------------------------------------
negfile = 'meidi_jd_neg_cut.txt'
posfile = 'meidi_jd_pos_cut.txt'
stoplist = 'stoplist.txt'

neg = pd.read_csv(negfile, encoding='utf-8', header=None, engine='python')
pos = pd.read_csv(posfile, encoding='utf-8', header=None, engine='python')
#sep设置分割词，由于csv默认以半角逗号为分割词，而改词恰好在停词表中，因此会导致读取出错
#所以解决办法是手动设置一个不存在的分割词。
stop = pd.read_csv(stoplist, encoding='utf-8', header=None, sep='tipdm', engine='python')

neg[1] = neg[0].apply(lambda s : s.split(' ')) #定义一个分割函数，然后用apply广播。
neg[2] = neg[1].apply(lambda x : [i for i in x if i not in stop]) #判断是否是停用词
pos[1] = pos[0].apply(lambda s : s.split(' '))
pos[2] = pos[1].apply(lambda x : [i for i in x if i not in stop]) 

from gensim import corpora, models
#corpora是gensim中的一个基本概念，是文档集的表现形式，也是后续进一步处理的基础。

#负面主题分析
# corpora.Dictionary可以理解为python中的字典对象, 其Key是字典中的词，其Val是词对应的唯一数值型ID
neg_dict = corpora.Dictionary(neg[2]) #建立词典
#doc2bow建立BOW词袋模型
neg_corpus = [neg_dict.doc2bow(i) for i in neg[2]] #建立语料库
neg_lda = models.LdaModel(neg_corpus, num_topics=3, id2word=neg_dict) #LDA模型训练
for i in range(3):
    print(neg_lda.print_topic(i)) #输入
print("----------------------------------------------------------------------")                       
#正面主题分析
pos_dict = corpora.Dictionary(pos[2]) #建立词典
pos_corpus = [pos_dict.doc2bow(i) for i in pos[2]] #建立语料库
pos_lda = models.LdaModel(pos_corpus, num_topics=3, id2word=pos_dict) #LDA模型训练
for i in range(3):
    print(pos_lda.print_topic(i)) #输入                         
                          
                          
                          
                          
                          
                          
                          
                          
                          
                          
                          
                          
                          
                          
                          