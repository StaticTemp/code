# -*- coding: utf-8 -*-

import sys
import logging

sys.path.append("..")
# import logging.config
from scripts.get_answer_debug import *

if __name__ == "__main__":
    # logging.config.fileConfig(r'C:/Users/lenovo/Desktop/智能客服/config/logging.config')
    ga = GetAnswer(r'data/haiguan.xlsx', r'/report/get_answer_result_gw.xls')
    ga.send_msg(4, ga.do_score, 'zhengli')
