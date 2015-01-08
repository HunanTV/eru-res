#!/usr/bin/python
#coding:utf-8

import click
import logging

from ext.influxdb import create

logger = logging.getLogger(__name__)

@click.option('--length', '-l', default=5, help='Password length')
@click.option('--admin', '-a', is_flag=True, help='Set as admin')
@click.pass_context
def create_influxdb(ctx, length, admin):
    if create(ctx.obj['influxdb'], ctx.obj['name'], ctx.obj['name'], length, ctx.obj['out'], admin):
        print ctx.obj['out']

