# coding:utf-8

import click
import logging
import yaml

from res.ext.common import get_etcd_client, get_influxdb_client, save, APP_CONFIG_PATH_FORMATTER
from res.ext.influxdb import create_influxdb


logger = logging.getLogger(__name__)


@click.argument('appname')
@click.option('--length', '-l', default=5, help='Password length')
@click.option('--admin', '-a', is_flag=True, help='Set as admin')
@click.pass_context
def add_influxdb(ctx, appname, length, admin):
    etcd = get_etcd_client(**ctx.obj['root_config']['etcd_config'])
    influxdb = get_influxdb_client(**ctx['root_config']['influxdb'])
    app_config_path = APP_CONFIG_PATH_FORMATTER.format(appname=appname)

    try:
        config = yaml.load(etcd.read(app_config_path).value) or {}
    except:
        logger.info('app %s config not exist' % appname)
        ctx.exit(-1)

    if 'influxdb' in config:
        logger.info('app %s already has influxdb' % appname)
        return

    influxdb_config = create_influxdb(influxdb, appname, appname, length, admin)
    if influxdb_config:
        config['influxdb'] = influxdb_config
        save(etcd, app_config_path, config)

