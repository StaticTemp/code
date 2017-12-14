# -*- coding: utf-8 -*-
"""
function：
@author: qinxunhui
time:
"""
import json

import Levenshtein
from collections import OrderedDict
import xgboost as xgb
import numpy as np
from progressbar import ProgressBar

import extract_feature
import get_debugtool_info
import load_similar_sen
from load_q_xianghai import load_q_info
from wmdr import wmd_sim


def init_do_score_res(topN):
    dic_res = OrderedDict()
    dic_res['paraphrase'] = ""
    dic_res['ground_truth'] = ""
    dic_res['answer'] = ""
    dic_res['shot'] = 0
    dic_res["shot_error"] = 0

    for i in range(topN):
        dic_res['top' + str(i+1)] = 0

    dic_res['error'] = 0
    dic_res['unknown'] = 0
    dic_res['find_que'] = ""
    return dic_res


def init_wmd_res():
    dic_res = OrderedDict()
    dic_res['paraphrase'] = ""
    dic_res['ground_truth'] = ""
    dic_res['answer'] = ""
    dic_res['top1'] = 0
    dic_res['top2'] = 0
    dic_res['top3'] = 0
    dic_res['error'] = 0
    dic_res['unknown'] = 0
    dic_res['find_que'] = ""
    return dic_res


def init_dic_from_dic(d):
    '''
    根据一个字典格式初始化另一个字典，将int类型置为0，其它置为“”
    :param d:
    :return:
    '''
    dic_new = {}
    for k in d:
        if type(d[k]) == int:
            dic_new[k] = 0
        else:
            dic_new[k] = ""
    return dic_new


def judge_right(sen_que, gt_que, gt_ans, res_que, res_ans, maxN = 5, type = 'do_score'):
    '''
    根据问题，知识库原问题，原答案。 结果问题list，结果答案list判断 top1-N,error,unknown
    :param gt_que:str
    :param gt_ans:str
    :param res_que:list[str]
    :param res_ans:list[str]
    :return:dic{top1-N,error,unknown}
    '''
    if type == 'do_score':
        dic_res = init_do_score_res(maxN)
    else:
        dic_res = init_wmd_res()

    dic_res['paraphrase'] = sen_que
    dic_res['ground_truth'] = gt_que
    dic_res['answer'] = gt_ans
    dic_res['find_que'] = str(res_que)
    if len(res_que) != len(res_ans):
        print("input len is error!")
        return

    leven_thre = 0.95
    if len(res_que) == 0:
        dic_res['unknown'] = 1
    elif len(res_que) == 1 and type == 'do_score':
        if Levenshtein.ratio(gt_que, res_que[0]) >= leven_thre or Levenshtein.ratio(gt_ans, res_ans[0]) >= leven_thre:
            dic_res["shot"] = 1
        else:
            dic_res["shot_error"] = 1
    else:
        for i in range(len(res_que)):
            if i > maxN - 1:
                break
            if  Levenshtein.ratio(gt_que, res_que[i]) > leven_thre or Levenshtein.ratio(gt_ans, res_ans[i]) > leven_thre:
                dic_res['top'+str(i+1)] = 1
                break

    if 1 not in dic_res.values():
        dic_res['error'] = 1

    return dic_res


def dic_add_all(dic_list):
    '''
    将dic_list按照int类型键值累计相加，最终得到的字典添加在原list最后
    :param dic_list:
    :return:
    '''
    if len(dic_list) == 0:
        return {}
    elif len(dic_list) == 1:
        return dic_list[0]
    else:
        int_keys = [ k for k in dic_list[0].keys() if type(dic_list[0][k]) == int]
        dic_counter = init_dic_from_dic(dic_list[0])
        for dic2 in dic_list:
            for k in int_keys:
                dic_counter[k] += dic2[k]
        dic_list.append(dic_counter)
        return dic_list


