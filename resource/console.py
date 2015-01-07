#!/usr/bin/python
#coding:utf-8

from __future__ import absolute_import

import os
import etcd
import yaml
import click
import logging
from MySQLdb import connect
from influxdb import InfluxDBClient

from resource.influxdb import create_influxdb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init(ctx, name, path, env, etcd_config):
    ctx.obj['etcd'] = etcd.Client(host=etcd_config, allow_reconnect=True)
    ctx.obj['root'] = yaml.load(ctx.obj['etcd'].read(path).value)
    out_path = '/NBE/%s/resource-%s' % (name, env)
    try:
        ctx.obj['out'] = yaml.load(ctx.obj['etcd'].read(out_path).value)
    except KeyError:
        ctx.obj['out'] = {}
        ctx.obj['name'] = name
    ctx.obj['influxdb'] = InfluxDBClient(**ctx.obj['root']['influxdb'])
    ctx.obj['mysql'] = connect(**ctx.obj['root']['mysql'])

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
    init(ctx, name, path, env, etcd_config)
    logger.info('NBE Resource Tool')

commands = cli.command()
commands(create_influxdb)

def main():
    cli(obj={})

