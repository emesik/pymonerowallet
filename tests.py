#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2016 Carl Chenet <chaica@backupcheckerproject.org>
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Unit tests for PyMoneroWallet
'''Unit tests for PyMoneroWallet'''

import sys
import unittest

from monerowallet import MoneroWallet
from mockapi import MockApi

class TestPyMoneroWallet(unittest.TestCase):
    '''TestPyMoneroWallet class'''

    def setUp(self):
        self.ma = MockApi('mockapi.ini')
        self.mwa = MoneroWallet(port=8000, path='/')

    def test_getaddress(self):
        '''Test the getaddress method'''
        mockaddress = self.mwa.getaddress()
        self.assertEqual(mockaddress, "427ZuEhNJQRXoyJAeEoBaNW56ScQaLXyyQWgxeRL9KgAUhVzkvfiELZV7fCPBuuB2CGuJiWFQjhnhhwiH1FsHYGQGaDsaBA")

    def tearDown(self):
        self.ma.shutdown()

################################################################
#
# End of the unit tests
#
################################################################

if __name__ == '__main__':
    unittest.main()
