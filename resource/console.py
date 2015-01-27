# coding:utf-8

from __future__ import absolute_import

import os
import click
import logging

from ext.common import load_etcd_config, get_root_config

from resource.influxdb import add_influxdb
from resource.sentry import add_sentry
from resource.nginx import nginx_reload

logger = logging.getLogger(__name__)

ETCD_CONFIG_PATH = os.path.expanduser('~/.armin.yaml')

@click.group()
@click.option('--config-path', '-p', default='/NBE/.root/config', help='Path for root config in etcd')
@click.pass_context
def cli(ctx, config_path):
    if not os.path.isfile(ETCD_CONFIG_PATH):
        logger.error('etcd config %s not exist' % ETCD_CONFIG_PATH)
        ctx.exit(-1)

    etcd_config = load_etcd_config(ETCD_CONFIG_PATH)
    ctx.obj['etcd_config'] = etcd_config
    ctx.obj['root_config'] = get_root_config(config_path, etcd_config)
    logger.info('NBE Resource Tool')


commands = cli.command()
commands(add_influxdb)
commands(add_sentry)
commands(nginx_reload)


def main():
    logging.basicConfig(level=logging.INFO)
    cli(obj={})

