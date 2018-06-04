# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import codecs
import os
import runpy
import subprocess
from setuptools import setup, find_packages
from distutils.command.build import build
try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    bdist_wheel = None


class CustomBuild(build):
    def run(self):
        build.run(self)
        subprocess.check_call(['make'], cwd='./build/lib/vimtips/unblank_check')


if bdist_wheel is not None:
    class CustomBdistWheel(bdist_wheel):
        def finalize_options(self):
            bdist_wheel.finalize_options(self)
            self.root_is_pure = False  # force the build of platform specific wheels
else:
    CustomBdistWheel = None


def get_version_from_pyfile(version_file='vimtips/_version.py'):
    file_globals = runpy.run_path(version_file)
    return file_globals['__version__']


def get_install_requires_from_requirements(requirements_filename='requirements.txt'):
    try:
        with codecs.open(requirements_filename, 'r', 'utf-8') as requirements_file:
            requirements = requirements_file.readlines()
    except OSError:
        import logging
        logging.warning('Could not read the requirements file.')
    return requirements


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


version = get_version_from_pyfile()
long_description = get_long_description_from_readme()
install_requires = get_install_requires_from_requirements()

setup(
    name='vimtips',
    version=version,
    packages=find_packages(),
    python_requires='~=3.3',
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'vimtips = vimtips.cli:main',
            'vimtips-daemon = vimtips.unblank_daemon:main',
        ],
        'gui_scripts': [
            'vimtips-gui = vimtips.gui:main',
        ]
    },
    cmdclass={
        'build': CustomBuild,
        'bdist_wheel': CustomBdistWheel
    },
    author='Ingo Heimbach',
    author_email='IJ_H@gmx.de',
    description='Vim Tips is a project to aggregate and show vim tips from different sources.',
    long_description=long_description,
    license='MIT',
    url='https://github.com/IngoHeimbach/vimtips',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Text Editors',
        'Topic :: Utilities'
    ]
)
