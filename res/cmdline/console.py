# coding:utf-8

from __future__ import absolute_import

import os
import click
import logging

from res.ext.common import load_etcd_config, get_root_config

from res.cmdline.influxdb import add_influxdb
from res.cmdline.sentry import add_sentry
from res.cmdline.nginx import nginx_reload, nginx_clean, \
        set_upstreams, remove_upstreams

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
commands(nginx_clean)
commands(set_upstreams)
commands(remove_upstreams)

def main():
    logging.basicConfig(level=logging.INFO)
    cli(obj={})

