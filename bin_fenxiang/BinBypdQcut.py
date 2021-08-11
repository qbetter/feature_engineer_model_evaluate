#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# File Name:'BinBypdQcut'
# Author: huaibei
# Create Date:'2021/8/9'
# 通过pandas.qcut函数对数据进行分箱操作

def binning():
  """
  #使用pandas.qcut函数来分箱。由于数据极不均匀，点击为0的占据95%，导致只能分一个箱子，
  """
  #先对数据进行统计。然后再对进行分箱
  # filename = "../data/part-02997_head"
  filename = "../data/part-02997"
  luicode_click_send_crt_map = {}
  with open(filename) as f:
    for line in f:
      spline = line.strip().split("\t")
      # print(spline)
      uid2luicodes = spline[12]
      # print(uid2luicodes)
      #对uid对业务的行为数据进行处理：10000216bjc_0_12;10001167_0_4。将之拆分到业务和行为
      if(uid2luicodes!=None):
        # print(uid2luicodes)
        uid2luicode_sp = uid2luicodes.split(";")
        for uid2luicode in uid2luicode_sp:
          luicode,cilck,send = uid2luicode.split("_")
          ctr = 0
          if (cilck!='0'):
            ctr = float(cilck)/float(send)
          if luicode+"_click" not in luicode_click_send_crt_map:
            luicode_click_send_crt_map[luicode + "_click"] = [int(cilck)]
          else:
            luicode_click_send_crt_map[luicode+"_click"].append(int(cilck))
          if luicode + "_send" not in luicode_click_send_crt_map:
            luicode_click_send_crt_map[luicode + "_send"] = [int(send)]
          else:
            luicode_click_send_crt_map[luicode+"_send"].append(int(send))
          if luicode+"_ctr" not in luicode_click_send_crt_map:
            luicode_click_send_crt_map[luicode+"_ctr"] = [ctr]
          else:
            luicode_click_send_crt_map[luicode+"_ctr"].append(ctr)

  luicode_action_bin_map = {}
  for ky in luicode_click_send_crt_map.keys():
    # print(ky)
    listValue = luicode_click_send_crt_map[ky]
    SetValue = set(listValue)
    listLen = len(listValue)
    Setlen = len(SetValue)
    cut_num = 4 if  Setlen > 4 else Setlen
    # print(SetValue,listLen,Setlen,cut_num)

    kyBin,bins = pd.qcut(listValue, cut_num, retbins=True,duplicates='drop')
    luicode_action_bin_map[ky] = bins
  # print("checkout---")
  # print(luicode_click_send_crt_map["10000216bjc_send"])
  for key in luicode_action_bin_map.keys():
    print(key,"border value:",luicode_action_bin_map[key])


if __name__ == '__main__':
    binning()
