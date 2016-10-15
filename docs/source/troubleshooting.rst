Troubleshooting
===============
The main issue you can encounter is the following error::

    >>> from monerowallet import MoneroWallet
    >>> mw = MoneroWallet()
    >>> mw.getaddress()
    ConnectionRefusedError: [Errno 111] Connection refused
    ...
    requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=18082): Max retries exceeded with url: /json_rpc (Caused by NewConnectionError('<requests.packages.urllib3.connection.HTTPConnection object at 0x7f852251a080>: Failed to establish a new connection: [Errno 111] Connection refused',))

It means the RPC server of your Monero wallet is not listening of the dedicated port and so can not reply to requests. Launch it as described in the Use section. For other errors, have a look at the monerowallet.exceptions module or open a bug report.
