# -*- coding: utf-8 -*-

import logging
import json
import requests
import xlrd
from xlutils.copy import copy
import sys

sys.path.append("..")
import logging.config


class PaChong:
    def __init__(self, read_url, save_url):

        self.READ_URL = read_url  # 读取文件路径
        self.SAVE_URL = save_url  # 保存文件路径

    def read_excel(self, url):

        """读取excel"""

        book = xlrd.open_workbook(url)
        self.sheet = book.sheet_by_name("Sheet1")

        oldWb = xlrd.open_workbook(url)
        self.w = copy(oldWb)

    def write_excel(self, result, reason, file):

        """向excel中写入结果"""
        logging.info('write excel')
        try:
            self.w.get_sheet(0).write(self.len, 5, result)
            self.w.get_sheet(0).write(self.len, 6, reason)
            self.w.save(file)
            print 'success'

        except IOError:
            print 'error'
            logging.exception('Exception Logged')

    def send_msg(self, num):
        self.read_excel(self.READ_URL)
        for i in range(0, num):

            row_data = self.sheet.row_values(i)

            self.len = i  # excel
            msg = row_data[3]  # question
            rules = row_data[1]  # rule
            grammar = row_data[0]  # grammar

            print msg
            data = {
                "grammar": grammar,
                "qs": [
                    msg
                ]
            }
            logging.info(data)
            url = 'http://192.168.59.9:9996/api/v1/sr'
            headers = {"content-type": "application/json"}
            r = requests.post(url, data=json.dumps(data), headers=headers)

            result = r.text

            rest = json.loads(result)

            code = rest["irs"][0]["code"]
            rule = rest["irs"][0]["rule"]
            # logging.info(code,rule)
            if code == 0 and rule == rules:

                self.write_excel("ok", "", self.SAVE_URL)

            elif code != 0 and rule == rules:
                self.write_excel("error", "code!=0", self.SAVE_URL)
                logging.debug('code!=0')

            elif rule != rules and code == 0:
                self.write_excel("error", "rule error", self.SAVE_URL)
                logging.debug('rule error')

            elif code != 0 and rule != rules:
                self.write_excel("error", "code and rule both error", self.SAVE_URL)
                logging.debug('code and rule both error')

            else:
                self.write_excel("error", "other", self.SAVE_URL)
                logging.error('error')


if __name__ == "__main__":
    logging.config.fileConfig(r'../config/logging.config')
    pz = PaChong(r'../data/pachong_170707.xlsx', r'../report/pc_result.xls')
    pz.send_msg(282)
