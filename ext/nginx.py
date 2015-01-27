# coding: utf-8

import logging


logger = logging.getLogger(__name__)

def reload_nginx(sshs):
    # (stdout, stderr, exit_code)
    rs = [ssh.execute('nginx -s reload', sudo=True) for ssh in sshs]
    for _, stderr, exit_code in rs:
        if exit_code:
            logger.error('\n'.join(stderr.readlines()))

