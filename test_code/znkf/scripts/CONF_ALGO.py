# -*- coding: utf-8 -*-
import json


def send_msg(times=0, func='', sh='Sheet1'):
    self.func = func
    # common.excel.read_excel(self.READ_URL, sh)
    self.read_excel(self.READ_URL, sh)
    for n in range(0, times):
        # len = n
        # row_data = self.sheet.row_values(n)
        # self.main_question = row_data[1]
        # self.real_answer = row_data[2]
        # self.like_question = row_data[0]
        #
        # print self.like_question

        url = 'http://113.207.31.77:10002/debug'  # http://192.168.59.9:9999/debug  http://113.207.31.77:10002/debug

        headers = {"content-type": "application/json"}

        data = {

            "tenant-id": 46,
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