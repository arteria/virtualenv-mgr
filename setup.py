#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import envmanager

version = envmanager.__version__

setup(
    name='envmanager',
    version=version,
    description="""Tool to manage your virtualenvs""",
    long_description=open('README.md').read(),
    author='arteria',
    author_email='admin@arteria.ch',
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().split('\n'),
    license="BSD",
    zip_safe=False,
    scripts=['envmanager/virtualenv-mgr.py'],
)
