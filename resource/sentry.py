# coding: utf-8

import click
import logging
import yaml

from ext.common import save
from ext.sentry import create_sentry

logger = logging.getLogger(__name__)


@click.option('--platform', '-p', default='python', help='language')
@click.option('--namespace', '-n', default='public', help='namespace of gitlab')
@click.pass_context
def add_sentry(ctx, platform, namespace):
    etcd, app_config_path = ctx.obj['etcd'], ctx.obj['app_config_path']
    try:
        config = yaml.load(etcd.read(app_config_path).value) or {}
    except:
        logger.info('app %s config not exist' % ctx.obj['app_name'])
        ctx.exit(-1)

    if 'sentry_dsn' in config:
        logger.info('app %s already has sentry' % ctx.obj['app_name'])
        return
    sentry = create_sentry(ctx.obj['root_config']['sentry_url'], namespace, platform, ctx.obj['app_name'])
    config['sentry_dsn'] = sentry['dsn']
    save(etcd, app_config_path, config)
