#!/usr/bin/python
#coding:utf-8

import logging

from res.ext.common import random_string

logger = logging.getLogger(__name__)

def create_influxdb(client, dbname, username, pass_len, admin=False):
    if not client.create_database(dbname):
        logger.info('create influxdb database error')
        return
    password = random_string(pass_len)
    client.switch_db(dbname)
    if not client.add_database_user(username, password):
        logger.info('create influxdb user error')
        return
    if admin and not client.set_database_admin(username):
        logger.info('set %s to admin error' % username)
        return
    return {
        'host': client._host,
        'port': client._port,
        'username': username,
        'password': password,
        'db': dbname,
    }
