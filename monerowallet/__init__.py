# -*- coding: utf-8 -*-

"""
    The ``monerowallet`` module
    =============================
 
    Provide pythonic way to request a Monero wallet.
 
    :Example:
 
    >>> import monerowallet
    >>> mw = monerowallet.MoneroWallet()
    >>> mw.getaddress()
    '94EJSG4URLDVwzAgDvCLaRwFGHxv75DT5MvFp1YfAxQU9icGxjVJiY8Jr9YF1atXN7UFBDx3vJq2s3CzULkPrEAuEioqyrP'
 

"""
# standard library imports
import json

# 3rd party library imports
import requests

# our own library imports
from monerowallet.exceptions import MethodNotFoundError
from monerowallet.exceptions import StatusCodeError
from monerowallet.exceptions import Error

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

        :return: A dictionary with the wallet balance and the unlocked balance
        :rtype: dict

        :Example:
 
        >>> mw.getbalance()
        {'unlocked_balance': 2262265030000, 'balance': 2262265030000}

        '''
        # prepare json content
        jsoncontent = b'{"jsonrpc":"2.0","id":"0","method":"getbalance"}'
        return self.__sendrequest(jsoncontent)

    def getaddress(self):
        '''
            Return the wallet's address.

        :return: A string with the address of the wallet
        :rtype: str

        :Example:
 
        >>> mw.getaddress()
        '94EJSG4URLDVwzAgDvCLaRwFGHxv75DT5MvFp1YfAxQU9icGxjVJiY8Jr9YF1atXN7UFBDx3vJq2s3CzULkPrEAuEioqyrP'

        '''
        # prepare json content
        jsoncontent = b'{"jsonrpc":"2.0","id":"0","method":"getaddress"}'
        return self.__sendrequest(jsoncontent)['address']

    def getheight(self):
        '''
            Returns the wallet's current block height.

        :return: An integer with the wallet's current block height
        :rtype: int

        :Example:
 
        >>> mw.getheight()
        1146043

        '''
        # prepare json content
        jsoncontent = b'{"jsonrpc":"2.0","id":"0","method":"getheight"}'
        return self.__sendrequest(jsoncontent)['height']

    def transfer(self, destinations):
        '''
            Send monero to a number of recipients.

        :param destinations: a list of destinations to receive XMR
        :return: a dict of with the hash and the key of the transaction

        :Example:

        >>> mw.transfer([{'amount': 10000000000, 'address': '51EqSG4URLDFfzSxvRBUxTLftcMM76DT3MvFp3JNJRih2icqrjVJiY5Jr2YF1atXN7UFBDx4vKq4s3ozUpkwrEAuEioqyPY'}])
        {'tx_hash': 'd4d0048c275e816ae1f6f55b4b04f7d508662679c044741db2aeb7cd63452059', 'tx_key': ''}

        '''
        finalrequest = b'{"jsonrpc":"2.0","id":"0","method":"transfer","params":{"destinations":DESTLIST}}}'
        dests = json.dumps(destinations)
        jsoncontent = finalrequest.replace(b'DESTLIST', dests.encode())
        return self.__sendrequest(jsoncontent)

    def transfer_split(self, destinations):
        '''
            Send monero to a number of recipients.

        :param destinations: a list of destinations to receive XMR
        :return: a list with the transaction hashes
        :rtype: list

        :Example:

        >>> mw.transfer_split([{'amount': 10000000000, 'address': '59EqSG5UKBDFfzSxvRABxTLftcNM77DT3MvFp4JNJRLh3KCTrjBJiY4Jr9YB2atXN7UFBDx4vKq4s3ozUpkwrEAuEioqyBP'}, {'amount': 10000000000, 'address': '12EqFG3DCSDFfzSx5RBUxTLftcNM43DT2MvFp2JNJRih4444rjVJFY8Jr9YF2AtXN7UFBDx4vKq4s3ozUKkwrVAuAi55yCC'}])
        ['653a5da2dd541ab4b3d9811f84255bb243dd7338c1218c5e75036725b6ca123e']

        '''
        finalrequest = b'{"jsonrpc":"2.0","id":"0","method":"transfer_split","params":{"destinations":DESTLIST}}}'
        dests = json.dumps(destinations)
        jsoncontent = finalrequest.replace(b'DESTLIST', dests.encode())
        return self.__sendrequest(jsoncontent)['tx_hash_list']

    def sweep_dust(self):
        '''
            Send all dust outputs back to the wallet's, to make them easier to spend (and mix).

            :return: a list of the hashes of the transactions
            :rtype: list

            :example:

            >>> mw.sweep_dust()
            []

        '''
        # prepare json content
        jsoncontent = b'{"jsonrpc":"2.0","id":"0","method":"sweep_dust"}'
        result = self.__sendrequest(jsoncontent)
        if type(result) is type({}) and not result:
            return []
        else:
            return result['tx_hash_list']

    def store(self):
        '''
            Save the blockchain.

        :return: An empty dictionary
        :rtype: dict

        :Example:
 
        >>> mw.store()
        {}
        
        '''
        # prepare json content
        jsoncontent = b'{"jsonrpc":"2.0","id":"0","method":"store"}'
        return self.__sendrequest(jsoncontent)

    def get_payments(self, payment_id):
        '''
            Get a list of incoming payments using a given payment id.

        :param payment_id: Payment id
        :type payment_id: str
        :return: A list of dictionaries with the details of the incoming payments
        :rtype: list

        :Example:
 
        >>> mw = MoneroWallet()
        >>> mw.get_payments('fdfcfd993482b58b')
        [{'unlock_time': 0, 'amount': 1000000000, 'tx_hash': 'db3870905ce3c8ca349e224688c344371addca7be4eb36d5dbc61600c8f75726', 'block_height': 1157951, 'payment_id': 'fdfcfd993482b58b'}]

        '''
        # prepare json content
        jsoncontent = b'{"jsonrpc":"2.0","id":"0","method":"get_payments","params":{"payment_id":"PAYMENTID"}}'
        jsoncontent = jsoncontent.replace(b'PAYMENTID', payment_id.encode())
        result = self.__sendrequest(jsoncontent)
        if type(result) is type({}) and not result:
            return []
        else:
            return result['payments']

    def get_bulk_payments(self,payment_ids, min_block_height):
        '''
            Get a list of incoming payments using a given payment id, or a list of payments ids, from a given height.
            This method is the preferred method over get_payments because it has the same functionality but is more extendable.
            Either is fine for looking up transactions by a single payment ID.

        :param payment_ids: A list of incoming payments
        :type payment_ids: list
        :return: A list of dictionaries with the details of the incoming payments
        :rtype: dict

        :Example:
 
        >>> mw.get_bulk_payments(['94dd4c2613f5919d'], 1148609)
        >>> mw.get_bulk_payments(['fdfcfd993482b58b'], 1157950)
        [{'unlock_time': 0, 'amount': 1000000000, 'tx_hash': 'db3870905ce3c8ca349e224688c344371addca7be4eb36d5dbc61600c8f75726', 'block_height': 1157951, 'payment_id': 'fdfcfd993482b58b'}]
        
        '''
        # prepare json content
        jsoncontent = b'{"jsonrpc":"2.0","id":"0","method":"get_bulk_payments","params":{"payment_ids":[PAYMENTIDS],"min_block_height":HEIGHT}}'
        payments_list = ['"{}"'.format(i) for i in payment_ids]
        payments_to_str = ','.join(payments_list) 
        jsoncontent = jsoncontent.replace(b'PAYMENTIDS', payments_to_str.encode())
        jsoncontent = jsoncontent.replace(b'HEIGHT', str(min_block_height).encode())
        result = self.__sendrequest(jsoncontent)
        if type(result) is type({}) and not result:
            return []
        else:
            return result['payments']

    def incoming_transfers(self, transfer_type='all'):
        """
            Return a list of incoming transfers to the wallet.

        :param transfer_type: The transfer type ('all', 'available' or 'unavailable')
        :type transfer_type: str
        :return: A list with the incoming transfers
        :rtype: list

        :Example:
 
        >>> import pprint # just useful for a nice display of data
        >>> pprint.pprint(mw.incoming_transfers())
        [{'amount': 30000,
                                   'global_index': 4593,
                                   'spent': False,
                                   'tx_hash': '0a4562f0bfc4c5e7123e0ff212b1ca810c76a95fa45b18a7d7c4f123456caa12',
                                   'tx_size': 606},
                                  {'amount': 5000000,
                                   'global_index': 23572,
                                   'spent': False,
                                   'tx_hash': '1a4567f0afc7e5e7123e0aa192b2ca101c75a95ba12b53a1d7c4f871234caa11',
                                   'tx_size': 606},
        ]

        """
        # prepare json content
        jsoncontent = b'{"jsonrpc":"2.0","id":"0","method":"incoming_transfers","params":{"transfer_type":"TYPE"}}'
        jsoncontent = jsoncontent.replace(b'TYPE', transfer_type.encode())
        return self.__sendrequest(jsoncontent)['transfers']

    def query_key(self, key_type='mnemonic'):
        '''
            Return the spend or view private key.

        :param key_type: Which key to retrieve ('mnemonic' or 'view_key', default is 'mnemonic')
        :type key_type: str
        :return: A string with either the mnemonic-format key either the hexadecimal-format key
        :rtype: str

        :Example:
 
        >>> mw.query_key(key_type='mnemonic')
        'adapt adapt nostril using suture tail faked relic huddle army gags bugs abyss wield tidy jailed ridges does stacking karate hockey using suture tail faked'
        >>> mw.query_key(key_type='view_key')
        '49c087c10112eea3554d85bc9813c57f8bbd1cac1f3abb3b70d12cbea712c908'
        
        '''
        jsoncontent = b'{"jsonrpc":"2.0","id":"0","method":"query_key","params":{"key_type":"KEYTYPE"}}'
        jsoncontent = jsoncontent.replace(b'KEYTYPE', key_type.encode())
        return self.__sendrequest(jsoncontent)['key']


    def make_integrated_address(self, payment_id=''):
        '''
            Make an integrated address from the wallet address and a payment id.

        :param payment_id: Specific payment id. Otherwise it is randomly generated
        :type payment_id: str
        :return: A dictionary with both integrated address and payment id
        :rtype: dict

        :Example:

        >>> mw.make_integrated_address()
        {'integrated_address': '4JwWT4sy2bjFfzSxvRBUxTLftcNM98DT5MvFp4JNJRih3icqrjVJiY8Jr9YF1atXN7UFBDx4vKq4s3ozUpkwrEAuMLBRqCy9Vhg9Y49vcq', 'payment_id': '8c9a5fd001c3c74b'}

        '''
        if not payment_id:
            jsoncontent = b'{"jsonrpc":"2.0","id":"0","method":"make_integrated_address","params":{"payment_id":""}}'
        else:
            jsoncontent = b'{"jsonrpc":"2.0","id":"0","method":"make_integrated_address","params":{"payment_id":"PAYMENTID"}}'
            jsoncontent = jsoncontent.replace(b'PAYMENTID', payment_id.encode())
        return self.__sendrequest(jsoncontent)

    def split_integrated_address(self, integrated_address):
        '''
            Retrieve the standard address and payment id corresponding to an integrated address.

            :param integrated_address: the integrated address to split
            :type integrated_address: str
            :return: a dictionary with the payment id and the standard address
            :rtype: dict

            :example:

            >>> mw.split_integrated_address('4JwWT4sy2bjFfzSxvRBUxTLftcNM98DT5MvFp4JNJRih3icqrjVJiY8Jr9YF1atXN7UFBDx4vKq4s3ozUpkwrEAuMLBRqCy9Vhg9Y49vcq')
            {'standard_address': '12GLv8KzVhxehv712FWPTF7CSWuVjuBarFd17QP163uxMaFyoqwmDf1aiRtS5jWgCkRsk12ycdBNJa6V4La8joznK4GAhcq', 'payment_id': '1acca0543e3082fa'}

        '''
        jsoncontent = b'{"jsonrpc":"2.0","id":"0","method":"split_integrated_address","params":{"integrated_address":"INTEGRATEDADDRESS"}}'
        jsoncontent = jsoncontent.replace(b'INTEGRATEDADDRESS', integrated_address.encode())
        return self.__sendrequest(jsoncontent)

    def stop_wallet(self):
        '''
            Stops the wallet, storing the current state.

        :return: An empty dictionary
        :rtype: dict

        :Example:
 
        >>> mw.stop_wallet()
        {}
        
        '''
        jsoncontent = b'{"jsonrpc":"2.0","id":"0","method":"stop_wallet"}'
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
        result = req.json()
        # manage returned http status code 
        if req.status_code != 200:
            raise StatusCodeError('Unexpected returned status code: {}'.format(req.status_code))
        # if server-side error is detected, print it
        if 'error' in result:
            if result['error']['message'] == 'Method not found':
                raise MethodNotFoundError('Unexpected method while requesting the server: {}'.format(jsoncontent))
            else:
                raise Error('Error: {}'.format(str(result)))
        # otherwise return result
        return result['result']
