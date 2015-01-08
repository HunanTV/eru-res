#!/usr/bin/python
#coding:utf-8

import logging

from ext.common import random_password

logger = logging.getLogger(__name__)

def create(influxdb, dbname, username, pass_len, out, admin):
    if out.get('influxdb'):
        logger.warn('This app contain a influxdb section')
        return False
    if not influxdb.create_database(dbname):
        logger.info('Create influxdb database failed')
        return False
    password = random_password(pass_len)
    influxdb.switch_db(dbname)
    if not influxdb.add_database_user(username, password):
        logger.info('Create influxdb username failed')
        return False
    #TODO because influxdb's bug, here we should set password again
    influxdb.update_database_user_password(username, password)
    if admin and not influxdb.set_database_admin(username):
        logger.info('Set username as admin failed')
        return False
    out['influxdb'] = {
        'host': influxdb._host,
        'port': influxdb._port,
        'username': username,
        'password': password,
        'database': dbname,
    }
    return True

