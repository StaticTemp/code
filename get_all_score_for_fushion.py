# -*- coding: utf-8 -*-
"""
function：
@author: qinxunhui
time:
"""
import get_debugtool_info
import load_similar_sen
import Levenshtein
# from collections import Counter
from collections import OrderedDict
import json
import pickle
from progressbar import ProgressBar

def classify_sen(sen_que, res_que, gt_que, gt_ans):
    leven_thre = 0.97
    if Levenshtein.ratio(gt_que, sen_que) >= leven_thre or Levenshtein.ratio(gt_ans, res_que) >= leven_thre:
        return 1
    else:
        return 0

version = 22859
env = 'test'
tid = 8

data_path = 'D:/svn_algorithm/standard/测试平台算法评测/data/测试数据/'
dic_tid = {
            169: data_path + '官网.xlsx',
            231: data_path + '医疗_test.xlsx',
            13:  data_path + 'finance_test.xlsx',
            8:   data_path + 'finance8000_test.xlsx'
            }

dic_env = {'online': 'http://113.207.31.77:10002',
           'test': 'http://192.168.59.9:9996',
           'develop': 'http://192.168.59.4:9999',
           'local': 'http://172.16.1.85:9999'
           }

get_debugtool_info.HOST = dic_env[env]
data = load_similar_sen.load_excel_para_sen(dic_tid[tid], -1)

topN_res = []
topN_res_all = {}

bar = ProgressBar(max_value=len(data))

for index, d in enumerate(data):
    bar.update(index)
    try:
        info = get_debugtool_info.get_debugtool_info(d['paraphrase'], tid)
    except:
        print("可能网络超时， d['paraphrase']：" + str(d['paraphrase']))
        continue
    topN_res_all[d['paraphrase']] = info

    for i in range(len(info['topN'])):
        dic_res = {}
        dic_res["q1"] = d['paraphrase']
        dic_res["q2"] = info['topN'][i]['raw-question']
        # dic_res["pass"] = classify_sen(info['topN'][i]['raw-question'], info['topN'][i]['raw-answer'], d['ground_truth'], d['answer'])
        dic_res["pass"] = classify_sen(info['topN'][i]['raw-question'], "meiyoudaan",
                                       d['ground_truth'], "没有答案")
        dic_res["es"] = float(info['topN'][i]['es_score'])
        dic_res["wmd"] = float(info['topN'][i]['wmd_score'])
        dic_res["edit"] = float(info['topN'][i]['edit_score'])

        dic_res['intent'] = json.loads(info['topN'][i]["intent_result"])
        topN_res.append(dic_res)

print(topN_res)

json_name = env + "_" + str(tid) + "_topN_"+str(version)+"_test.json"
with open(json_name, 'w') as file:
    json.dump(topN_res, file)

json_name = env + "_" + str(tid) + str(version)+"_all_test.json"
with open(json_name, 'w') as file:
    json.dump(topN_res_all, file)











