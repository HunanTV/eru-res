#!/usr/bin/python
#coding:utf-8

import logging

from res.ext.common import random_string

logger = logging.getLogger(__name__)

def create_mysql(conn, dbname, username, pass_len):
    def _execute(sql, args=None):
        cur = conn.cursor()
        cur.execute(sql, args)
        conn.commit()
        cur.close()

    # Create database
    sql = r'''CREATE DATABASE IF NOT EXISTS `%s`;'''
    _execute(sql % (dbname, ))

    passwd = random_string(pass_len)
    sql = r'''
GRANT DROP, CREATE, SELECT, INSERT, UPDATE, DELETE ON `%s`.* TO '%s'@'%%' IDENTIFIED BY '%s';
'''
    _execute(sql% (dbname, username, passwd, ))

    sql = r'''
GRANT DROP, CREATE, SELECT, INSERT, UPDATE, DELETE ON `%s`.* TO '%s'@'localhost' IDENTIFIED BY '%s';
'''
    _execute(sql% (dbname, username, passwd, ))
    return {
        'host': conn.get_host_info().split(' ',1)[0],
        'port': conn.port,
        'user': username,
        'passwd': passwd,
        'db': dbname,
    }

