# coding: utf-8

import logging

from utils.helper import scp_file
from ext.common import random_password


logger = logging.getLogger(__name__)

def reload_nginx(sshs, local_path, remote_path):
    for ssh in sshs:
        file_name = local_path.rsplit('/')[-1]
        tmp_path = '/tmp/%s.tmp.%s' % (file_name, random_password(4))
        scp_file(ssh, local_path, tmp_path)
        ssh.execute('cp %s %s' % (tmp_path, remote_path), sudo=True)
        ssh.execute('nginx -s reload', sudo=True)

