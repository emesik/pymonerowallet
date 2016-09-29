# -*- coding: utf-8 -*-

"""
    The ``monerowallet`` module
    =============================
 
    Provide pythonic way to request a Monero wallet.
 
    :Example:
 
    >>> import monerowallet
    >>> mw = monerowallet.MoneroWallet()
    >>> mw.getaddress()
    94EJSG4URLDVwzAgDvCLaRwFGHxv75DT5MvFp1YfAxQU9icGxjVJiY8Jr9YF1atXN7UFBDx3vJq2s3CzULkPrEAuEioqyrP
 

"""

import requests

class MoneroWallet(object):
    '''
        The MoneroWallet class. Instantiate a MoneroWallet object with parameters
        to  dialog with the RPC wallet server.

        :param protocol: Protocol for requesting the RPC server ('http' or 'https, defaults to 'http')
        :type protocol: str
        :param host: The host for requesting the RPC server (defaults to '127.0.0.1')
        :type protocol: str
        :param port: The port for requesting the RPC server (defaults to 18082)
        :type port: str
        :param path: The path for requesting the RPC server (defaults to '/json_rpc')
        :type path: str
        :return: A MoneroWallet object
        :rtype: MoneroWallet

        :Example:
 
        >>> mw = MoneroWallet()
        >>> mw
        <monerowallet.MoneroWallet object at 0x7fe09e4e8da0>

    '''

    def __init__(self, protocol='http', host='127.0.0.1', port=18082, path='/json_rpc'):
        self.server = {'protocol': protocol, 'host': host, 'port': port, 'path': path}

    def getbalance(self):
        '''
            Return the wallet's balance.

        :return: A dictionary with the status of the request and the wallet balance
        :rtype: dict

        :Example:
 
        >>> mw.getbalance()
        {'result': {'unlocked_balance': 2262265030000, 'balance': 2262265030000}, 'status': 200}

        '''
        # prepare json content
        jsoncontent = open('json/getbalance.json', 'rb').read()
        return self.__sendrequest(jsoncontent)

    def getaddress(self):
        '''
            Return the wallet's address.

        :return: A dictionary with the status of the request and the address of the wallet
        :rtype: dict

        :Example:
 
        >>> mw.getaddress()
        {'result': {'address': '94EJSG4URLDVwzAgDvCLaRwFGHxv75DT5MvFp1YfAxQU9icGxjVJiY8Jr9YF1atXN7UFBDx3vJq2s3CzULkPrEAuEioqyrP'}, 'status': 200}

        '''
        jsoncontent = open('json/getaddress.json', 'rb').read()
        return self.__sendrequest(jsoncontent)

    def getheight(self):
        '''
            Returns the wallet's current block height.

        :return: A dictionary with the status of the request and the wallet's current block height
        :rtype: dict

        :Example:
 
        >>> mw.getheight()
        {'result': {'height': 1146043}, 'status': 200}

        '''
        jsoncontent = open('json/getheight.json', 'rb').read()
        return self.__sendrequest(jsoncontent)

    def transfer(self):
        '''Send monero to a number of recipients.'''
        pass


    def transfer_split(self):
        '''Same as transfer, but can split into more than one tx if necessary.'''
        pass

    def sweep_dust(self):
        '''Send all dust outputs back to the wallet's, to make them easier to spend (and mix).'''
        jsoncontent = open('json/sweepdust.json', 'rb').read()
        return self.__sendrequest(jsoncontent)

    def store(self):
        '''
            Save the blockchain.

        :return: A dictionary with the status of the request and an empty dictionary for the result key
        :rtype: dict

        :Example:
 
        >>> mw.store()
        {'result': {}, 'status': 200
        
        '''
        jsoncontent = open('json/store.json', 'rb').read()
        return self.__sendrequest(jsoncontent)

    def get_payments(self):
        '''Get a list of incoming payments using a given payment id.'''
        pass

    def get_bulk_payments(self):
        '''Get a list of incoming payments using a given payment id, or a list of payments ids, from a given height. This method is the preferred method over get_payments because it has the same functionality but is more extendable. Either is fine for looking up transactions by a single payment ID.'''
        pass

    def incoming_transfers(self, transfer_type='all'):
        """
            Return a list of incoming transfers to the wallet.

        :param transfer_type: The transfer type ('all', 'available' or 'unavailable')
        :type transfer_type: str
        :return: A dictionary with the status of the request and
        :rtype: dict

        :Example:
 
        >>> import pprint # just useful for a nice display of data
        >>> pprint.pprint(mw.incoming_transfers())
        {'result': {'transfers': [{'amount': 30000,
                                   'global_index': 4593,
                                   'spent': False,
                                   'tx_hash': '0a4562f0bfc4c5e7123e0ff212b1ca810c76a95fa45b18a7d7c4f123456caa12',
                                   'tx_size': 606},
                                  {'amount': 5000000,
                                   'global_index': 23572,
                                   'spent': False,
                                   'tx_hash': '1a4567f0afc7e5e7123e0aa192b2ca101c75a95ba12b53a1d7c4f871234caa11',
                                   'tx_size': 606}}]},
         'status': 200}
        
        """
        jsoncontent = open('json/incomingtransfers.json', 'rb').read()
        jsoncontent = jsoncontent.replace(b'TYPE', transfer_type.encode())
        return self.__sendrequest(jsoncontent)

    def query_key(self, key_type='mnemonic'):
        '''
            Return the spend or view private key.

        :param key_type: Which key to retrieve ('mnemonic' or 'view_key', default is 'mnemonic')
        :type key_type: str
        :return: A dictionary with the status of the request and the key to retrieve
        :rtype: dict

        :Example:
 
        >>> mw.query_key(key_type='mnemonic')
        {'status': 200, 'result': {'key': 'adapt adapt nostril using suture tail faked relic huddle army gags bugs abyss wield tidy jailed ridges does stacking karate hockey using suture tail faked'}}
        >>> mw.query_key(key_type='view_key')
        {'status': 200, 'result': {'key': '49c087c10112eea3554d85bc9813c57f8bbd1cac1f3abb3b70d12cbea712c908'}}
        
        '''
        jsoncontent = open('json/querykey.json', 'rb').read()
        jsoncontent = jsoncontent.replace(b'KEYTYPE', key_type.encode())
        return self.__sendrequest(jsoncontent)


    def make_integrated_address(self):
        '''Make an integrated address from the wallet address and a payment id.'''
        pass

    def split_integrated_address(self):
        '''Retrieve the standard address and payment id corresponding to an integrated address.'''
        pass

    def stop_wallet(self):
        '''
            Stops the wallet, storing the current state.

        :return: A dictionary with the status of the request and an empty result dictionary
        :rtype: dict

        :Example:
 
        >>> mw.stop_wallet()
        {'status': 200, 'result': {}}
        
        '''
        jsoncontent = open('json/stopwallet.json', 'rb').read()
        return self.__sendrequest(jsoncontent)

    def __sendrequest(self, jsoncontent):
        '''Send a request to the server'''
        self.headers = {'Content-Type': 'application/json'}
        req = requests.post('{protocol}://{host}:{port}{path}'.format(protocol=self.server['protocol'],
                                                                     host=self.server['host'],
                                                                     port=self.server['port'],
                                                                     path=self.server['path']),
                                                                     headers=self.headers,
                                                                     data=jsoncontent)
        if req.status_code >= 200 and req.status_code <= 299:
            return {'status': req.status_code, 'result': req.json()['result']}
        else:
            return {'status': req.status_code, 'result': {}}
