# -*- coding: utf-8 -*-
"""
function：
@author: qinxunhui
time:
"""

from get_key_words import GetKeyWords
import wmdr


def get_qca_feature(qca_res):
    qca_list = ['reason_rules', 'amount_rules', 'advice_rules', 'definition_rules', 'evaluation_rules']
    feature = [0] * (len(qca_list)+1)
    try:
        index = qca_list.index(qca_res)
        feature[index+1] = 1
    except:
        if qca_res != 'unknown':
            print("warning: qca_res is not in set!" + qca_res)
        pass
    return feature


def get_qcc_feature(qcc_res):
    qcc_list = ['time_rules', 'location_rules', 'name_rules', 'price_rules', 'contact_rules', 'enumeration_rules']
    feature = [0] * (len(qcc_list)+1)
    try:
        index = qcc_list.index(qcc_res)
        feature[index+1] = 1
    except:
        if qcc_res != 'unknown':
            print("warning: qcc_res is not in set!" + qcc_res )
        pass
    return feature


def get_intent_feature(rule_list):
    rules = ['time_rules', 'reason_rules', 'price_rules', 'name_rules', 'location_rules', 'evaluation_rules',
             'enumeration_rules', 'definition_rules', 'contact_rules', 'amount_rules', 'advice_rules']
    feature = [0] * (len(rules)+1)

    for r in rule_list:
        try:
            index = rules.index(r)
            feature[index+1] = 1
        except:
            if r != 'unknown':
                print("warning: rule is not in rules set! ", r)
            continue
    return feature

KW = GetKeyWords('D:/evaluation/data/测试数据/product_name.txt')


def trans_dic(debugtool_dic):
    """
    :param debugtool_dic: 调试工具输出的do_score每一行
    :return: {"q1":, "q2":, "es":, "edit":, "wmd", ...}
    """
    fea_dic = {}
    # fea_dic['q1'] = debugtool_dic['paraphrase']
    # fea_dic['q2'] = debugtool_dic['ground_truth']
    fea_dic['es'] = debugtool_dic['es_score']
    fea_dic['edit'] = debugtool_dic['edit_score']
    fea_dic['wmd'] = debugtool_dic['wmd_score']
    return fea_dic


def get_all_feature(debugtool_dic, q_info_dic):
    """
    :param debugtool_dic: {"q1":, "q2":, "es":, "edit":, "wmd", ...}
    :param q_info_dic: {q:{"is", "ltp_seg_list", "ltp_pos_list", "merged_seg_list"，“merged_pos_list”，“trunk_seg_list”，“trunk_pos_list”}}
    :return: [es_score, ...]
    """

    q1_intent = q_info_dic.get(debugtool_dic["q1"], {}).get("is", [])
    q2_intent = q_info_dic.get(debugtool_dic["q2"], {}).get("is", [])
    q1_intent_feature = get_intent_feature(q1_intent)
    q2_intent_feature = get_intent_feature(q2_intent)
    q1_type_feature = q_info_dic.get(debugtool_dic["q1"], {}).get("question_type", {})
    q1_intent_feature = [q1_type_feature["YES_NO"], q1_type_feature["DESCRIPTION"], q1_type_feature["ENTITY"]]
    q2_type_feature = q_info_dic.get(debugtool_dic["q2"], {}).get("question_type", {})
    q1_intent_feature = [q2_type_feature["YES_NO"], q2_type_feature["DESCRIPTION"], q2_type_feature["ENTITY"]]

    wmdr_score = wmdr.wmd_sim(debugtool_dic['q1'], debugtool_dic['q2'], q_info_dic)

    kw_fea = KW.compare_key_words(debugtool_dic['q1'], debugtool_dic['q2'])

    feature_one = [debugtool_dic['es'], debugtool_dic['edit'], debugtool_dic['wmd'], wmdr_score]
    # feature_one = [debugtool_dic['es'], debugtool_dic['edit'], debugtool_dic['wmd']]
    # feature_one = [debugtool_dic['es'], debugtool_dic['edit'], wmdr_score, kw_fea]
    # feature_one = [debugtool_dic['es'], debugtool_dic['edit'], debugtool_dic['wmd'], wmdr_score, kw_fea]
    feature_one = [debugtool_dic['es'], debugtool_dic['edit'], debugtool_dic['wmd'], wmdr_score]
    # feature_one.extend(q1_intent_feature)
    # feature_one.extend(q2_intent_feature)
    feature_one.extend(q1_intent_feature)
    feature_one.extend(q2_intent_feature)

    return feature_one