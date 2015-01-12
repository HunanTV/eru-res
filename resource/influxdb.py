#!/usr/bin/python
#coding:utf-8

import click
import logging
import yaml

from ext.common import save
from ext.influxdb import create_influxdb

logger = logging.getLogger(__name__)


@click.option('--length', '-l', default=5, help='Password length')
@click.option('--admin', '-a', is_flag=True, help='Set as admin')
@click.pass_context
def add_influxdb(ctx, length, admin):
    etcd, influxdb, app_config_path = ctx.obj['etcd'], ctx.obj['influxdb'], ctx.obj['app_config_path']
    try:
        config = yaml.load(etcd.read(app_config_path).value)
    except:
        logger.info('app %s config not exist' % ctx.obj['app_name'])
        ctx.exit(-1)

    if 'influxdb' in config:
        logger.info('app %s already has influxdb' % ctx.obj['app_name'])
        return

    influxdb_config = create_influxdb(influxdb, ctx.obj['app_name'], ctx.obj['app_name'], length, admin)
    if influxdb_config:
        config['influxdb'] = influxdb_config
        save(etcd, app_config_path, config)

