# -*- coding: utf-8 -*-
"""
Created on Wed April 13 10:57:59 2022

@author: jct
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns #直方图
# 数据分析类
class ManaHotelAnalysis:
    def __init__(self):
        self.data = pd.DataFrame()
        
    def readAnalysis(self, txtName):
        self.data = pd.read_csv(txtName, sep=',', header='infer')  # 读取文件
        return 1

    def scoreAnalysis(self):
        data = self.data.values
        score_mean = data[:, 4].mean()
        score_var = data[:, 4].std()
        res = data[:, [0, 4]]
        print("=========scoreAnalysis===========")
        hist = plt.figure()
        sns.distplot(data[:,4], bins=20, hist=True, kde=True)
        return score_mean, score_var,hist

    def avgPriceAnalysis(self):
        data = self.data.values
        avgPrice_mean = data[:, 3].mean()
        avgPrice_var = data[:, 3].std()
        res = data[:, [0, 3]]
        print("=========avgPriceAnalysis===========")
        box = plt.figure()
        plt.boxplot(data[:,3])
        #plt.show()
        return avgPrice_mean, avgPrice_var,box