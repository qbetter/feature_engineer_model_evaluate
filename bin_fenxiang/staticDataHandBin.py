#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# File Name:'staticDataHandBin'
# Author: huaibei
# Create Date:'2021/8/11'
# 统计数据。将数据中占据频率比较大的先捡出来，剩余的再均分。适用于数据分布极度不均衡的情况

def StatisticData():
  """
  统计数据。聚合某种行为的数据，将至存储到字典的形式，key为行为，value为具体的list。
  :return: 行为数据字典。
  """
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
            ctr = round(float(cilck)/float(send),3)
            ctr = 1.0 if ctr > 1.0 else ctr
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

  luicode_click_send_crt_dict = {}
  for key in luicode_click_send_crt_map:
    # print(key,luicode_click_send_crt_map[key])
    number_list = luicode_click_send_crt_map[key]
    number_vc =  pd.Series(luicode_click_send_crt_map[key]).value_counts(normalize=True)
    luicode_click_send_crt_dict[key] = dict(number_vc)

  return luicode_click_send_crt_dict

def equirFreqentBinAddBigNum(count_value_dict,fenxiangKey,binNum):
  """
  对数据进行分频分箱，较大的值直接加入箱中
  :param count_value_dict: 统计字典
  :param binNum: 分箱数量
  """
  print("--")
  print(fenxiangKey,"分箱.")
  # binNumber 表示要分箱的数量
  binNumber = binNum
  bigBinNum = []
  total_percent = 1.0
  cut_percent = round(total_percent / float(binNumber),4)
  count_value_dt = count_value_dict
  print("cut_percent:",cut_percent)
  #得到本身大于n分之一的桶号
  for k in count_value_dt.keys():
    # print(k,count_value_dt[k])
    if count_value_dt[k] > cut_percent and len(bigBinNum) < binNum-1 :
    # if count_value_dt[k] > cut_percent :
      bigBinNum.append(k)
      binNumber -= 1
      total_percent -= count_value_dt[k]
      cut_percent = round(total_percent / float(binNumber),4)
      # print("cut_percent:",cut_percent)
  #剩余的部分均分成n-m份
  print("bigBinNum len:",len(bigBinNum))
  all_keys = list(count_value_dt.keys())
  # print(all_keys)
  left_list = list(set(all_keys).difference(bigBinNum))
  # print(left_list)

  #获取平均的分箱数据。得到的结果是一个左开右闭的数组
  bonder_sum = 0
  bonder_left = -1
  bonder_result = []
  # print(count_value_dt[1])
  for ky_i in sorted(all_keys):
    # print(fenxiangKey,ky_i,count_value_dt[ky_i])
    if ky_i in bigBinNum:
      if bonder_left != -1:
        bonder_result.append(bonder_left)
        bonder_left = -1
      bonder_result.append(ky_i)
    else:
      if bonder_left ==-1:
        bonder_left = ky_i
      bonder_sum = bonder_sum + float(count_value_dt[ky_i])
      if bonder_sum > cut_percent:
        bonder_result.append(bonder_left)
        bonder_sum = 0
        bonder_left = -1
  #将最右侧的边界数据加进去
  length_all_key = sorted(all_keys)[-1]
  # len(all_keys)

  if length_all_key not in bonder_result:
    bonder_result.append(length_all_key)
  print("bonder_result:",bonder_result)
  return bonder_result

def getDataBin():
  """
  对于统计的数据得到分桶的边界限
  """
  #binNumber 表示要分桶的桶号
  clickBinNumber = 6
  sendBinNumber = 10
  ctrBinNumber = clickBinNumber
  static_data_dict = StatisticData()

  luicode_border_dict = {}
  for luicode_action in static_data_dict:
    luicode_action_value_count = static_data_dict[luicode_action]
    binNumber = clickBinNumber
    if "_send" in luicode_action:
      binNumber = sendBinNumber
    if "_ctr" in luicode_action:
      binNumber = ctrBinNumber
    #对统计数据进行分箱操作
    #得到某行为的分箱边界值了
    bonder_number_list = equirFreqentBinAddBigNum(luicode_action_value_count,luicode_action,binNumber)
    luicode_border_dict[luicode_action] = bonder_number_list

  for key in luicode_border_dict:
    value = luicode_border_dict[key]
    print("key:",key,"\t border value is:",value)

  return luicode_border_dict

if __name__ == '__main__':

    getDataBin()


