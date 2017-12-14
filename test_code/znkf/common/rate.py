# -*- coding: utf-8 -*-

import xlrd
from xlutils.copy import copy
import MySQLdb
import datetime


class Rate():
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456789',
            db='suanfa'
        )
        self.cur = self.conn.cursor()
        self.n = 0
        self.e3 = 0
        self.e2 = 0
        self.e1 = 0
        self.error = 0
        self.g1_p = 0
        self.g1_e = 0
        self.no_answer = 0
        self.total = 0

    def read_excel(self, url, sheet_name):
        """读取excel"""

        book = xlrd.open_workbook(url)
        self.sheet = book.sheet_by_name(sheet_name)

        oldWb = xlrd.open_workbook(url)
        self.w = copy(oldWb)

    def write_excel(self, h, l, right_num, result, g_p, g_e, es_1, es_2, es_3, error, no_answer, file):

        self.w.get_sheet(0).write(h, int(l) + 1, result)
        self.w.get_sheet(0).write(h, l, right_num)
        self.w.get_sheet(0).write(h, int(l) + 2, g_p)
        self.w.get_sheet(0).write(h, int(l) + 3, g_e)
        self.w.get_sheet(0).write(h, int(l) + 4, es_1)
        self.w.get_sheet(0).write(h, int(l) + 5, es_2)
        self.w.get_sheet(0).write(h, int(l) + 6, es_3)
        self.w.get_sheet(0).write(h, int(l) + 7, error)
        self.w.get_sheet(0).write(h, int(l) + 8, no_answer)

        self.w.save(file)
        print 'success'

    def rate(self, url, func, sh):

        self.read_excel(url, sh)

        num = self.sheet.nrows
        for i in range(num):

            row_data = self.sheet.row_values(i)
            rs = str(row_data[9])
            es = row_data[10]
            error = row_data[10]
            group = row_data[7]
            # if es != '' and es != 'no answer ' and es != 'answer false ':
            #     es = int(row_data[9])

            # no_answer
            if rs != 'pass' and error == 'no answer':
                self.no_answer += 1

            # only one answer results
            if group == '1' and rs == 'pass':
                self.g1_p += 1
            elif group == '1' and rs != 'pass':
                self.g1_e += 1

            # answer's number !=1
            elif group != '1':

                if rs != 'pass' and error != 0 and rs != '' and error != 'no answer' and error != 'no answer ':
                    self.error += 1
                    print i
                if rs == 'pass':
                    self.n += 1
                    if es == 1.0:
                        self.e1 += 1
                    elif es == 2.0:
                        self.e2 += 1
                    elif es == 3.0:
                        self.e3 += 1

        if num != 0.0:
            self.total = self.n + self.g1_p
            r = (self.n + self.g1_p) / float(num)

        else:
            print 'error'
        total = str(self.n)
        top1 = str(self.e1)
        top2 = str(self.e2)
        top3 = str(self.e3)
        error = str(self.error)

        if func == 'ga.es_info':
            self.cur.execute(
                "insert into es_info(insert_time,num,top1,top2,top3,error) VALUES (now() ," + total + "," + top1 + "," + top2 + "," + top3 + "," + error + ") ")

        elif func == 'ga.do_score':

            self.cur.execute(
                "insert into do_score(insert_time,num,top1,top2,top3,error) VALUES (now() ," + total + "," + top1 + "," + top2 + "," + top3 + "," + error + ") ")
        elif func == 'ga.wmd_info':

            self.cur.execute(
                "insert into wmd_info(insert_time,num,top1,top2,top3,error) VALUES (now() ," + total + "," + top1 + "," + top2 + "," + top3 + "," + error + ") ")

        # print  self.no_answer
        self.cur.close()
        self.conn.commit()
        self.conn.close()
        self.write_excel(num + 1, 4, 'right:' + str(self.total), self.g1_p, self.g1_e, top1, top2, top3, error,
                         self.no_answer, r, url)

#
# r = Rate()
# r.rate(r'../report/online_169_do_0807.xls', 'ga.do_score', 'zhengli')
