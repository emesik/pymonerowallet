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
from decimal import Decimal
import json
import logging

# 3rd party library imports
import requests

# our own library imports
from monerowallet import exceptions

_log = logging.getLogger(__name__)


class MoneroWallet(object):
    '''
    The MoneroWallet class. Instantiate a MoneroWallet object with parameters
    to  dialog with the RPC wallet server.

    :param protocol: Protocol for requesting the RPC server ('http' or 'https, defaults to 'http')
    :type protocol: str
    :param host: The host for requesting the RPC server (defaults to '127.0.0.1')
    :type protocol: str
    :param port: The port for requesting the RPC server (defaults to 18082)
    :type port: int
    :param path: The path for requesting the RPC server (defaults to '/json_rpc')
    :type path: str
    :param rpcuser: The username to log in to the RPC server (defaults to 'default')
    :type rpcuser: str
    :param rpcpassword: The password to log in to the RPC server (defaults to 'default')
    :type rpcpassword: str

    :return: A MoneroWallet object
    :rtype: MoneroWallet

    :Example:

    >>> mw = MoneroWallet()
    >>> mw
    <monerowallet.MoneroWallet object at 0x7fe09e4e8da0>

    '''

    def __init__(self, protocol='http', host='127.0.0.1', port=18082, path='/json_rpc', rpcuser='default', rpcpassword='default'):
        self.server = {'protocol': protocol, 'host': host, 'port': port, 'path': path, 'rpcuser': rpcuser, 'rpcpassword': rpcpassword}

    def getbalance(self, account_index=0):
        '''
        Return the account's balance.

        :param account_index: Index of the account to check balance for
        :type account_index: int
        :return: A dictionary with the wallet balance, unlocked balance and a list of subaddresses with their balances
        :rtype: dict

        :Example:

        >>> mw.getbalance()
        {'unlocked_balance': 2262265030000, 'balance': 2262265030000}

        :Example with subaddresses:

        >>> mw.getbalance()
        {'balance': 31976252778736417, 'per_subaddress': [{'address': '9u9j6xG1GNu4ghrdUL35m5PQcJV69YF8731DSTDoh7pDgkBWz2LWNzncq7M5s1ARjPRhvGPX4dBUeC3xNj4wzfrjV6SY3e9', 'address_index': 0, 'balance': 31776252778736417, 'label': 'Primary account', 'num_unspent_outputs': 8519, 'unlocked_balance': 30829196841324088}, {'address': 'BcUqEB1xnpBV2T3E9oYRwgGSzCGTEkDGD3zAEW1on9UMXBoRT7PBZfLTWjA6wgfHc824C6JxRT5N7GN74X3EehApQT4FbHR', 'address_index': 2, 'balance': 200000000000000, 'label': '(Untitled address)', 'num_unspent_outputs': 26, 'unlocked_balance': 200000000000000}], 'unlocked_balance': 31029196841324088}

        '''
        return self.__sendrequest("getbalance", {'account_index': account_index})

    def getaddress(self, account_index=0):
        '''
        Return the account's address.

        :param account_index: Index of the account to get address for
        :type account_index: int
        :return: A string with the address of the account
        :rtype: str

        :Example:

        >>> mw.getaddress()
        '94EJSG4URLDVwzAgDvCLaRwFGHxv75DT5MvFp1YfAxQU9icGxjVJiY8Jr9YF1atXN7UFBDx3vJq2s3CzULkPrEAuEioqyrP'

        '''
        return self.__sendrequest("getaddress", {'account_index': account_index})['address']

    def create_address(self, account_index=0, label=None):
        '''
        Create new subaddress.

        :param account_index: Index of the account to create address within
        :type account_index: int
        :param label: Label for the new address
        :type label: str
        :return: A dictionary with new subaddress and its' index within account.
        :rtype: dict

        :Example:

        >>> mw.create_address()
        {'address': 'BgZRz9ow9UUjU2ZhhJGLejDLACY7Tf74UGQjaD8YpVguYH76A8RZGC27hLgTGDo38mBaP78vyTFQbM1oV7YSuMjH3Wj5iBj', 'address_index': 3}
        '''
        return self.__sendrequest("create_address", {'account_index': account_index, 'label': label})

    def label_address(self, account_index=0, address_index=0, label=None):
        return self.__sendrequest(
            "label_address", {
                'index': { 'major': account_index, 'minor': address_index },
                'label': label})

    def get_accounts(self):
        return self.__sendrequest("get_accounts")

    def create_account(self, label=None):
        return self.__sendrequest("create_account", { 'label': label })

    def getheight(self):
        '''
        Returns the wallet's current block height.

        :return: An integer with the wallet's current block height
        :rtype: int

        :Example:

        >>> mw.getheight()
        1146043

        '''
        return self.__sendrequest("getheight")['height']

    def transfer(self, destinations,
            mixin=None, payment_id=None, priority=0,
            get_tx_key=True, get_tx_hex=False, unlock_time=None,
            account_index=0, subaddr_indices=None):
        '''
        Send monero to a number of recipients.

        :param destinations: a list of dicts of destinations to receive XMR. A destination is a dict consisting of two key/value pairs. The two keys are the amount (atomic units as int)  and the destination public address (str).
        :type destinations: list
        :param mixin: number of outputs from the blockchain to mix with
        :type mixin: int
        :param payment_id: 32-byte/64-character hex string to identify a transaction. If none is given a payment_id is randomly generated (defaults to None)
        :type payment_id: str
        :param priority: set a priority for the transaction (1-4 for unimportant, normal, elevated, priority; 0 = default)
        :type priority: int
        :param get_tx_key: return the transaction key after sending (defaults to True)
        :type get_tx_key: bool
        :param get_tx_hex: return the transaction as hex string after sending (defaults to False)
        :type get_tx_hex: bool
        :param unlock_time: Number of blocks before the monero can be spent (0 to not add a lock). (defaults to None)
        :type unlock_time: int
        :return: a dict with the transaction hash (tx_hash; type: str), the fee (fee; type: int), the transaction as hex string (tx_blob; type: str) if get_tx_hex was True and the key of the transaction (tx_key; type: str) if get_tx_key was True
        :rtype: dict

        :Example:

        >>> mw.transfer([{"amount":10000000,"address":"A135xq3GVMdU5qtAm4hN7zjPgz8bRaiSUQmtuDdjZ6CgXayvQruJy3WPe95qj873JhK4YdTQjoR39Leg6esznQk8PckhjRN"}])
{'fee': 20141160000, 'tx_blob': '', 'tx_hash': '04cdf47d7927895cde9d3ddf687f70c68bd6fbbd4a21bfd1c669bb3b4b670823', 'tx_key': '150926e63b78f788993cb0efd111c95026ced686735fe0daf3b5cff63fd72b0c'}

        '''
        return self.__sendrequest(
            "transfer", {
                "destinations": destinations,
                "account_index": account_index,
                "subaddr_indices": subaddr_indices,
                "mixin": mixin,
                "payment_id": payment_id,
                "priority": priority,
                "unlock_time": unlock_time,
                "get_tx_key": get_tx_key,
                "get_tx_hex": get_tx_hex,
            })

    def transfer_split(self, destinations,
            mixin=None, payment_id=None, priority=0,
            get_tx_keys=True, get_tx_hex=False,
            unlock_time=None, new_algorithm=True,
            account_index=0, subaddr_indices=None):
        '''
        Send monero to a number of recipients. Can split into more than one transaction if necessary.

        :param destinations: a list of dicts of destinations to receive XMR. A destination is a dict consisting of two key/value pairs. The two keys are the amount (atomic units as int)  and the destination public address (str).
        :type destinations: list
        :param mixin: number of outputs from the blockchain to mix with
        :type mixin: int
        :param payment_id: 32-byte/64-character hex string to identify a transaction. If none is given a payment_id is randomly generated (defaults to None)
        :type payment_id: str
        :param priority: set a priority for the transaction (1-4 for unimportant, normal, elevated, priority; 0 = default)
        :type priority: int
        :param get_tx_keys: return the transaction key after sending (defaults to True)
        :type get_tx_keys: bool
        :param get_tx_hex: return the transaction as hex string after sending (defaults to False)
        :type get_tx_hex: str
        :param unlock_time: Number of blocks before the monero can be spent (0 to not add a lock). (defaults to None)
        :type unlock_time: int
        :param new_algorithm: True to use the new transaction construction algorithm (defaults to False)
        :type new_algorithm: bool

        :return: a dict containing a list with the atomic amounts per transaction (amount_list; type:int), a list of the fees per transaction (fee_list; type: int), a list containing the transaction hashes (tx_hash_list; type: str) and a list containing the transaction keys (tx_key_list; type: str) if get_tx_key was True
        :rtype: dict of lists

        :Example:

        >>> mw.transfer_split([{"amount":10000000,"address":"A135xq3GVMdU5qtAm4hN7zjPgz8bRaiSUQmtuDdjZ6CgXayvQruJy3WPe95qj873JhK4YdTQjoR39Leg6esznQk8PckhjRN"}])
        {'amount_list': [10000000], 'fee_list': [20140120000], 'tx_hash_list': ['b2bfcffa3c69d9e2cf1bd11bd08929a8353cd72ff1c3b85ed3d049c2aea99264'], 'tx_key_list': ['f4fc52c2f09661ac2b1c5767889aac2d4636989cafa29ffb29340207080f8a07']}


        '''
        return self.__sendrequest(
            "transfer_split", {
                "destinations": destinations,
                "account_index": account_index,
                "subaddr_indices": subaddr_indices,
                "mixin": mixin,
                "payment_id": payment_id,
                "priority": priority,
                "unlock_time": unlock_time,
                "get_tx_keys": get_tx_keys,
                "get_tx_hex": get_tx_hex,
                "new_algorithm": new_algorithm
            })

    def sweep_dust(self):
        '''
        Send all dust outputs back to the wallet's, to make them easier to spend (and mix).

        :return: a list of the hashes of the transactions
        :rtype: list

        :example:

        >>> mw.sweep_dust()
        []

        '''
        result = self.__sendrequest("sweep_dust")
        if 'tx_hash_list' in result:
            return result['tx_hash_list']
        else:
            return []

    def store(self):
        '''
        Save the blockchain.

        :return: An empty dictionary
        :rtype: dict

        :Example:

        >>> mw.store()
        {}

        '''
        return self.__sendrequest("store")

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
        result = self.__sendrequest("get_payments", {"payment_id": payment_id})
        if 'payments' in result:
            return result['payments']
        else:
            return []

    def get_bulk_payments(self, payment_ids=[], min_block_height=0):
        '''
        Get a list of incoming payments using a given payment id, or a list of payments ids, from a given height.
        This method is the preferred method over get_payments because it has the same functionality but is more extendable.
        Either is fine for looking up transactions by a single payment ID.

        :param payment_ids: A list of incoming payments, gets every payment if empty list is provided. (Defaults to [])
        :type payment_ids: list
        :param min_block_height: The minimum block height from which to look
        :type min_block_height: int
        :return: A list of dictionaries with the details of the incoming payments
        :rtype: dict

        :Example:

        >>> mw.get_bulk_payments(['94dd4c2613f5919d'], 1148609)
        >>> mw.get_bulk_payments(['fdfcfd993482b58b'], 1157950)
        [{'unlock_time': 0, 'amount': 1000000000, 'tx_hash': 'db3870905ce3c8ca349e224688c344371addca7be4eb36d5dbc61600c8f75726', 'block_height': 1157951, 'payment_id': 'fdfcfd993482b58b'}]

        '''
        # prepare json content
