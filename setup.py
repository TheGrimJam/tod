#!/usr/bin/env python3
"""
Mr Setup File for Mr Tod 
"""
from setuptools import setup, find_packages
from io import open
from os import path

import pathlib
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
config_file = path.join(HERE, 'tod', 'config.py')

# automatically captured required modules for install_requires in requirements.txt and as well as configure dependency links
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
    install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]


dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]

setup (
 name = 'TOD',
 description = 'A very very simple interface for todoist. There are better ones.',
 version = '1.0.0',
 packages = find_packages(), # list of all packages
 install_requires = install_requires,
 python_requires='>=2.7', # any python greater than 2.7
 entry_points='''
        [console_scripts]
        tod=tod.tod
    ''',
 author="Gavin McCormack",
 long_description=README,
 long_description_content_type="text/markdown",
 license='MIT',
 url='https://github.com/TheGrimJam/tod',
 download_url='https://github.com/TheGrimJam/tod/1.0.0.tar.gz',
  dependency_links=dependency_links,
  author_email='info@jamdigital.tech',
  classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ]
)