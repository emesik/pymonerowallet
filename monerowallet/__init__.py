import requests

class MoneroWallet(object):
    '''MoneroWallet class'''

    def __init__(self):
        self.server = {'protocol': 'http', 'host': '127.0.0.1', 'port': 18082, 'uri': '/json_rpc'}
        self.data = {"jsonrpc": "2.0","id": "0"}
        self.main()

    def main(self):
        '''Main of MoneroWallet class'''
        pass

    def getbalance(self):
        '''Return the wallet's balance.'''
        self.__sendrequest('getbalance')

    def getaddress(self):
        '''Return the wallet's address.'''
        self.__sendrequest('getaddress')

    def getheight(self):
        '''Returns the wallet's current block height.'''
        pass

    def transfer(self):
        '''Send monero to a number of recipients.'''
        pass


    def transfer_split(self):
        '''Same as transfer, but can split into more than one tx if necessary.'''
        pass

    def sweep_dust(self):
        '''Send all dust outputs back to the wallet's, to make them easier to spend (and mix).'''
        pass

    def store(self):
        '''Save the blockchain.'''
        pass

    def get_payments(self):
        '''Get a list of incoming payments using a given payment id.'''
        pass

    def get_bulk_payments(self):
        '''Get a list of incoming payments using a given payment id, or a list of payments ids, from a given height. This method is the preferred method over get_payments because it has the same functionality but is more extendable. Either is fine for looking up transactions by a single payment ID.'''
        pass

    def incoming_transfers(self):
        '''Return a list of incoming transfers to the wallet.'''
        pass

    def query_key(self):
        '''Return the spend or view private key.'''
        pass

    def make_integrated_address(self):
        '''Make an integrated address from the wallet address and a payment id.'''
        pass

    def split_integrated_address(self):
        '''Retrieve the standard address and payment id corresponding to an integrated address.'''
        pass

    def stop_wallet:
        '''Stops the wallet, storing the current state.'''
        pass

    def __sendrequest(self, reqtype):
        '''Send a request to the server'''
        self.data['method'] = reqtype
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        req = requests.post('{protocol}://{host}:{port}{uri}'.format(url=self.server['protocol'],
                                                                     host=self.server['host'],
                                                                     port=self.server['port'],
                                                                     uri=self.server['uri']),
                                                                     headers=self.header,
                                                                     data=self.data)
        if req.status_code >= 200 and req.status_code <= 299:
            return {'status': req.status_code, result: req.json}
        else:
            return {'status': req.status_code, result: {}}
