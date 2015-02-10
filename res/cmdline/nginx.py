# coding: utf-8

import os
import click

from res.utils.helper import get_ssh
from res.ext.nginx import reload_nginx, clean_nginx, \
        update_upstream, delete_upstream


def _load_nginx_hosts(path):
    hosts = []
    with open(path, 'r') as f:
        for host in f:
            hosts.append(host.strip())
    return hosts


def _gen_upstreams(upstreams):
    return ';'.join('server %s' % upstream for upstream in upstreams.split(',')) + ';'


@click.argument('local_path')
@click.argument('remote_path')
@click.option('--nginx-list', '-l', default=os.path.expanduser('~/.nginx'), help='Nginx list file')
@click.option('--key-file', '-k', default=os.path.expanduser('~/.ssh/armin.pub'), help='SSH public key file')
@click.option('--user', '-u', default='armin', help='User name to login')
@click.pass_context
def nginx_reload(ctx, local_path, remote_path, nginx_list, key_file, user):
    hosts = _load_nginx_hosts(nginx_list)
    sshs = [get_ssh(host, key_file, user) for host in hosts]
    reload_nginx(sshs, local_path, remote_path)


@click.argument('remote_path')
@click.option('--nginx-list', '-l', default=os.path.expanduser('~/.nginx'), help='Nginx list file')
@click.option('--key-file', '-k', default=os.path.expanduser('~/.ssh/armin.pub'), help='SSH public key file')
@click.option('--user', '-u', default='armin', help='User name to login')
@click.pass_context
def nginx_clean(ctx, remote_path, nginx_list, key_file, user):
    hosts = _load_nginx_hosts(nginx_list)
    sshs = [get_ssh(host, key_file, user) for host in hosts]
    clean_nginx(sshs, remote_path)

@click.argument('appname')
@click.argument('upstreams')
@click.option('--update-list', '-l', default=os.path.expanduser('~/.update'), help='Nginx update interface list file')
@click.pass_context
def set_upstreams(ctx, appname, upstreams, update_list):
    hosts = _load_nginx_hosts(update_list)
    upstreams = _gen_upstreams(upstreams)
    update_upstream(hosts, appname, upstreams)

@click.argument('appname')
@click.option('--update-list', '-l', default=os.path.expanduser('~/.update'), help='Nginx update interface list file')
@click.pass_context
def remove_upstreams(ctx, appname, update_list):
    hosts = _load_nginx_hosts(update_list)
    delete_upstream(hosts, appname)

