# coding: utf-8

import os
import click

from utils.helper import get_ssh
from ext.nginx import reload_nginx


def _load_nginx_hosts(path):
    hosts = []
    with open(path, 'r') as f:
        for host in f:
            hosts.append(host.strip())
    return hosts


@click.option('--nginx-list', '-l', default=os.path.expanduser('~/.nginx'), help='Nginx list file')
@click.option('--key-file', '-k', default=os.path.expanduser('~/.ssh/armin.pub'), help='SSH public key file')
@click.option('--user', '-u', default='armin', help='User name to login')
@click.pass_context
def nginx_reload(ctx, nginx_list, key_file, user):
    hosts = _load_nginx_hosts(nginx_list)
    sshs = [get_ssh(host, key_file, user) for host in hosts]
    reload_nginx(sshs)
