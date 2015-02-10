# coding: utf-8

import click
import logging
import yaml

from res.ext.common import save, get_etcd_client, APP_CONFIG_PATH_FORMATTER
from res.ext.sentry import create_sentry

logger = logging.getLogger(__name__)


@click.argument('appname')
@click.option('--platform', '-p', default='python', help='Programming Language')
@click.option('--namespace', '-n', default='public', help='Namespace of Gitlab')
@click.pass_context
def add_sentry(ctx, appname, platform, namespace):
    etcd = get_etcd_client(**ctx.obj['root_config']['etcd_config'])
    app_config_path = APP_CONFIG_PATH_FORMATTER.format(appname=appname)

    try:
        config = yaml.load(etcd.read(app_config_path).value) or {}
    except:
        logger.info('app %s config not exist' % appname)
        ctx.exit(-1)

    if 'sentry_dsn' in config:
        logger.info('app %s already has sentry' % appname)
        return

    sentry = create_sentry(ctx.obj['root_config']['sentry_url'], namespace, platform, appname)
    config['sentry_dsn'] = sentry['dsn']
    save(etcd, app_config_path, config)
