# coding: utf-8

import requests


def create_sentry(sentry_url, app_name, namespace, platform):
    url = '%s/register_dsn/%s/%s/%s' % (sentry_url, namespace, platform, app_name)
    r = requests.get(url)
    return r.json()

