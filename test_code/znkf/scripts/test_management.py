# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from time import sleep
from xlutils.copy import copy
import xlrd


class TestManagement():
    def __init__(self):

        self.s = []

    def is_visible(self, locator, timeout=10):
        try:
            ui.WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
            False
            return True
        except TimeoutException:
            return

    def read_excel(self, url, sheet_name):

        """读取excel"""

        book = xlrd.open_workbook(url)
        self.sheet = book.sheet_by_name(sheet_name)

    def open_brower(self):
        self.browser = webdriver.Chrome()
        self.browser.get('http://yfzx.cqwisest.com:9135/login.html')
        self.read_excel('../data/test.xlsx', 'zhengli')

        self.browser.find_element_by_id('account').send_keys('13638321740')
        self.browser.find_element_by_id('pwd').send_keys('zjh123456')
        self.browser.find_element_by_xpath('/html/body/div/div[1]/div/div[2]/div[4]/a').click()
        self.is_visible('/html/body/div[2]/div/div[1]/ul/li[2]/a')
        self.browser.find_element_by_xpath('/html/body/div[2]/div/div[1]/ul/li[2]/a').click()  # select repository

    def repository_add(self):
        self.open_brower()

        for i in range(1, 3):
            row_data = self.sheet.row_values(i)
            main_question = row_data[0]
            answer = row_data[4]
            self.s.append(main_question)
            sleep(1)
            self.browser.find_element_by_id('add_repository').click()

            self.browser.find_element_by_id('check_class').click()
            self.browser.find_element_by_xpath('//*[@id="abc_content"]/dl[1]/dd/a').click()  # select class
            self.browser.find_element_by_id('main_que').send_keys(main_question)  # send main question
            self.browser.find_element_by_id('txt_content').send_keys(answer)  # send txt
            self.browser.find_element_by_id('save').click()

    def repository_delete(self):
        for i in self.s:
            self.browser.find_element_by_id('pro_key').clear()
            self.browser.find_element_by_id('pro_key').send_keys(i)
            sleep(1)
            self.browser.find_element_by_id('query').click()
            self.browser.maximize_window()
            self.is_visible('//*[@id="que_table_tb"]/tr/td[6]/a[2]')
            self.browser.find_element_by_xpath('//*[@id="que_table_tb"]/tr/td[6]/a[2]').click()  # click delete
            self.browser.find_element_by_id('con_sure_btn').click()  # SURE delete

    def repository_lead(self):
        pass

#
# test = TestManagement()
#
# test.repository_add()
# test.repository_delete()