def evaluation_main():

    online_type = True
    version =389
    env = 'local'
    tid = 4

    topN = 10

    data_path = 'D:/evaluation/data/测试数据/'
    dic_tid = {
                12: data_path + '官网.xlsx',
                231: data_path + '医疗_test.xlsx',
                13:  data_path + 'finance_test.xlsx',
                8:  data_path + 'finance8000_test.xlsx',
                4: data_path + 'baidu_tid4_0_1_3_30_31_32_33_34_60_61_62.xlsx'
                }

    dic_env = {'online': 'http://113.207.31.77:10002',
               'test': 'http://192.168.59.9:9996',
               'develop': 'http://192.168.59.4:9999',
               'local': 'http://192.168.240.3:9996'
               }

    # xgbst = xgb.Booster({'nthread':4}) #init model
    # xgbst.load_model("finance8000_xgboost_scores_wmdr.model") # load data

    get_debugtool_info.HOST = dic_env[env]
    data = load_similar_sen.load_excel_para_sen(dic_tid[tid], -1)
    # data = data[0:1000]

    do_score_res = []
    wmd_res = []
    es_res = []
    xg_res = []

    wmdr_res = []
    path = 'D:/evaluation/data/测试数据/finance8000_q_extend_info_ex_with_type.txt'
    q_info_dic = load_q_info(path)


    bar = ProgressBar(max_value=len(data))

    debugtool_info_all = {}
    if online_type == False:
        json_name = env + "_" + str(tid) + "_" + str(version) + "_all_test.json"
        with open(data_path + json_name, 'r') as file:
            debugtool_info_all = json.load(file)

    for index, d in enumerate(data[:1000]):
        bar.update(index)
        if online_type:
            try:
                info = get_debugtool_info.get_debugtool_info(d['paraphrase'], tid)
            except Exception as e:
                print("----------------------------------------")
                print(e)
                print("可能网络超时， d['paraphrase']：" + str(d['paraphrase']))
                print("----------------------------------------")
                continue
        else:
                info = debugtool_info_all.get(d['paraphrase'], {})

        d['answer'] = "sdhfskfhsifsgffs"
        #do_score:
        raw_que = [row['raw-question'] for row in info['final_result']]
        # raw_answer = [json.loads(row['raw-answer'])['answer'] for row in info['final_result']]
        raw_answer = ["没有录入答案"] * len(raw_que)
        res_one = judge_right(d['paraphrase'], d['ground_truth'], d['answer'], raw_que, raw_answer, topN)
        do_score_res.append(res_one)

        #wmd_res:
        raw_que = [row['raw-question'] for row in info['topN']]
        # raw_answer = [json.loads(row['raw-answer'])['answer'] for row in info['topN']]
        raw_answer = ["没有录入答案"] * len(raw_que)
        res_one = judge_right(d['paraphrase'], d['ground_truth'], d['answer'], raw_que, raw_answer, topN)
        wmd_res.append(res_one)

        #es_res:
        raw_que = [row['知识库原问题结果'] for row in info['es']]
        raw_answer = raw_que
        res_one = judge_right(d['paraphrase'], d['ground_truth'], d['answer'], raw_que, raw_answer, topN)
        es_res.append(res_one)

        # #wmdr_res:
        # wmdr_sort = {}
        # for q2 in raw_que:
        #     wmdr_sort[q2] = wmd_sim(d['paraphrase'], q2, q_info_dic)
        # wmdr_sort = sorted(wmdr_sort.items(), key = lambda b:b[1], reverse = True)
        # raw_que = [row[0] for row in wmdr_sort]
        # raw_answer = ["没有录入答案"] * len(raw_que)
        # res_one = judge_right(d['paraphrase'], d['ground_truth'], d['answer'], raw_que, raw_answer, topN)
        # wmdr_res.append(res_one)

        #xg_fusion_res：
        # feature = []
        # for row in info['topN']:
        #     fea_dic = extract_feature.trans_dic(row)
        #     fea_dic['q1'] = d['paraphrase']
        #     fea_dic['q2'] = d['ground_truth']
        #     f = extract_feature.get_all_feature(fea_dic, q_info_dic)
        #     feature.append(f)
        #
        # if len(feature) < 1:
        #     continue
        # feature = np.array(feature)
        # ypred = xgbst.predict(xgb.DMatrix(feature))  # 取值0~1，越接近1则是label 1的概率越高
        # for index, row in enumerate(info['topN']):
        #     row['xg_score'] = ypred[index]
        #
        # info['topN'] = sorted(info['topN'], key=lambda e: e["xg_score"], reverse=True)
        #
        # raw_que = [row['raw-question'] for row in info['topN']]
        # raw_answer = ["没有录入答案"] * len(raw_que)
        # # raw_answer = [json.loads(row['raw-answer'])['answer'] for row in info['topN']]
        # res_one = judge_right(d['paraphrase'], d['ground_truth'], d['answer'], raw_que, raw_answer, topN)
        # xg_res.append(res_one)

    do_score_res = dic_add_all(do_score_res)
    wmd_res = dic_add_all(wmd_res)
    es_res = dic_add_all(es_res)
    # wmdr_res = dic_add_all(wmdr_res)
    # xg_res = dic_add_all(xg_res)

    load_similar_sen.write_list_dic_to_excel(do_score_res, env + "_" +str(tid) + "_do_score_"+str(version)+".xlsx")
    load_similar_sen.write_list_dic_to_excel(wmd_res, env + "_" +str(tid) + "_wmd_"+str(version)+".xlsx")
    load_similar_sen.write_list_dic_to_excel(es_res, env + "_" +str(tid) + "_es_"+str(version)+".xlsx")
    # load_similar_sen.write_list_dic_to_excel(wmdr_res, env + "_" + str(tid) + "_wmdr_" + str(version) + ".xlsx")
    # load_similar_sen.write_list_dic_to_excel(xg_res, env + "_" +str(tid) + "_xg_"+str(version)+"_scores_wmdr.xlsx")

    yy = 0

if __name__ == "__main__":
    evaluation_main()




