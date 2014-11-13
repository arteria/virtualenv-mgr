#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='envmanager',
    version='0.0.1',
    description="""Tool to manage your virtualenvs""",
    long_description=open('README.md').read(),
    author='arteria',
    author_email='admin@arteria.ch',
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().split('\n'),
    license="BSD",
    zip_safe=False,
    scripts=['envmanager/epm.py'],
)
