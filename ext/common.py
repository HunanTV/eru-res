#!/usr/bin/python
#coding:utf-8

import etcd
import yaml
import logging
from MySQLdb import connect
from influxdb import InfluxDBClient

logger = logging.getLogger(__name__)

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

