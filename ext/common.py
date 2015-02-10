# coding:utf-8

from __future__ import absolute_import

import etcd
import yaml
import time
import string
import random
import logging
import MySQLdb
import influxdb

logger = logging.getLogger(__name__)

LETTERS = string.ascii_letters + string.digits
APP_CONFIG_PATH_FORMATTER = '/NBE/{appname}/resource-prod'


def load_etcd_config(path):
    config = {}
    with open(path, 'r') as f:
        config = yaml.load(f)
    etcds = config.get('etcd', [])

    def _translate(h):
        host, port = h.split(':')
        return host, int(port)

    return tuple(_translate(e) for e in etcds)


def get_etcd_client(etcd_config):
    return etcd.Client(host=etcd_config, allow_reconnect=True)


def get_influxdb_client(**kw):
    return influxdb.InfluxDBClient(**kw)


def get_mysql_client(**kw):
    return MySQLdb.connect(**kw)


def get_root_config(path, etcd_config):
    etcd_client = get_etcd_client(etcd_config)
    return yaml.load(etcd_client.read(path).value)


def random_string(l):
    random.seed(time.time())
    return ''.join(random.sample(LETTERS, l))


def save(client, out_path, out_data):
    data = yaml.safe_dump(out_data, default_flow_style=False)
    client.write(out_path, data)

