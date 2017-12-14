# -*- coding: utf-8 -*-
# @author: xianghai
import json
import logging
import requests

from pprint import pprint


G_TID = 169
G_WMD_MODE = '1'


def get_rule(rsp):
    if rsp['status'] == '0':
        return rsp['rule']
    else:
        return 'unknown'


def get_ltp(q):
    uri_base = "http://192.168.59.4:9688/api/ltp"
    data = {
        'text': q
    }
    rsp = requests.post(url=uri_base, data=data)
    pq = []
    for w in rsp.json()[0][0]:
        if w['pos'] in ['wp']:
            continue
        pq.append(w['cont'])
    return ' '.join(pq)


def get_intent(q):
    qcc = requests.post(url='http://192.168.59.4:9988/ir', json={
        "tid": "002",
        "q": q
    })

    qca = requests.post(url='http://192.168.59.4:9988/ir', json={
        "tid": "003",
        "q": q
    })
    return qcc.json(),  qca.json()


def get_wmd(q1, q2):
    rsp = requests.post(url='http://192.168.59.4:9999/debug', json={
        "tenant-id": G_TID,
        "queue-type": "Q_QUEUE",
        "type": "score-alg-info-debug",
        "parameters":
            [{
                "q1": str.replace(q1, ' ', ''),
                "q2": str.replace(q2, ' ', ''),
                "match_mode": G_WMD_MODE
            }]
    })
    return rsp.json()['debug-info']['ltp']['wmd_distance']


def add_info(row):
    print(row)
    pq1 = get_ltp(row['q1'])
    pq2 = get_ltp(row['q2'])
    qcc1, qca1 = get_intent(pq1)
    qcc2, qca2 = get_intent(pq2)

    ret = {}
    ret.update(row)
    ret.update({
        'qcc1': get_rule(qcc1),
        'qca1': get_rule(qca1),
        'qcc2': get_rule(qcc2),
        'qca2': get_rule(qca2),
    })
    # wmd-ex stage.
    if ret['qcc1'] == ret['qcc2']and ret['qcc1'] != 'unknown':
        ret.update({'wmdc': get_wmd(qcc1['words'], qcc2['words'])})
    else:
        ret.update({'wmdc': -1})
    if ret['qca1'] == ret['qca2'] and ret['qca1'] != 'unknown':
        ret.update({'wmda': get_wmd(qca1['words'], qca2['words'])})
    else:
        ret.update({'wmda': -1})
    print(ret)
    return ret

# r = {'qcc1': 'time_rules', 'qca2': 'unknown', 'qca1': 'unknown',
#      'q2': '安装后，多久可以正常使用？', 'edit': 0.3333, 'pass': 1,
#      'qcc2': 'time_rules',  'wmd': 0.3841, 'q1': '多久可以正式投入使用？', 'es': 0.5006}
# add_info(r)

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    with open('18362.txt', mode='a', encoding='utf-8') as out:
        # fetch & add info
        with open('develop_169_topN_18362.json', mode='r', encoding='utf-8') as f:
            terms = json.load(f)
            for term in terms:
                out.write(json.dumps(add_info(term), sort_keys=True) + '\n')
                # break

