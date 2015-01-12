#!/usr/bin/python
#coding:utf-8

from __future__ import absolute_import

import os
import click
import logging

from ext.common import get_connections
from resource.influxdb import add_influxdb

logger = logging.getLogger(__name__)

OUTPATH_FORMATTER = '/NBE/%s/resource-%s'

@click.group()
@click.argument('name')
@click.option('--path', '-p', default='/NBE/.root/config', help='Path for root config')
@click.option('--env', '-e', default='prod', help='Config for which environment')
@click.pass_context
def cli(ctx, name, path, env):
    if not os.getenv('ETCD'):
        logger.warn('Please Set Etcd in environment first')
        ctx.exit(-1)

    etcd_config = tuple(map(lambda z:(z[0], int(z[1])), (x.split(":"),))[0] for x in os.getenv('ETCD').split(','))
    ctx.obj['app_config_path'] = OUTPATH_FORMATTER % (name, env)
    ctx.obj['app_name'] = name
    ctx.obj['etcd'], ctx.obj['influxdb'], ctx.obj['mysql'] = get_connections(path, etcd_config)
    logger.info('NBE Resource Tool')


commands = cli.command()
commands(add_influxdb)


def main():
    logging.basicConfig(level=logging.INFO)
    cli(obj={})

