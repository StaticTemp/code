# -*- coding: utf-8 -*-
import json
import requests


def send_msg(question):
    url = 'http://192.168.59.9:9999/debug'  # http://192.168.59.9:9999/debug  http://113.207.31.77:10002/debug

    headers = {"content-type": "application/json"}

    data = {

        "tenant-id": 169,
        "queue-type": "Q_QUEUE",
        "type": "get_answer_debug",
        "parameters": [{"question": question

                        }]}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    result = r.text
    rest = json.loads(result)
    return rest
