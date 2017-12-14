# -*- coding: utf-8 -*-

# import logging
import json
import requests
# import common.excel
from common.rate import *
import xlrd
import datetime
from xlutils.copy import copy
import sys
import common.use_mysql

sys.path.append("..")
import logging.config

reload(sys)
sys.setdefaultencoding('utf-8')


class GetAnswer:
    def __init__(self, read_url, save_url, start_time='', end_time="", use_time=''):

        self.READ_URL = read_url  # 读取文件路径
        self.SAVE_URL = save_url  # 保存文件路径

        self.start_time = start_time
        self.end_time = end_time
        self.use_time = use_time

    def read_excel(self, url, sheet_name):

        """读取excel"""
        self.sheet_name = sheet_name
        book = xlrd.open_workbook(url)
        self.sheet = book.sheet_by_name(sheet_name)
        oldWb = xlrd.open_workbook(self.READ_URL)
        self.w = copy(oldWb)

    def write_excel(self, time, top, result, reason, file):

        """向excel中写入结果"""

        try:

            if self.sheet_name != 'fanli':
                self.w.get_sheet(0).write(self.len, 6, time)
                self.w.get_sheet(0).write(self.len, 8, top)
                self.w.get_sheet(0).write(self.len, 9, result)
                self.w.get_sheet(0).write(self.len, 10, reason)
            else:
                self.w.get_sheet(1).write(self.len, 6, time)
                self.w.get_sheet(1).write(self.len, 8, top)
                self.w.get_sheet(1).write(self.len, 9, result)
                self.w.get_sheet(1).write(self.len, 10, reason)

            self.w.save(file)
            print 'success'

        except IOError:
            print 'error'

    def send_msg(self, times=0, func='', sh='Sheet1'):

        self.func = func
        # common.excel.read_excel(self.READ_URL, sh)
        self.read_excel(self.READ_URL, sh)
        for n in range(0, times):
            self.len = n
            row_data = self.sheet.row_values(n)
            self.main_question = row_data[1]
            self.real_answer = row_data[2]
            self.like_question = row_data[0]
            logging.info(self.like_question)
            print self.like_question

            url = ' http://192.168.59.9:9999/debug'  # http://192.168.59.9:9999/debug  http://113.207.31.77:10002/debug

            headers = {"content-type": "application/json"}

            data = {

                "tenant-id": 169,
                "queue-type": "Q_QUEUE",
                "type": "get_answer_debug",
                "parameters": [{"question": self.like_question

                                }]}
            self.start_time = datetime.datetime.now()  # 开始时间

            r = requests.post(url, data=json.dumps(data), headers=headers)
            self.end_time = datetime.datetime.now()  # 结束时间
            self.use_time = self.end_time - self.start_time
            result = r.text
            self.rest = json.loads(result)

            func()

    def do_score(self):

        value = self.rest['debug-info']['final_result']['value']
        if len(value) == 0:
            self.write_excel(str(self.use_time), len(value), "Fail", "no answer", self.SAVE_URL)
            self.w.get_sheet(0).write(self.len, 7, '0')
            print 'no'
        for i in range(len(value)):
            if len(value) == 1:
                score = value[i]
                # extend_id = score[2]['value']
                correct_question = score[4]['value']
                # sql语句
                # mysql_str = "select question FROM main_question WHERE tenant_id=46 AND  is_delete=0 AND id in (select main_id FROM like_question WHERE question='" + correct_question + "' and tenant_id=46);"
                # """调用mysql"""
                # info = common.use_mysql.get_mysql('222.180.162.163','reader','test001','intelligent_server',mysql_str)
                # try:
                #
                #     que = info[0][0]
                #
                # except:
                #     que = ""
                answer = score[5]['value']
                self.real_answer = self.real_answer.replace("\n", "").replace(" ", "")
                answer = answer.replace("\n", "").replace(" ", "")

                if answer == self.real_answer or correct_question == self.main_question:
                    # and correct_question == self.main_question
                    self.write_excel(str(self.use_time), 1, "pass", 1, self.SAVE_URL)
                    self.w.get_sheet(0).write(self.len, 3, correct_question)
                    self.w.get_sheet(0).write(self.len, 7, '1')
                    # self.w.get_sheet(0).write(self.len, 12, que)
                else:

                    self.write_excel(str(self.use_time), 1, "Fail", " answer false ", self.SAVE_URL)
                    self.w.get_sheet(0).write(self.len, 3, correct_question)
                    self.w.get_sheet(0).write(self.len, 7, '1')
                    # self.w.get_sheet(0).write(self.len, 12, que)

            elif len(value) != 1 and len(value) != 0:

                score = value[i]
                correct_question = score[4]['value']
                answer = score[5]['value']
                answer = answer.replace("\n", "").replace(" ", "")

                if correct_question == self.main_question or self.real_answer == answer:

                    self.write_excel(str(self.use_time), 1, "pass", int(i) + 1, self.SAVE_URL)
                    self.w.get_sheet(0).write(self.len, 3 + i, answer)
                    self.w.get_sheet(0).write(self.len, 7, 'n')
                    break

                else:
                    self.write_excel(str(self.use_time), 0, "Fail", int(i) + 1, self.SAVE_URL)
                    # logging.debug('top3 error')
                    self.w.get_sheet(0).write(self.len, 3 + i, answer)
                    self.w.get_sheet(0).write(self.len, 7, 'n')
                    # break

            else:
                self.write_excel(str(self.use_time), len(value), "Fail", "无答案 ", self.SAVE_URL)
                self.w.get_sheet(0).write(self.len, 3 + i, answer)
                self.w.get_sheet(0).write(self.len, 7, '')
                print 'no'

    def base_info(self):
        value = self.rest['debug-info']['base_info']['value']
        if len(value) != 0:
            info = value[0]
            print info
            print info[1]
            if info[1]['value'] == 'meta-name_rules':
                self.write_excel(str(self.use_time), len(value), "pass", "", self.SAVE_URL)
            else:
                self.write_excel(str(self.use_time), len(value), "pass", "", self.SAVE_URL)
        else:
            self.write_excel(str(self.use_time), len(value), "error", "", self.SAVE_URL)

        self.i = 0

        self.read_excel(self.SAVE_URL, 'Sheet1')
        num = self.sheet.nrows
        print num

    def es_info(self):
        value = self.rest['debug-info']['es']['value']

        if len(value) == 0:
            self.write_excel(str(self.use_time), 0, "error", "no answer", self.SAVE_URL)
        for i in range(len(value)):

            str_info_out = value[i][8]['value']
            self.main_question = self.main_question.replace('\n', '').replace(" ", "")
            str_info_out = str_info_out.replace('\n', '').replace(" ", "")

            if self.main_question == str_info_out or self.like_question == str_info_out:
                if i == 0:
                    self.write_excel(str(self.use_time), 1, "pass", i + 1, self.SAVE_URL)
                elif i <= 2:
                    self.write_excel(str(self.use_time), 1, "pass", i + 1, self.SAVE_URL)
                else:
                    self.write_excel(str(self.use_time), 1, "pass", "", self.SAVE_URL)

                # self.write_excel(str(self.use_time), 1, "pass", "", self.SAVE_URL)
                break
            else:
                self.write_excel(str(self.use_time), 0, "error", "", self.SAVE_URL)

    def wmd_info(self):
        value = self.rest['debug-info']['topN']['value']
        if len(value) == 0:
            self.write_excel(str(self.use_time), 0, "error", "no answer", self.SAVE_URL)
        for w in range(len(value)):
            que = value[w][4]['value']
            asw = value[w][11]['value']
            self.real_answer = self.real_answer.replace('\n', '').replace(" ", "")
            asw = asw.replace("\n", "").replace(" ", "")
            if self.main_question == que or self.real_answer == asw:
                if w == 0:
                    self.write_excel(str(self.use_time), 1, "pass", w + 1, self.SAVE_URL)
                    self.sheet_name
                elif w <= 2:
                    self.write_excel(str(self.use_time), 1, "pass", w + 1, self.SAVE_URL)

                # else:
                #     self.write_excel(str(self.use_time), 1, "pass_1", '', self.SAVE_URL)
                else:
                    self.write_excel(str(self.use_time), 0, "error", "over 3", self.SAVE_URL)

                break
            else:
                self.write_excel(str(self.use_time), 0, "error", "", self.SAVE_URL)


if __name__ == "__main__":
    logging.config.fileConfig(r'../config/logging.config')

    ga = GetAnswer(r'../data/guanwang2.xls', r'../report/test_46_do_0810.xls')

    ga.send_msg(309, ga.do_score, 'zhengli')
    # ga.send_msg(10, ga.base_info)
    # ga.send_msg(309, ga.es_info, 'zhengli')
    # ga.send_msg(309, ga.wmd_info, 'zhengli')
    r = Rate()
    r.rate(r'../report/test_46_do_0810.xls', 'ga.do_score', 'zhengli')
