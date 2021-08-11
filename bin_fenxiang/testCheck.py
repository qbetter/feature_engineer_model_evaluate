#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
# File Name:'testCheck'
# Author: huaibei
# Create Date:'2021/8/11'
def fencxiang():
  # 1.52971136 , 0.53533325 , 0.93095874]
  factors = [25,10,17,17,34,26,13,39,19,21,37,23,5,7,8,20,10,23,15,21,22,10,12,36,30,34,23,17,23,32,31,11,33,24,28,19,10,9,20,25,6,8,27]
  # factors = [25, 10, 17, 17]
  # factors =  ['0', '0', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
  # factors = [0, 0, 0, 0, 2, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  # factors =  [2, 1, 0, 0, 0]
  print("random number is:",factors)
  # three_bin,bins = pd.qcut(factors, 2,retbins=True,duplicates='drop')
  # three_bin,bins = pd.qcut(factors,3,retbins=True,precision=3,duplicates='drop')
  countV = pd.Series(factors).value_counts(normalize=True)
  print(countV)
  countV.plot.bar()

  # three_bin = pd.qcut(factors, 4, labels=["a","b","c","d"])
  # print(three_bin)
  # print(three_bin.value_counts())
  # print(bins)
  # plt.plot(np.random.normal(size=100), np.random.normal(size=100), 'ro')
  # fig = plt.figure()
  # plt.bar(countV)
  plt.show()


if __name__ == '__main__':
    fencxiang()
