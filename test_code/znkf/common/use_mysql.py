#! /usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import re


def get_mysql(ip, user, pw, db, str_sql):
    conn = MySQLdb.connect(
        host=ip,
        port=3306,
        user=user,
        passwd=pw,
        db=db,
        charset="utf8"
    )
    info = ''
    conn.set_character_set('utf8')
    cur = conn.cursor()
    aa = cur.execute(str_sql)
    if re.match('select', str_sql):
        info = cur.fetchmany(aa)
    elif re.match('insert', str_sql):
        pass
    elif re.match('delete', str_sql):
        pass
    else:
        print 'error'

    return info
