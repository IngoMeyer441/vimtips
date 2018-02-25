# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import codecs
import os
import subprocess
from setuptools import setup, find_packages
from vimtips._version import __version__


def get_long_description_from_readme(readme_filename='README.md'):
    rst_filename = '{}.rst'.format(os.path.splitext(os.path.basename(readme_filename))[0])
    created_tmp_rst = False
    if not os.path.isfile(rst_filename):
        try:
            subprocess.check_call(['pandoc', readme_filename, '-t', 'rst', '-o', rst_filename])
            created_tmp_rst = True
        except (OSError, subprocess.CalledProcessError):
            import logging
            logging.warning('Could not convert the readme file to rst.')
    long_description = None
    if os.path.isfile(rst_filename):
        with codecs.open(rst_filename, 'r', 'utf-8') as readme_file:
            long_description = readme_file.read()
    if created_tmp_rst:
        os.remove(rst_filename)
    return long_description


long_description = get_long_description_from_readme()

setup(
    name='vimtips',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'PyQt5',
        'tweepy'
    ],
    entry_points={
        'console_scripts': [
            'vimtips = vimtips.cli:main',
        ],
        'gui_scripts': [
            'vimtips-gui = vimtips.gui:main',
        ]
    },
    author='Ingo Heimbach',
    author_email='IJ_H@gmx.de',
    description='description',
    long_description=long_description,
    license='MIT',
    url='url',
    keywords=['vim', 'tips'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Text Editors',
        'Topic :: Utilities'
    ]
)
