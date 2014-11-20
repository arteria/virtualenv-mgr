#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import virtualenvmgr

version = virtualenvmgr.__version__

setup(
    name='virtualenv-mgr',
    version=version,
    description="""Tool to manage your virtualenvs""",
    long_description=open('README.md').read(),
    author='arteria',
    author_email='admin@arteria.ch',
    url='https://github.com/arteria/virtualenv-mgr',
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().split('\n'),
    license="BSD",
    zip_safe=False,
    scripts=['virtualenvmgr/virtualenv-mgr'],
)
