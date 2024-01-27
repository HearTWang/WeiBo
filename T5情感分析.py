# -*- codeing = utf-8 -*-
# @Time : 2023/7/8 15:33
# @Author : WxY
# @File : T5情感分析.py
# @Software : PyCharm

import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer, T5Config


# 获取文件夹路径的函数
def GetfolderPath():
    root=tk.Tk()
    root.withdraw()
    folderPath= filedialog.askdirectory()
    print('文件夹路径:', folderPath)
    return folderPath


# 获取文件夹指定后缀的文件
def GetAllFilePath(FolderPath):
    listdir = os.listdir(FolderPath)
    allfile = []
    for file in listdir:
        if '.csv' in file and 'ZhiHu' not in file:
            allfile.append(FolderPath + '/' + file)
    return allfile


# 情感分析-T5
def EmotionAnalysis(text_list):
    # T5-LLM导入
    model_file = 't5-chinese-784M'  # 可更换其他model

    special_tokens = ["<extra_id_{}>".format(i) for i in range(100)]
    tokenizer = T5Tokenizer.from_pretrained(model_file, do_lower_case=True, max_length=1024, truncation=True,
                                            additional_special_tokens=special_tokens)
    config = T5Config.from_pretrained(model_file)

    model = T5ForConditionalGeneration.from_pretrained(model_file, config=config)
    model.resize_token_embeddings(len(tokenizer))
    model.eval()

    # 情感预测
    emotion_list = []
    for text in text_list:
        prompt = '情感分析任务：' + text + '这篇文章的情感态度是什么？好评/中评/差评'
        encode_dict = tokenizer(prompt, max_length=1024, padding='max_length', truncation=True)

        inputs = {
            'input_ids': torch.tensor([encode_dict['input_ids']]).long(),
            'attention_mask': torch.tensor([encode_dict['attention_mask']]).long(),
        }

        # 生成label
        logits = model.generate(input_ids=inputs['input_ids'], max_length=100, do_sample=True)

        logits = logits[:, 1:]
        emotion = [tokenizer.decode(i, skip_special_tokens=True) for i in logits]
        emotion_list.append(emotion)
    return emotion_list


# 情感获取
def getEmotion(data_path):
    df = pd.read_csv(data_path, encoding='utf-8-sig')
    text_list = df['content'].values.tolist()
    emotion_list = EmotionAnalysis(text_list)
    add_list = {'情感': emotion_list}
    df['情感'] = pd.DataFrame(add_list)
    df.to_csv(data_path, encoding='utf-8-sig')


if __name__ == '__main__':
    # 获取文件夹路径
    dataFolderPath = GetfolderPath()
    DataPathList = GetAllFilePath(dataFolderPath)
    for path in DataPathList:
        getEmotion(path)
    print('预测完毕')
