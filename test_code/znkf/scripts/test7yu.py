#! /usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from xlwt import *
import xlrd
from xlutils.copy import copy

import sys

sys.path.append("..")
import logging.config


class compare():
    def __init__(self, url):
        self.URL = url

        self.read_excel('zhengli')
        self.answer_list = []

        lenth = self.sheet.nrows
        for i in range(lenth):
            row_data = self.sheet.row_values(i)
            data = row_data[2]
            self.answer_list.append(data)
        self.answer_list = list(set(self.answer_list))

        print self.answer_list

    def read_excel(self, sheet_name):

        """读取excel"""

        book = xlrd.open_workbook(self.URL)
        self.sheet = book.sheet_by_name(sheet_name)

        oldWb = xlrd.open_workbook(self.URL)
        self.w = copy(oldWb)

    def openfile(self, times, file):
        """wait elements"""
        self.read_excel('zhengli')

        def is_visible(locator, timeout=10):
            try:
                ui.WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
                False
                return True
            except TimeoutException:
                return

        self.browser = webdriver.Chrome()
        self.browser.get(
            "https://qiyukf.com/client?k=bbfedac00ac2a56ebb0618101309a43f&u=svvsflztctl7m2v9ojw6&gid=0&sid=0&qtype=0&dvctimer=0&robotShuntSwitch=0&t=%25EF%25BF%25BD%25C7%25BB%25EF%25BF%25BD%25CB%25BC%25EF%25BF%25BD%25EF%25BF%25BD%25EF%25BF%25BD%25EF%25BF%25BD%25EF%25BF%25BD%25EF%25BF%25BD%25EF%25BF%25BD%25CA%25B4%25EF%25BF%25BD%25CF%25B5%25CD%25B3")

        time.sleep(2)
        for i in range(0, times):

            frame = self.browser.find_element_by_xpath(".//*[@src='about:blank']")

            self.browser.switch_to.frame(frame)

            self.num = i  # 插入excel行数
            logging.debug(i)
            row_data = self.sheet.row_values(i)
            print row_data[0]
            logging.debug(row_data[0])
            self.real_answer = row_data[2]  # excel中问题的准确答案

            self.real_qustion = row_data[1]  # excel中问题的相似答案
            self.like_answer = row_data[0]

            time.sleep(0.5)
            self.browser.find_element_by_xpath('/html/body').send_keys(self.like_answer)

            self.browser.switch_to.default_content()
            element = self.browser.find_element_by_xpath(".//*[@type='submit']")
            self.browser.execute_script('arguments[0].click();', element)

            # self.browser.find_element_by_xpath(".//*[@type='submit']").click()
            # time.sleep(1.5)
            self.starttime = datetime.datetime.now()  # 开始时间

            try:

                time.sleep(1.5)

                self.leng = self.browser.find_element_by_xpath(
                    ".//*[@class='msg msg_left f-cb'][last()]/div/div/ul").text.split('\n')
                is_visible(".//*[@class='qa_label']")

                self.endtime = datetime.datetime.now()  # 结束时间
                # self.robotanswer = self.browser.find_element_by_xpath(".//*[@class='qa_label']").text
                usetime = self.endtime - self.starttime

                self.leng = self.browser.find_element_by_xpath(
                    ".//*[@class='msg msg_left f-cb'][last()]/div/div/ul").text.split('\n')

                length = len(self.leng)
                # time.sleep(1.5)

                for n in range(1, int(length) + 1):
                    is_visible(".//*[@class='msg msg_left f-cb'][last()]/div/div/ul/li[" + str(n) + "]/a")
                    time.sleep(1.5)
                    self.robotanswer = self.browser.find_element_by_xpath(
                        ".//*[@class='msg msg_left f-cb'][last()]/div/div/ul/li[" + str(n) + "]/a").text

                    logging.info(n)
                    logging.info(self.robotanswer)
                    logging.info(self.real_qustion)
                    if self.robotanswer.replace("\n", "") == self.real_qustion.replace("\n", ""):
                        res = 'ok'
                        print res
                        break
                    else:
                        res = 'error'
                        print res

                self.writeexcel(str(usetime), n, 'n', res, file)

                time.sleep(1)

            except:
                # answer only one
                try:
                    self.endtime = datetime.datetime.now()  # 结束时间
                    usetime = self.endtime - self.starttime
                    time.sleep(2)
                    is_visible(".//*[@class='msg msg_left f-cb'][last()]/div/div")
                    self.answer = self.browser.find_element_by_xpath(
                        ".//*[@class='msg msg_left f-cb'][last()]/div/div/div").text

                    self.real_answer = self.real_answer.replace("\n", "").replace(" ", "")
                    self.answer = self.answer.replace("\n", "").replace(" ", "")

                    logging.info(self.answer)
                    logging.info(self.real_answer)
                    print self.answer
                    print self.real_answer

                    if self.answer == self.real_answer:
                        res = 'ok'
                        print res
                        self.writeexcel(str(usetime), 1, 1, res, file)
                    else:
                        for l in range(len(self.answer_list)):
                            if self.answer == self.answer_list[l]:
                                print self.answer_list[l]
                                res = 'error'
                                print res
                                logging.error(res + '哦')
                                self.writeexcel(str(usetime), 1, 1, res, file)
                                break
                            else:
                                res = 'Fail'
                                # print res
                                self.writeexcel(str(usetime), 1, 1, res, file)
                                # self.browser.quit()
                except:
                    self.writeexcel(0, 0, 0, 'no answer', file)

    def writeexcel(self, ut, length, group, result, file):

        self.w.get_sheet(0).write(self.num, 4, ut)
        self.w.get_sheet(0).write(self.num, 5, group)
        self.w.get_sheet(0).write(self.num, 6, length)
        self.w.get_sheet(0).write(self.num, 7, result)
        self.w.save(file)
        # print 'success'


if __name__ == '__main__':
    logging.config.fileConfig(r'../config/logging.config')
    com = compare(r'../data/guanwang2.xls')

    com.openfile(310, r'../report/7yu_test_25.xls')
