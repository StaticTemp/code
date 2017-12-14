#! /usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
import datetime
import time
from email.mime.text import MIMEText
from html import HTML
import MySQLdb

mailto_list = ["372509392@qq.com", "9937003394@qq.com"]


class SendEmail:
    def __init__(self):
        self.mail_host = "smtp.163.com"  # 设置服务器
        self.mail_user = "zhoujiahui0217"  # 用户名
        self.mail_pass = "zjh123456"  # 口令
        self.mail_postfix = "163.com"  # 发件箱的后缀

        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456789',
            db='suanfa'
        )
        self.cur = self.conn.cursor()
        # do_score
        self.cur.execute("select * from do_score where id in (SELECT max(id) FROM do_score)")
        self.do_score = self.cur.fetchone()
        # es_info
        self.cur.execute('select * from es_info  where id in (SELECT max(id) FROM es_info)')
        self.es = self.cur.fetchone()

        # wmd_info
        self.cur.execute('select * from wmd_info  where id in (SELECT max(id) FROM wmd_info)')
        self.wmd = self.cur.fetchone()

    def send_mail(self, to_list, sub, content):  # to_list：收件人；sub：主题；content：邮件内容
        me = "hello" + "<" + self.mail_user + "@" + self.mail_postfix + ">"  # 这里的hello可以任意设置，收到信后，将按照设置显示
        msg = MIMEText(content, _subtype='html', _charset='utf-8')  # 创建一个实例，这里设置为html格式邮件

        msg['Subject'] = sub  # 设置主题
        msg['From'] = me
        msg['To'] = ";".join(to_list)

        try:
            s = smtplib.SMTP()
            s.connect(self.mail_host)  # 连接smtp服务器
            s.login(self.mail_user, self.mail_pass)  # 登陆服务器
            s.sendmail(me, to_list, msg.as_string())  # 发送邮件
            s.close()
            return True
        except Exception, e:
            print str(e)
            return False

    def html(self):
        inline_css = {
            'class1': 'border: 1px solid #DADADA',
            'class2': 'background:#DDDDDD;color:#666;padding:10px 12px;width:60px; border:none; font-family:verdana,arial,sans-serif;',
            'class3': 'color:#646464;border:none;background:#ececec;text-align:center',
        }

        d_1 = self.do_score[2]
        d_2 = self.do_score[3]
        d_3 = self.do_score[4]
        d_4 = self.do_score[5]
        d_5 = self.do_score[6]

        e_1 = self.es[2]
        e_2 = self.es[3]
        e_3 = self.es[4]
        e_4 = self.es[5]
        e_5 = self.es[6]

        w_1 = self.wmd[2]
        w_2 = self.wmd[3]
        w_3 = self.wmd[4]
        w_4 = self.wmd[5]
        w_5 = self.wmd[6]

        self.h = HTML()
        self.h.h2('生产环境官网-算法测试结果')
        self.h.h2('总数314')
        self.h.h3('do_score')
        t1 = self.h.table(style=inline_css['class1'])

        r1 = t1.tr()
        r1.th('totle', style=inline_css['class2'])
        r1.th('top1', style=inline_css['class2'])
        r1.th('top2', style=inline_css['class2'])
        r1.th('top3', style=inline_css['class2'])
        r1.th('error', style=inline_css['class2'])
        n1 = t1.tr()
        n1.td(str(d_1), style=inline_css['class3'])
        n1.td(str(d_2), style=inline_css['class3'])
        n1.td(str(d_3), style=inline_css['class3'])
        n1.td(str(d_4), style=inline_css['class3'])
        n1.td(str(d_5), style=inline_css['class3'])

        self.h.h2('es_info')
        t2 = self.h.table(style=inline_css['class1'])

        r2 = t2.tr()
        r2.th('totle', style=inline_css['class2'])
        r2.th('top1', style=inline_css['class2'])
        r2.th('top2', style=inline_css['class2'])
        r2.th('top3', style=inline_css['class2'])
        r2.th('error', style=inline_css['class2'])
        n2 = t2.tr()
        n2.td(str(e_1), style=inline_css['class3'])
        n2.td(str(e_2), style=inline_css['class3'])
        n2.td(str(e_3), style=inline_css['class3'])
        n2.td(str(e_4), style=inline_css['class3'])
        n2.td(str(e_5), style=inline_css['class3'])

        self.h.h2('wmd_info')
        t3 = self.h.table(style=inline_css['class1'])

        r3 = t3.tr()
        r3.th('totle', style=inline_css['class2'])
        r3.th('top1', style=inline_css['class2'])
        r3.th('top2', style=inline_css['class2'])
        r3.th('top3', style=inline_css['class2'])
        r3.th('error', style=inline_css['class2'])
        n3 = t3.tr()
        n3.td(str(w_1), style=inline_css['class3'])
        n3.td(str(w_2), style=inline_css['class3'])
        n3.td(str(w_3), style=inline_css['class3'])
        n3.td(str(w_4), style=inline_css['class3'])
        n3.td(str(w_5), style=inline_css['class3'])
        self.h = str(self.h)
        print self.h
        self.send_mail(mailto_list, 'online_43', self.h)


sm = SendEmail()
sm.html()
