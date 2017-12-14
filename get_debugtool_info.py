# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:38:44 2017

@author: qxh 
fun: 从调试工具获得算法结果
"""
import json
HOST = 'http://192.168.59.9:9996'

import requests
#requests调用更加简单
def get_debugtool_json(que, tid):

    #url = HOST + '/debug'  #注意修改
    url = HOST + '/api/v1/debug'
    data = {
            "tenant-id": tid, #菜谱尾号57，知乎是59
            "chat_close": True,
            "net_close": True,
            "queue-type": "Q_QUEUE",
            "type": "get_answer_debug",
            "parameters": [
             {
              "question": que
             }
            ]
        } 
    res = requests.post(url = url, data = json.dumps(data),timeout=10).json() #timeout单位为秒
    
    return res

def get_debugtool_info(que, tid):
    '''
    输入：
    返回：几种信息 
    '''
    result_json = get_debugtool_json(que, tid)

    methods = list(result_json['debug-info'].keys())
    
    all_info = {}
    for me in methods: 
        try:
            #有几种类型不满足这种格式
            me_info = result_json['debug-info'][me]['value']
            me_info = get_dic_from_sen_list(me_info)
            all_info[me] = me_info
        except:
            pass
        
    return all_info
    
def get_dic_from_sen_list(list_info):
    '''
    输入：[[{'desc','value'}]]
    输出：[dic{'desc-value':'value-value'}]
    '''
    dic_result = []
    if len(list_info) > 0:
        for sen_info in list_info:
            dic_temp = {}
            for pro in sen_info:
                dic_temp[pro['desc']] = pro['value']
            dic_result.append(dic_temp)
    return dic_result

if __name__ == '__main__':
    
    que = '我想问一下什么是动态口令卡？'
    res2 = get_debugtool_info(que, 13)
    yy = 0
    print(res2)
