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

PyMoneroWallet 0.1 was only tested with Monero 0.10.0.0

### Use PyMoneroWallet


#### Get the balance and the unlocked balance of the wallet

        $ python3
        >>> from monerowallet import MoneroWallet
        >>> mw = MoneroWallet()
        >>> mw.getbalance()
        {'unlocked_balance': 2262265030000, 'balance': 2262265030000}

#### Transfer Monero to a given address

        >>> mw.transfer([{'amount': 10000000000, 'address': '51EqSG4URLDFfzSxvRBUxTLftcMM76DT3MvFp3JNJRih2icqrjVJiY5Jr2YF1atXN7UFBDx4vKq4s3ozUpkwrEAuEioqyPY'}])
        {'tx_hash': 'd4d0048c275e816ae1f6f55b4b04f7d508662679c044741db2aeb7cd63452059', 'tx_key': ''}

The complete documentation about using PyMoneroWallet is available in docs/ or [online](https://pymonerowallet.readthedocs.org/en/latest).

### Authors

Carl Chenet <chaica@ohmytux.com>
Cryptobadger <cryptobadger@riseup.net>


### License

This software comes under the terms of the GPLv3+. See the LICENSE file for the complete text of the license.
