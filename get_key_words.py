# -*- coding: utf-8 -*-
"""
function：给定一组词汇，和两句话A、b, 判断A、b包含核心词的交/并比。当都不包含核心词的时候，返回-1
@author: qinxunhui
time:20171205
"""

class GetKeyWords():
    def __init__(self, lst_path):
        data = []
        with open(lst_path, 'r', encoding='utf8') as file:
            data = file.readlines()
        self.key_words = [row.strip() for row in data]
        if self.key_words == []:
            print("GetKeyWords init fail ! \n")

    def get_words(self, que):
        '''
        :param que:
        :return: ['关键词1'，...]
        '''
        words = []
        for w in self.key_words:
            if w in que:
                words.append(w)
        return words

    def compare_key_words(self, q1, q2):
        '''
        :param q1:
        :param q2:
        :return:
            -1: q1和q2都不含有关键词时
            0-1: inter/union
        '''
        words_q1 = self.get_words(q1)
        words_q2 = self.get_words(q2)
        #并集
        w1_uni = {}
        words = words_q1 + words_q2
        union_words = [w1_uni.setdefault(x, x) for x in words if (x not in w1_uni)]
        #交集
        inter_words = []
        for w in words_q1:
            if w in words_q2:
                inter_words.append(w)
        #交集/并集
        if len(union_words) > 0:
            same = 0
            for w in inter_words:
                if w in union_words:
                    same += 1
            return same/len(union_words)
        else:
            return -1

if __name__ == "__main__":
    KW = GetKeyWords('D:/evaluation/data/测试数据/product_name.txt')
    print("KW", KW.key_words)
    words = KW.get_words('紫金2号集合计划的内容是什么')
    print(words)
    same = KW.compare_key_words('号集合计划的内容是什么紫金2sdf1号', '紫金x1号集合计划的内容是什么')
    print(same)