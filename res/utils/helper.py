#!/usr/bin/python
#coding:utf-8

import os


def output_logs(log, lines):
    for line in lines:
        log(line.strip('\n'))


def get_lines(lines):
    p = lines.rfind('\n')
    return lines[p+1:], lines[:p+1].splitlines()


def get_address(server):
    return server.split(':')


def get_path(ctx, d, key, dirname, pattern):
    value = d.get(key)
    if not value:
        ctx.fail('Key %s not exists' % key)
    path = os.path.join(dirname, pattern % value)
    if not os.path.exists(path):
        ctx.fail('Target file %s not exist' % path)
    return value, path


def shell_escape(string):
    """
    Escape double quotes, backticks and dollar signs in given ``string``.

    For example::

        >>> _shell_escape('abc$')
        'abc\\\\$'
        >>> _shell_escape('"')
        '\\\\"'
    """
    for char in ('"', '$', '`'):
        string = string.replace(char, '\%s' % char)
    return string


def get_ssh(server, key_filename, username):
    from libs.ssh import SSHClient
    return SSHClient(server, username=username, key_filename=key_filename)


def scp_file(ssh, local_path, remote_path):
    from libs.scp import SCPClient
    scp = SCPClient(ssh.get_transport())
    scp.put(local_path, remote_path)

