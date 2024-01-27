# -*- codeing = utf-8 -*-
# @Time : 2022/12/3 11:32
# @Author : WxY
# @File : Baidu情感分析(知乎).py
# @Software : PyCharm
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image

# 获取文件夹路径的函数
def getfolderPath():
    root=tk.Tk()
    root.withdraw()
    folderPath= filedialog.askdirectory()
    print('文件夹路径:',folderPath)
    return folderPath

# 获取文件夹指定后缀的文件
def getAllFilePath(FolderPath):
    listdir = os.listdir(FolderPath)
    for file in listdir:
        if '.csv' in file and 'ZhiHu' in file:
            allfile_zh = FolderPath + '/' + file
    return allfile_zh

# 获取文件夹路径
dataFolderPath = getfolderPath()
DataPath_zh = getAllFilePath(dataFolderPath)

AllData_df = pd.DataFrame()
AllData_df= pd.read_csv(DataPath_zh,encoding='utf-8')
AllData_df = AllData_df.reset_index(drop=True)
AllData_df.info()
print(AllData_df.情感方向.value_counts(),'\n')

data1=AllData_df[AllData_df.情感方向 == '正向'].reset_index(drop = True)
print('正向评论:\n',data1)
data1.to_csv("D:/WxYown/数据分析中心/舆情结果/2023年8月/month202308_pos_zh.csv",encoding="utf_8_sig")

data2=AllData_df[AllData_df.情感方向 == '负向'].reset_index(drop = True)
print('负向评论:\n',data2)
data2.to_csv("D:/WxYown/数据分析中心/舆情结果/2023年8月/month202308_neg_zh.csv",encoding="utf_8_sig")

data3=AllData_df[AllData_df.情感方向 == '中性'].reset_index(drop = True)
print('中性评论:\n',data3)
data3.to_csv("D:/WxYown/数据分析中心/舆情结果/2023年8月/month202308_neu_zh.csv",encoding="utf_8_sig")

from matplotlib import pyplot as plt
from wordcloud import WordCloud
import jieba
import pandas as pd
import re

stopwords = set()
content = [line.strip() for line in open('D:/WxYown/数据分析中心/情感划分(不要动位置)/stopwords.txt','r').readlines()]
stopwords.update(content)
stoplist = stopwords

#正向情感
dic_list1 = [] # 字段典，装不重复的字段
freq_list1 = [] # 装重复，用于统计频数
zhmodel1 = re.compile('[\u4e00-\u9fa5]+')  #检查中文
for sentence in data1.answerRaw.values:
    sentence_depart = jieba.lcut(sentence,HMM=False)
    for word in sentence_depart:
        if len(word) > 1:
            freq_list1.append(str(word))
        if word not in stoplist and word not in dic_list1 and zhmodel1.search(word) and len(word) >1 :
            dic_list1.append(str(word))
freqDf1 = pd.Series(freq_list1).value_counts()

#负向情感
dic_list2 = [] # 字段典，装不重复的字段
freq_list2 = [] # 装重复，用于统计频数
zhmodel2 = re.compile('[\u4e00-\u9fa5]+')  #检查中文
for sentence in data2.answerRaw.values:
    sentence_depart = jieba.lcut(sentence,HMM=False)
    for word in sentence_depart:
        if len(word) >1:
            freq_list2.append(str(word))
        if word not in stoplist and word not in dic_list2 and zhmodel2.search(word) and len(word) >1 :
            dic_list2.append(str(word))
freqDf2 = pd.Series(freq_list2).value_counts()

#评论词云图
dropwords = [line.strip() for line in open('dropwords.txt',encoding="utf_8_sig").readlines()]

maskph=np.array(Image.open('ciyun.png'))
#积极评论
freqDf1 = freqDf1[~freqDf1.index.isin(dropwords)]
# 设置参数，创建WordCloud对象
w1 = WordCloud(font_path="msyh.ttc", mask=maskph, collocations=False, background_color='white',max_words=130)
# 根据文本数据生成词云
w1.fit_words(freqDf1)
plt.imshow(w1)
plt.axis("off")
# 保存词云文件
w1.to_file('知乎积极评论词云2023年8月.png')

#消极评论
freqDf2 = freqDf2[~freqDf2.index.isin(dropwords)]
# 设置参数，创建WordCloud对象
w2 = WordCloud(font_path="msyh.ttc", mask=maskph, collocations=False, background_color='white',max_words=130)
# 根据文本数据生成词云
w2.fit_words(freqDf2)
plt.imshow(w2)
plt.axis("off")
# 保存词云文件
w2.to_file('知乎消极评论词云2023年8月.png')


