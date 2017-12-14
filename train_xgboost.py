# -*- coding: utf-8 -*-
"""
function：
@author: qinxunhui
time:
"""

import xgboost as xgb
import json
import numpy as np

from load_q_xianghai import load_q_info
import extract_feature

path = 'D:/evaluation/data/测试数据/finance8000_q_extend_info_ex_with_type.txt'
q_info_dic = load_q_info(path)


def gen_feature_label(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    label = [row['pass'] for row in data]

    feature = []
    for row in data:
        feature_one = extract_feature.get_all_feature(row, q_info_dic)
        feature.append(feature_one)

    label = np.array(label)
    feature = np.array(feature)
    return feature, label


def train_test():

    # 训练样本路径和测试样本路径
    json_path_train = "D:\evaluation\data\测试数据\\test_8_topN_22859_train.json"
    json_path_test = "D:\evaluation\data\测试数据\\test_8_topN_22859_test.json"

    model_path = "finance8000_xgboost_scores_wmdr_type.model"

    # xgboost param
    param = {
        'booster': 'gbtree',                #gbtree使用基于树的模型进行提升计算，gblinear使用线性模型进行提升计算
        'learning_rate': 0.01,              #学习率
        'max_depth': 10,                    #树的最大深度。缺省值为6。通常取值：3-10。树的深度越大，则对数据的拟合程度越高
        'min_child_weight': 1,              #孩子节点中最小的样本权重和。如果一个叶子节点的样本权重和小于min_child_weight则拆分过程结束。即调大这个参数能够控制过拟合。
        'gamma': 0.1,                       #gamma值【0-】值越大算法算法更conservation（保守），且其值依赖于loss function ，在模型中应该进行调参
        'subsample': 0.7,                   #用于训练模型的子样本占整个样本集合的比例。如果设置为0.5则意味着XGBoost将随机的从整个样本集合中抽取出50%的子样本建立树模型，这能够防止过拟合。
        'objective': 'binary:logistic',     #目标函数类型，'binary:logistic'二分类的逻辑回归问题，输出为概率。
        'scale_pos_weight': 1,              #大于0的取值可以处理类别不平衡的情况。帮助模型更快收敛
        'seed': 1000                        #随机数的种子。缺省值为0。可以用于产生可重复的结果
    }

    plst = param.items()

    # 训练样本
    # feature_train, label_train = gen_feature_label(json_path_train)
    feature_train, label_train = gen_feature_label(json_path_train)

    # 测试样本
    # feature_test, label_test = gen_feature_label(json_path_test)
    feature_test, label_test = gen_feature_label(json_path_test)

    dtrain = xgb.DMatrix(feature_train, label=label_train)
    dtest = xgb.DMatrix(feature_test, label=label_test)
    evallist = [(dtest,'eval'), (dtrain,'train')]

    num_round = 20
    bst = xgb.train(plst, dtrain, num_round, evallist)
    bst.save_model(model_path)


if __name__ == "__main__":
    # json_path_train = "D:\svn_algorithm\standard\测试平台算法评测\code\\test_13_topN_22859_train.json"
    # intent_path = "../data/测试数据/finance8000_intent.txt"
    # feature, label = gen_feature_label(json_path_train, intent_path)
    # print(feature, label)

    train_test()




