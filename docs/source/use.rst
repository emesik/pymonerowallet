Use the PyMoneroWallet library
==============================
The first thing you need to install the Monero wallet 10.0.0::

    $ mkdir monero_0.10.0.0
    $ cd monero_0.10.0.0
    $ wget https://downloads.getmonero.org/monero.linux.x64.v0-10-0-0.tar.bz2
    $ tar jxvf monero.linux.x64.v0-10-0-0.tar.bz2

Now you need to synchronize your Monero wallet::

    $ monerod

Once you are synchronized, you need to launch your Monero wallet for the first time to define your wallet password::

    $ monero-wallet-cli

After having creating your Monero wallet and define your password, you need to launch your Monero wallet activating the RPC calls::

    $ monero-wallet-cli --wallet-file monerowallet --password 'v3rY S3cr3t P4sSw0rd' --rpc-bind-ip 127.0.0.1 --rpc-bind-port 1808

Now we are ready to use the PyMoneroWallet library with Python3::

    $ python3
    >>> from monerowallet import MoneroWallet
    >>> mw = MoneroWallet()
    >>> mw.getbalance()
    {'unlocked_balance': 2262265030000, 'balance': 2262265030000}

To get extensive details about available methods, see the documentation of the monerowallet module.