#        jsoncontent = b'{"jsonrpc":"2.0","id":"0","method":"get_bulk_payments","params":{"payment_ids":[PAYMENTIDS],"min_block_height":HEIGHT}}'
#        payments_list = ['"{}"'.format(i) for i in payment_ids]
#        payments_to_str = ','.join(payments_list)
#        jsoncontent = jsoncontent.replace(b'PAYMENTIDS', payments_to_str.encode())
#        jsoncontent = jsoncontent.replace(b'HEIGHT', str(min_block_height).encode())
        result = self.__sendrequest("get_bulk_payments", {"payment_ids": payment_ids, "min_block_height": min_block_height})
        if isinstance(result, dict) and not result:
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
        result = self.__sendrequest("incoming_transfers", {"transfer_type": transfer_type})
        try:
            return result['transfers']
        except KeyError:
            # XXX: It would be nice of wallet RPC to return empty list here
            return []

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
        return self.__sendrequest("query_key", {"key_type": key_type})['key']

    # todo: check payment_id <= emptystring leads to error or random id?
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
        return self.__sendrequest("make_integrated_address", {"payment_id": payment_id})

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
        return self.__sendrequest("split_integrated_address", {"integrated_address": integrated_address})

    def stop_wallet(self):
        '''
            Stops the wallet, storing the current state.

        :return: An empty dictionary
        :rtype: dict

        :Example:

        >>> mw.stop_wallet()
        {}

        '''
        return self.__sendrequest("stop_wallet")

    def make_uri(self, address, amount, payment_id, recipient_name, tx_description):
        '''
        Create a payment URI using the official URI specification.


        '''
        return self.__sendrequest("make_uri", {"address": address, "amount": amount, "payment_id": payment_id, "recipient_name": recipient_name, "tx_description": tx_description})

    def create_wallet(self, filename, password, language='English'):
        '''
        Create a new wallet. The daemon should be running with --wallet-dir arg.
        '''
        return self.__sendrequest(
            "create_wallet", {
                'filename': filename,
                'password': password,
                'language': language })

    def open_wallet(self, filename, password):
        '''
        Open existing wallet. The daemon should be running with --wallet-dir arg.
        '''
        return self.__sendrequest(
            "open_wallet", {
                'filename': filename,
                'password': password })

    def __sendrequest(self, method, params={}):
        '''Send a request to the server'''
        self.headers = {'Content-Type': 'application/json'}
        data = {'jsonrpc': '2.0', 'id': '0', 'method': method}
        validparams = {}
        for key in params:
            if params[key] is not None:
                validparams[key] = params[key]
        if validparams:
            data['params'] = validparams
        _log.debug("Method: {0}, params: {1}".format(method, validparams))
        req = requests.post('{protocol}://{host}:{port}{path}'.format(protocol=self.server['protocol'],
                                                                      host=self.server['host'],
                                                                      port=self.server['port'],
                                                                      path=self.server['path']),
                            headers=self.headers,
                            data=json.dumps(data),
                            auth=requests.auth.HTTPDigestAuth(self.server['rpcuser'], self.server['rpcpassword'])
                            )

        if req.status_code == 401:
            raise exceptions.Unauthorized('401 Unauthorized. Check username and password.')
        elif req.status_code != 200:
            raise exceptions.StatusCodeError('Unexpected returned status code: {}'.format(req.status_code))
        result = req.json()
        _log.debug("Result: {0}".format(result))

        # if server-side error is detected, print it
        if 'error' in result:
            code = result['error']['code']
            message = result['error']['message']
            if code == -32601:
                raise exceptions.MethodNotFoundError(
                    'Unexpected method while requesting the server: {}'.format(
                        json.dumps(data)))
            elif code == -32602:
                raise exceptions.InvalidParamsError(
                    'Invalid parameters while requesting the server: {}'.format(
                        json.dumps(data)))
            elif code in exceptions._errorcode_to_exception.keys():
                raise exceptions._errorcode_to_exception[code](message)
            else:
                raise exceptions.Error('Error {code}: {message}'.format(**result['error']))
            # otherwise return result
        return result['result']


def atomic_to_coins(units):
    '''
    Converts Monero atomic units to Monero coins. One coin is 1e12 atomic units.

    :param units: Atomic units which are converted to coins
    :type units: int

    :return: Monero coins
    :rtype: Decimal

    :Example:
    >>> monerowallet.atomic_to_coins(10000000000000)
    Decimal('10.0')

    '''
    return units / Decimal(1000000000000)


def coins_to_atomic(coins):
    '''
    Converts Monero coins to Monero atomic units. One coin is 1e12 atomic units.

    :param coins: Monero coins which are converted to atomic units
    :type coins: Decimal or float

    :return: Atomic units
    :rtype: int

    :Example:
    >>> monerowallet.coins_to_atomic(10)
    10000000000000

    '''
    return int(coins * 1000000000000)
