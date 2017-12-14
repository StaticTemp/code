from sklearn.datasets import load_iris
from sklearn import tree
import sys
import os


iris = load_iris()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)

with open("iris.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)

import pydotplus

dot_data = tree.export_graphviz(clf, out_file=None)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("iris.pdf")


from xgboost import XGBClassifier
from xgboost import plot_tree
import matplotlib.pyplot as plt
import xgboost as xgb

model = XGBClassifier()
model.fit(iris.data, iris.target)

plot_tree(model)
plt.show()

xgbst = xgb.Booster({'nthread': 4})  # init model
xgbst.load_model("finance8000_xgboost_scores_wmdr.model")  # load data

booster = xgbst.get_booster()
tree = booster.get_dump(fmap='xgb.fmap')[0]
tree = tree.split()

# plot_tree(xgbst)
# plt.show()





#
# from IPython.display import Image
# dot_data = tree.export_graphviz(clf, out_file=None,
#                          feature_names=iris.feature_names,
#                          class_names=iris.target_names,
#                          filled=True, rounded=True,
#                          special_characters=True)
# graph = pydotplus.graph_from_dot_data(dot_data)
# Image(graph.create_png())

#
# from itertools import product
#
# import numpy as np
# import matplotlib.pyplot as plt
#
# from sklearn import datasets
# from sklearn.tree import DecisionTreeClassifier
#
#
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
#
# from IPython.display import Image
# from sklearn import tree
# import pydotplus
# dot_data = tree.export_graphviz(clf)
# dot_data = tree.export_graphviz(clf, out_file=None)
# # dot_data = tree.export_graphviz(clf, out_file=None,
# #                          feature_names=iris.feature_names,
# #                          class_names=iris.target_names,
# #                          filled=True, rounded=True,
# #                          special_characters=True)
# graph = pydotplus.graph_from_dot_data(dot_data)
# Image(graph.create_png())