#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from setuptools import setup, find_packages


version = __import__('attachable').__version__
readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='django-attachable',
    version=version,
    description='',
    long_description=readme,
    author='Sasha Matijasic',
    author_email='sasha@logit.hr',
    url='http://bitbucket.org/selectnull/django-attachable/',
    packages=find_packages(),
    license='MIT',
    install_requires=('django', ),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
