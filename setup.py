#!/usr/bin/env python
# -*- coding: utf8 -*-
import os.path

from setuptools import setup

import compose_mode

install_requires = [
    'docker-compose >= 1.7, < 1.8',
    'PyYAML >= 3.10, < 4',
]

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
]

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme_file:
    long_description = readme_file.read()

setup(
    # Metadata
    name='compose-mode',
    version=compose_mode.__version__,
    packages=['compose_mode'],
    author='Kit Barnes',
    author_email='k.barnes@mhnltd.co.uk',
    description='A tiny wrapper around docker-compose to '
                'easily use multiple sets of config files',
    long_description=long_description,
    url='https://github.com/KitB/compose-mode',
    license='MIT',
    keywords='docker',
    classifiers=classifiers,

    # Non-metadata (mostly)
    py_modules=[],
    zip_safe=False,
    install_requires=install_requires,
    extras_require={},
    scripts=['bin/compose-mode'],
    package_data={},
)
