from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

import train_xgboost


def train_test():

    # 训练样本路径和测试样本路径
    json_path_train = "D:\evaluation\data\测试数据\\test_8_topN_22859_train.json"
    json_path_test = "D:\evaluation\data\测试数据\\test_8_topN_22859_test.json"

    model_path = "finance8000_cart_scores_wmdr_type.model"

    # 训练样本
    feature_train, label_train = train_xgboost.gen_feature_label(json_path_train)

    # 测试样本
    feature_test, label_test = train_xgboost.gen_feature_label(json_path_test)

    # 训练
    clf = DecisionTreeClassifier(max_depth=20, min_samples_leaf=10) # class_weight="balanced"效果反而降低了 #, min_impurity_split=0.2
    clf.fit(feature_train, label_train)

    z = clf.predict(feature_train)
    pos_right = 0
    neg_right = 0
    for index, e in enumerate(z):
        if label_train[index] == z[index]:
            if label_train[index] == 1:
                pos_right += 1
            else:
                neg_right += 1
    pos_total = list(z).count(1)
    neg_total = len(list(z)) - pos_total
    print("train pos_right: %d/%d => %f" % (pos_right, pos_total, pos_right/pos_total))
    print("train neg_right: %d/%d => %f" % (neg_right, neg_total, neg_right/neg_total))

    # 测试
    z = clf.predict(feature_test)
    pos_right = 0
    neg_right = 0
    for index, e in enumerate(z):
        if label_test[index] == z[index]:
            if label_test[index] == 1:
                pos_right += 1
            else:
                neg_right += 1
    pos_total = list(z).count(1)
    neg_total = len(list(z)) - pos_total
    print("test pos_right: %d/%d => %f" % (pos_right, pos_total, pos_right/pos_total))
    print("test neg_right: %d/%d => %f" % (neg_right, neg_total, neg_right/neg_total))

    # 保存模型
    with open(model_path[:-4] + ".dot", 'w') as f:
        f = tree.export_graphviz(clf, out_file=f)

    import pydotplus

    dot_data = tree.export_graphviz(clf, out_file=None)
    graph = pydotplus.graph_from_dot_data(dot_data)
    graph.write_pdf(model_path[:-4] + ".pdf")

if __name__ == "__main__":

    train_test()









# # 仍然使用自带的iris数据
# iris = datasets.load_iris()
# X = iris.data[:, [0, 2]]
# y = iris.target
#
# # 训练模型，限制树的最大深度4
# clf = DecisionTreeClassifier(max_depth=4)
# #拟合模型
# clf.fit(X, y)
#
#
# # 画图
# x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
# y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
# xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
#                      np.arange(y_min, y_max, 0.1))
#
# Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
# Z = Z.reshape(xx.shape)
#
# plt.contourf(xx, yy, Z, alpha=0.4)
# plt.scatter(X[:, 0], X[:, 1], c=y, alpha=0.8)
# plt.show()