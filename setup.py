# -*- coding: utf-8 -*-
# Copyright © 2016 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# Setup for PyMoneroWallet 
'''Setup for PyMoneroWallet'''

# standard library imports
import os.path

# external library imports
from setuptools import setup

CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Environment :: Console',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.4'
]

setup(
    name='pymonerowallet',
    version='0.1',
    license='GNU GPL v3',
    description='Python library to query a Monero wallet',
    long_description='Python library to query a Monero wallet',
    classifiers=CLASSIFIERS,
    author='Carl Chenet',
    author_email='chaica@ohmytux.com',
    url='https://github.com/chaica/pymonerowallet',
    download_url='https://github.com/chaica/pymonerowallet',
    packages=['monerowallet','monerowallet.exceptions'],
    install_requires=['requests'],
    test_suite = 'tests',
)
