# -*- coding: utf-8 -*-
"""
function：
@author: qinxunhui
time:
"""
import json


def load_q_info(q_path):
    """
    :param path: 向海的问句信息路径
    :return: {"q":{}}
    """

    with open(q_path, mode='r', encoding='utf-8') as file:
        data = file.readlines()

    q_info_dic = {}
    for row in data:
        try:
            info_row = json.loads(row)
            q_info_dic[info_row["q"]] = info_row
            q_info_dic[info_row["q"]]['ltp_seg_list'] = [e["cont"] for e in info_row['s1']]
            q_info_dic[info_row["q"]]['ltp_pos_list'] = [e["pos"] for e in info_row['s1']]
            q_info_dic[info_row["q"]]['merged_seg_list'] = [e["cont"] for e in info_row['s2']]
            q_info_dic[info_row["q"]]['merged_pos_list'] = [e["pos"] for e in info_row['s2']]
            q_info_dic[info_row["q"]]['trunk_seg_list'] = [e["cont"] for e in info_row['trunk']]
            q_info_dic[info_row["q"]]['trunk_pos_list'] = [e["pos"] for e in info_row['trunk']]
        except Exception as e:
            print(e)

    return q_info_dic


def load_q_intent(path):
    with open(path, mode = 'r', encoding = 'utf-8') as file:
        data = file.readlines()
    intent_dic = {}
    for row in data:
        row = eval(row)
        intent_dic[row["q"]] = row["is"]
    return intent_dic
