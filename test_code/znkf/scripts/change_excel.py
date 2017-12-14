# -*- coding: utf-8 -*-

import xlrd
from xlutils.copy import copy
import sys
from pyExcelerator import *

sys.path.append("..")


class change:
    def __init__(self):
        self.read_excel()
        len = self.sheet.nrows
        self.answer_list = []
        for m in range(len):

            row = self.sheet.row_values(m)
            d = row[1]
            if d not in self.answer_list:
                d = d.replace('\n', '').replace(" ", "")
                self.answer_list.append(d)

                # print self.answer_list

    def read_excel(self):
        """读取excel"""
        # self.w = w
        book = xlrd.open_workbook('../data/main2.xls')
        self.sheet = book.sheet_by_name("Sheet1")

        # oldWb = xlrd.open_workbook(url)
        # self.w = copy(oldWb)
        # return self.w

    def write_excel(self):
        """向excel中写入结果"""
        self.read_excel()
        book = xlrd.open_workbook(r'../data/7.27.xlsx')
        self.sheet_2 = book.sheet_by_name("Sheet1")

        oldWb = xlrd.open_workbook(r'../data/7.27.xlsx')
        self.w = copy(oldWb)

        for i in range(400):

            # main_question = data[0]
            data2 = self.sheet_2.row_values(i)  # question excel

            for n in range(len(self.answer_list)):

                data = self.sheet.row_values(n)  # main question excel

                answer = data[1]

                q_answer = data2[2]  # 2 answer
                q_answer = q_answer.replace('\n', '').replace(" ", "")
                if q_answer == self.answer_list[n]:
                    main_question = data[0]
                    self.w.get_sheet(0).write(i, 1, main_question)
                    break
            self.w.save(r'../data/7.27.xls')


if __name__ == "__main__":
    c = change()
    c.write_excel()
