# coding: utf-8

import logging
import requests

from res.utils.helper import scp_file
from res.ext.common import random_string


logger = logging.getLogger(__name__)

def reload_nginx(sshs, local_path, remote_path):
    for ssh in sshs:
        file_name = local_path.rsplit('/')[-1]
        tmp_path = '/tmp/%s.tmp.%s' % (file_name, random_string(4))
        scp_file(ssh, local_path, tmp_path)
        ssh.execute('mv %s %s' % (tmp_path, remote_path), sudo=True)
        ssh.execute('nginx -s reload', sudo=True)


def clean_nginx(sshs, remote_path):
    for ssh in sshs:
        ssh.execute('rm %s' % remote_path, sudo=True)
        ssh.execute('nginx -s reload', sudo=True)


def update_upstream(hosts, name, upstreams):
    for host in hosts:
        url = '%s/upstream/%s' % (host, name)
        r = requests.post(url, data=upstreams)
        if r.status_code != 200:
            logger.error('Update %s failed, code %d' % (url, r.status_code))

def delete_upstream(hosts, name):
    for host in hosts:
        url = '%s/upstream/%s' % (host, name)
        r = requests.delete(url)
        if r.status_code != 200:
            logger.error('Delete %s failed, code %d' % (url, r.status_code))

