# -*- coding: utf-8 -*-
"""
function：
@author: qinxunhui
time:
"""

import json
from progressbar import ProgressBar

import load_similar_sen
import algorithm_evaluate_debugtool
from wmdr import wmd_sim
from load_q_xianghai import load_q_info


def evaluation_main():
    version = 22859
    env = 'test'
    tid = 8
    topN = 10

    data_path = 'D:/evaluation/data/测试数据/'
    dic_tid = {
                169: data_path + '官网.xlsx',
                231: data_path + '医疗_test.xlsx',
                13:  data_path + 'finance_test.xlsx',
                8:   data_path + 'finance8000_test.xlsx'
                }

    q_info_dic = load_q_info(data_path + "finance8000_q_extend_info_ex.txt")

    json_name = env + "_" + str(tid) + str(version)+"_all_test.json"
    with open(data_path + json_name, 'r') as file:
        topN_res_all = json.load(file)

    data = load_similar_sen.load_excel_para_sen(dic_tid[tid], -1)
    bar = ProgressBar(max_value=len(data))

    wmd_res = []
    wmdr_res = []

    for index, d in enumerate(data):
        bar.update(index)
        try:
            info = topN_res_all[d['paraphrase']]
        except Exception as e:
            print("----------------------------------------")
            print(e)
            print("之前入库问题不对，重新入库， d['paraphrase']：" + str(d['paraphrase']))
            print("----------------------------------------")
            continue

        d['answer'] = "sdhfskfhsifsgffs"

        # wmd_res:
        raw_que = [row['raw-question'] for row in info['topN']]
        # raw_answer = [json.loads(row['raw-answer'])['answer'] for row in info['topN']]
        raw_answer = ["没有录入答案"] * len(raw_que)
        res_one = algorithm_evaluate_debugtool.judge_right(d['paraphrase'], d['ground_truth'], d['answer'], raw_que, raw_answer, topN)
        wmd_res.append(res_one)

        # wmdr_res:
        wmdr_sort = {}
        for q2 in raw_que:
            wmdr_sort[q2] = wmd_sim(d['paraphrase'], q2, q_info_dic)
        wmdr_sort = sorted(wmdr_sort.items(), key = lambda b:b[1], reverse = True)
        raw_que = [row[0] for row in wmdr_sort]
        res_one = algorithm_evaluate_debugtool.judge_right(d['paraphrase'], d['ground_truth'], d['answer'], raw_que, raw_answer, topN)
        wmdr_res.append(res_one)

    wmd_res = algorithm_evaluate_debugtool.dic_add_all(wmd_res)
    wmdr_res = algorithm_evaluate_debugtool.dic_add_all(wmdr_res)

    load_similar_sen.write_list_dic_to_excel(wmd_res, env + "_" +str(tid) + "_wmd_"+str(version)+".xlsx")
    load_similar_sen.write_list_dic_to_excel(wmdr_res, env + "_" +str(tid) + "_wmdr_"+str(version)+".xlsx")

if __name__ == "__main__":
    evaluation_main()













