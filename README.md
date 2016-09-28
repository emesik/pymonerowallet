### Python library for the Monero Wallet

PyMoneroWallet is a Python library to query a Monero wallet.
Full official documentation available [online](https://pymonerowallet.readthedocs.org/en/latest/).

### Quick Install

* Install PyMoneroWallet from PyPI

        # pip3 install pymonerowallet

* Install PyMoneroWallet from sources    
  *(see the installation guide for full details)
  [Installation Guide](http://pymonerowallet.readthedocs.org/en/latest/install.html)*
  

        # tar zxvf pymonerowallet-0.1.tar.gz
        # cd pymonerowallet
        # python3.4 setup.py install
        # # or
        # python3.4 setup.py install

### Use PyMoneroWallet

        $ python3
        Python 3.4.2 (default, Oct  8 2014, 10:45:20) 
        [GCC 4.9.1] on linux
        Type "help", "copyright", "credits" or "license" for more information.
        >>> from monerowallet import MoneroWallet
        >>> mw = MoneroWallet()
        >>> mw.getbalance()
        {'result': {'unlocked_balance': 2262265030000, 'balance': 2262265030000}, 'status': 200}

The complete documentation about using PyMoneroWallet is available in docs/ or [online](https://pymonerowallet.readthedocs.org/en/latest).


### Authors

Carl Chenet <chaica@ohmytux.com>

### License

This software comes under the terms of the GPLv3+. See the LICENSE file for the complete text of the license.
