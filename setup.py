#!/usr/bin/python
#coding:utf-8
import os
from setuptools import setup

# package meta info
NAME = "resource"
VERSION = "0.0.1"
DESCRIPTION = "NBE resource tool"
AUTHOR = "CMGS"
AUTHOR_EMAIL = "ilskdw@gmail.com"
LICENSE = "BSD"
URL = "http://git.hunantv.com"
KEYWORDS = "influxdb mysql"

ENTRY_POINTS = {
    'console_scripts':['res=resource.console:main',]
}

INSTALL_REQUIRES = [
    'click',
    'influxdb',
    'python-etcd',
    'MySQL-python',
    'PyYAML',
    'requests',
]

PACKAGES = ['resource', 'ext',]

here = os.path.abspath(os.path.dirname(__file__))

def read_long_description(filename):
    path = os.path.join(here, filename)
    if os.path.exists(path):
        return open(path).read()
    return ""

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read_long_description('README.rst'),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    url=URL,
    keywords=KEYWORDS,
    packages=PACKAGES,
    zip_safe=False,
    entry_points=ENTRY_POINTS,
    install_requires=INSTALL_REQUIRES,
)

