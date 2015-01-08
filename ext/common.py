#!/usr/bin/python
#coding:utf-8

from __future__ import absolute_import

import etcd
import yaml
import time
import string
import random
import logging
from MySQLdb import connect
from influxdb import InfluxDBClient

logger = logging.getLogger(__name__)

LETTERS = string.ascii_letters + string.digits

def get_connections(name, path, env, etcd_config, out_path):
    client = etcd.Client(host=etcd_config, allow_reconnect=True)
    root = yaml.load(client.read(path).value)
    try:
        out = yaml.load(client.read(out_path).value)
    except KeyError:
        out = {}
    influxdb = InfluxDBClient(**root['influxdb'])
    mysql = connect(**root['mysql'])
    return client, influxdb, mysql, out

def random_password(l):
    random.seed(time.time())
    return ''.join(random.sample(LETTERS, l))

def save(client, out_path, out_data):
    pass
