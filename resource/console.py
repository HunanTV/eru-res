#!/usr/bin/python
#coding:utf-8

import os
import sys
import click
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.group()
@click.pass_context
def cli(ctx):
    if os.getenv('ETCD'):
        logger.info('NBE Resource Tool')
        return
    sys.exit(-1)

commands = cli.command()

def main():
    cli()

