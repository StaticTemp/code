# -*- coding: utf-8 -*-
"""
function：多分数融合排序规则， 返回策略。
@author: qinxunhui
time:
"""

def muti_scores_rank(tenant_id, muti_score_lst):
    '''
    对多个分数进行组合排序
    :param tenant_id:
    :param muti_score_lst: [{'es_score':, 'wmd_score':,...}]
    :return: 同上，不过增加了综合分数字段：‘score’
    '''

    top3_thre_prec = 0.35
    leven_match = 0.001
    inten_match = 0.01
    MATCH_MODE = 1

    wmd_w = 0.73
    edit_w = 0
    es_w = 0

    for row in muti_score_lst:
        if row["edit_score"] < 0.05:
            row["score"] = leven_match
        else:
            score_three = (wmd_w * row["wmd_score"] + edit_w * row["edit_score"] + es_w * row["es_score"]) / (wmd_w + edit_w + es_w)
            row["score"] = score_three

            if score_three < top3_thre_prec:
            # 如果有一个意图匹配上，分数置为0.01*, 两个匹配上0.002*，没有匹配上0.35*
                if row["inten_score"] == 1:
                    row["score"] = inten_match * (1 + score_three)
                elif row["inten_score"] >= 2:
                    row["score"] = inten_match * (1 + score_three) * 0.2
                elif row["inten_score"] < 0:
                    if MATCH_MODE == 0:  # 对于精确匹配意图不一致则放弃
                        row["score"] = top3_thre_prec + inten_match * (1 + score_three)
                    else:
                        row["score"] = top3_thre_prec
                else:
                    pass

    return muti_score_lst


def filter_result(tenant_id, res):
    '''
    输入算法得到的排序后的候选结果，过滤出前几位给q_robot。
    :param res: [{"score":,...},]
    :return:
    '''
    # max_num_return = conf_algorithm.get_value(tenant_id, "MAX_NUM_RETURN")
    # space_top1_top2 = conf_algorithm.get_value(tenant_id, "SPACE_TOP1_TOP2")
    # top3_thre_prec = conf_algorithm.get_value(tenant_id, "TOP3_THRE_PREC")
    # top3_thre_index = conf_algorithm.get_value(tenant_id, "TOP3_THRE_INDEX")
    # leven_match = conf_algorithm.get_value(tenant_id, "LEVEN_MATCH")
    # top1_thre = conf_algorithm.get_value(tenant_id, "TOP1_THRE")
    max_num_return = 3
    space_top1_top2 = 0.03
    top3_thre_prec = 0.35
    top3_thre_index = 0.5
    leven_match = 0.01
    top1_thre = 0.25
    MATCH_MODE = 1

    if MATCH_MODE == 0:
        res_obj = list(filter(lambda x: float(x["score"]) <= top3_thre_prec, res))
    else:
        res_obj = list(filter(lambda x: float(x["score"]) <= top3_thre_index, res))

    if len(res_obj) > 0:
        #问题和知识库问题全匹配，直接返回。这条必须有，和刘科逻辑相关。
        if res_obj[0]["score"] <= leven_match:
            return res_obj[0:1]
        #top0 < 阈值，且相似度低于top2 0.03. 返回top1
        if res_obj[0]["score"] <= top1_thre: # 属于不同问题 且 得分相差很小的情况
            if len(res_obj) > 1 and res_obj[1]["score"] - res_obj[0]["score"] < space_top1_top2 and res_obj[1]["qa-id"] != res_obj[0]["qa-id"]:
                return res_obj[0:min(max_num_return, len(res_obj))]
            else:
                return res_obj[0:1]
        else:
            return res_obj[0:min(max_num_return, len(res_obj))]
    else:
        return []