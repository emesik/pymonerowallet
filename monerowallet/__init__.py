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

        :param protocol: Protocol for requesting the RCP server ('http' or 'https, defaults to 'http')
        :type protocol: str
        :param host: The host for requesting the RCP server (defaults to '127.0.0.1')
        :type protocol: str
        :param port: The port for requesting the RCP server (defaults to 18082)
        :type port: str
        :param uri: The uri for requesting the RCP server (defaults to '/json_rpc')
        :type uri: str
        :return: A MoneroWallet object
        :rtype: MoneroWallet

        :Example:
 
        >>> mw = MoneroWallet()

    '''

    def __init__(self, protocol='http', host='127.0.0.1', port=18082, uri='/json_rpc'):
        #self.server = {'protocol': 'http', 'host': '127.0.0.1', 'port': 18082, 'uri': '/json_rpc'}
        self.server = {'protocol': protocol, 'host': host, 'port': port, 'uri': uri}

    def getbalance(self):
        '''
            Return the wallet's balance.

        :return: A dictionary with the status of the request and the wallet balance
        :rtype: dict

        :Example:
 
        >>> mw.getbalance()
        2

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
        2

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
        2

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

        :return: A dictionary with the status of the request and
        :rtype: dict

        :Example:
 
        >>> mw.store()
        
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
 
        >>> mw.incoming_transfers('all')
        
        """
        jsoncontent = open('json/incomingtransfers.json', 'rb').read()
        jsoncontent = jsoncontent.replace(b'TYPE', transfer_type.encode())
        return self.__sendrequest(jsoncontent)

    def query_key(self):
        '''Return the spend or view private key.'''
        pass

    def make_integrated_address(self):
        '''Make an integrated address from the wallet address and a payment id.'''
        pass

    def split_integrated_address(self):
        '''Retrieve the standard address and payment id corresponding to an integrated address.'''
        pass

    def stop_wallet(self):
        '''
            Stops the wallet, storing the current state.

        :return: A dictionary with the status of the request and
        :rtype: dict

        :Example:
 
        >>> mw.stop_wallet()
        
        '''
        jsoncontent = open('json/stopwallet.json', 'rb').read()
        return self.__sendrequest(jsoncontent)

    def __sendrequest(self, jsoncontent):
        '''Send a request to the server'''
        self.headers = {'Content-Type': 'application/json'}
        req = requests.post('{protocol}://{host}:{port}{uri}'.format(protocol=self.server['protocol'],
                                                                     host=self.server['host'],
                                                                     port=self.server['port'],
                                                                     uri=self.server['uri']),
                                                                     headers=self.headers,
                                                                     data=jsoncontent)
        if req.status_code >= 200 and req.status_code <= 299:
            return {'status': req.status_code, 'result': req.json()['result']}
        else:
            return {'status': req.status_code, 'result': {}}
