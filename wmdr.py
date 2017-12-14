import sys
sys.path.append("d:/robot/robot")
from wmd import wmd_sim_core


def wmd_sim(q1, q2, seg_info_dic):
    '''
    读入两句话和tid信息，计算wmd距离。es词频此时传入空
    :return:
    '''
    try:
        pre_q1_ltp = seg_info_dic[q1]['trunk_seg_list']
        pos_q1_ltp = seg_info_dic[q1]['trunk_pos_list']
        pre_q2_ltp = seg_info_dic[q2]['trunk_seg_list']
        pos_q2_ltp = seg_info_dic[q2]['trunk_pos_list']
        if len(pre_q1_ltp) == 0 or len(pre_q2_ltp) == 0:
            return 0
    except:
        print("no seg info: ", q1)
        print("no seg info: ", q2)
        return 0

    debug_info = dict()
    debug_info["ltp"] = {}

    if wmd_sim_core.inited == False:
        wmd_sim_core.init()
    wmd_sim_core.ES_DF_WC_DICT = {}
    wmd_sim_core.MATCH_MODE = 0
    # wmd_sim_core.TENANT_ID_INFO = TENANT_ID_DIC.get(tenant_id, {})
    # wmd_sim_core.B_SHORT_SEN = short_sen_classify(q1, pre_q1_ltp, pos_q1_ltp)
    wmd_sim_core.SEN_ASK = q1
    wmd_sim_core.SEN_ES = q2
    tenant_id = 0
    dist = wmd_sim_core.score(tenant_id, pre_q1_ltp, pre_q2_ltp, pos_q1_ltp, pos_q2_ltp, debug_info["ltp"])

    return 1 - dist